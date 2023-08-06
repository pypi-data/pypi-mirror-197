import enum
import logging
import robespierre
from typing import List, Any


class ReportFormat(str, enum.Enum):
    RAW = "raw"


class Command:
    _main_config: "MainConfig"  # backref to MainConfig
    _name: str  # name of itself
    db_name: str
    directory_name: str
    instructions: List[str]
    options: List[Any]
    send_report: bool
    rcpt_emails: List[str]  # TODO Not used
    # rcpt_emails=["me+check_dbs@mail.com"]  # optional, mail to send report to, instead of default_recipients ; NOT IMPLEMENTED

    def __init__(self, db_name: str, directory_name: str, instructions: List[str], rcpt_emails: List[str] = None, options: List[Any] = None, send_report: bool = False) -> None:
        if rcpt_emails is None:
            rcpt_emails = []
        if options is None:
            options = []
        self.db_name = db_name
        self.directory_name = directory_name
        self.instructions = instructions
        self.options = options
        self.send_report = send_report
        self.rcpt_emails = rcpt_emails

    def get_db(self) -> "Database":
        return self._main_config.databases.get_db_by_name(self.db_name)

    def get_directory(self) -> "Directory":
        return self._main_config.directories.get_directory_by_name(self.directory_name)

    def get_name(self):
        return self._name

    def is_send_report(self) -> bool:
        return self.send_report or self._main_config.config.defaults.send_report

    def set_main_config(self, main_config):
        self._main_config = main_config

    def set_command_name(self, name):
        self._name = name


class Commands:
    _command_names: list[str] = []
    _main_config: "MainConfig"

    def __init__(self, commands: dict, main_config: "MainConfig") -> None:
        self._main_config = main_config
        for key in commands:
            cmd = Command(**commands[key])
            cmd.set_main_config(self._main_config)  # backref to mainConfig
            cmd.set_command_name(key)  # make Cmd aware of its name
            setattr(Commands, key, cmd)
            self._command_names.append(key)

    def get_all_command(self) -> list[Command]:
        return [self.__getattribute__(x) for x in self._command_names]


class Defaults:
    send_report: bool
    report_format: str

    def __init__(self, send_report: bool = False, report_format: ReportFormat = ReportFormat.RAW) -> None:
        try:
            report_format = ReportFormat(report_format.lower())
        except ValueError:
            report_format = ReportFormat.RAW
            if robespierre.DEBUG:
                logging.exception("Provided report format is not valid. Using 'raw'.")
            else:
                logging.warning("Provided report format is not valid. Using 'raw'.")

        self.send_report = send_report
        self.report_format = report_format


class Email:
    relay_host: str
    relay_port: int
    use_tls: bool
    sender: str
    default_recipients: List[str]
    password: str

    def __init__(self, sender: str, default_recipients: List[str], password, relay_host: str, relay_port: int = 465, use_tls: bool = True) -> None:
        self.relay_host = relay_host
        self.relay_port = relay_port
        self.sender = sender
        self.default_recipients = default_recipients
        self.password = password
        self.use_tls = use_tls


class Database:
    path: str

    def __init__(self, path: str) -> None:
        self.path = path


class Databases:
    _db_names: list[str] = []  # Keep db names so that we can enumerate Databases

    def __init__(self, databases: dict) -> None:
        for key in databases:
            setattr(Databases, key, Database(**databases[key]))
            self._db_names.append(key)

    def get_all_db(self) -> list[Database]:
        return [self.__getattribute__(x) for x in self._db_names]

    def get_db_by_name(self, db_name) -> Database:
        return self.__getattribute__(db_name)


class Directory:
    path: str

    def __init__(self, path: str) -> None:
        self.path = path


class Directories:
    _directory_names: list[str] = []  # Keep dir names so that we can enumerate Directories

    def __init__(self, directories: dict) -> None:
        for key in directories:
            setattr(Directories, key, Directory(**directories[key]))
            self._directory_names.append(key)

    def get_all_directory(self) -> list[Directory]:
        return [self.__getattribute__(x) for x in self._directory_names]

    def get_directory_by_name(self, directory_name) -> "Directory":
        return self.__getattribute__(directory_name)


class Config:
    defaults: Defaults
    email: Email

    def __init__(self, defaults: dict, email: dict = None) -> None:
        self.defaults = Defaults(**defaults)
        if email:
            self.email = Email(**email)


class MainConfig:
    databases: Databases
    directories: Directories
    commands: Commands
    config: Config
    version: float

    def __init__(self, databases: dict, directories: dict, commands: dict, config: dict, version: float = 1.0) -> None:
        self.databases = Databases(databases)
        self.directories = Directories(directories)
        self.commands = Commands(commands, self)
        self.config = Config(**config)
        self.version = version

    def get_default_mail_rcpt(self):
        if self.config.email:
            return self.config.email.default_recipients
        else:
            return []
