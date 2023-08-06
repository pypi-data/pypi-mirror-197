import logging
import os
import subprocess
import sys
import datetime

import robespierre
import robespierre.utils.mail as mail

if sys.version_info.major >= 3 and sys.version_info.minor >= 11:
    import tomlib
else:
    import tomli as tomlib
from robespierre.models import *
from robespierre.utils import files


def check_dbs(databases: Databases):
    """
    Check that databases are writable
    :param databases:
    :return:
    """
    logging.debug(databases)
    db: Database
    for db in databases.get_all_db():
        path = db.path
        try:
            with open(path, "a"):  # "w" also initialize the file
                logging.debug("Database {} is writable".format(path))
        except PermissionError:
            logging.error("Database {} is not writable".format(path))


def check_directories(directories: Directories):
    """
    Check that directories are readable
    :param directories:
    :return:
    """
    logging.debug(directories)
    directory: Directory
    for directory in directories.get_all_directory():
        path = directory.path
        if not os.path.exists(path):
            logging.error("Directory {} doesn't exist".format(path))
        elif not os.path.isdir(path):
            logging.error("Directory {} is not a directory".format(path))
        elif not os.access(path, os.R_OK):
            logging.error("Directory {} is not readable".format(path))
        else:
            logging.debug("Directory {} is ok".format(path))


def check_command(main_config: MainConfig, command: Command):
    """
    Check that command is valid and can be executed.
    :param main_config:
    :param command:
    :return:
    """
    logging.debug("Checking command {}".format(command.get_name()))
    is_valid = True
    if command.is_send_report():
        if not command.rcpt_emails and not main_config.get_default_mail_rcpt():
            logging.error("Report is enabled but no recipient was provided")
            is_valid = False
    # Check the referenced DB exists
    try:
        main_config.databases.get_db_by_name(command.db_name)
    except AttributeError:
        logging.error("Failed to find DB: {}.".format(command.db_name))
        is_valid = False
    # Check the referenced directory exists
    try:
        main_config.directories.get_directory_by_name(command.directory_name)
    except AttributeError:
        logging.error("Failed to find directory: {}.".format(command.directory_name))
        is_valid = False

    return is_valid


def execute_commands(main_config: MainConfig, commands: Commands):
    command: Command
    report_files = []
    for command in commands.get_all_command():
        if not check_command(main_config=main_config, command=command):
            logging.error("Command {} is invalid. Ignoring it.".format(command.get_name()))
            continue

        logging.info("Executing {}".format(command.get_name()))
        for instruction in command.instructions:
            scorch_exec_path = os.path.join(os.path.dirname(__file__), 'vendor/scorch')
            options: str = ""
            if command.options:
                options += " ".join(command.options)
            if robespierre.DEBUG and "-v" not in command.options and "--verbose" not in command.options:
                options += " -v"

            arg_line = "{} {} --db {} {} {}".format(scorch_exec_path, options, str(command.get_db().path), str(instruction), command.get_directory().path)
            cmd = ["bash", "-c", arg_line]
            logging.info("Running {}".format(cmd))

            out_file_path = "/tmp/robespierre-{}-{}-{}".format(command.get_name(), instruction, files.id_generator(6))
            with open(out_file_path, "w") as f:
                f.write("Running: {}\n".format(" ".join(cmd)))
                f.write("Time: {}\n".format(datetime.datetime.now()))
                f.flush()
                p = subprocess.Popen(cmd, stdout=f, stderr=f, bufsize=0)
                p.wait()
                f.write("Time: {}\n".format(datetime.datetime.now()))
                f.write("Done.")

                logging.debug("File written to: {}".format(f.name))

                if command.is_send_report():
                    logging.debug("Command is marked as need to send report. Adding output file to the list.")
                    report_files.append(f.name)

            if robespierre.SHOW_OUT:
                with open(out_file_path, "r") as f:
                    logging.debug(f.read())

    if report_files:
        # TODO rcpt list
        mail.send_mail(main_config=main_config, file_list=report_files)


def run(config):
    try:
        with open(config, 'rb') as f:
            data = tomlib.load(f)
    except tomlib.TOMLDecodeError:
        if robespierre.DEBUG:
            logging.exception("Provided config file isn't a valid toml file.")
        else:
            logging.critical("Provided config file isn't a valid toml file.")
        exit(1)
    except FileNotFoundError:
        if robespierre.DEBUG:
            logging.exception("Provided config file could not be found: {}".format(config))
        else:
            logging.critical("Provided config file could not be found: {}".format(config))
        exit(1)
    except PermissionError:
        if robespierre.DEBUG:
            logging.exception("No read access to the config file {}.".format(config))
        else:
            logging.critical("No read access to the config file {}.".format(config))
        exit(1)

    main_config: MainConfig = MainConfig(**data)

    check_dbs(databases=main_config.databases)
    check_directories(directories=main_config.directories)

    execute_commands(main_config=main_config, commands=main_config.commands)

