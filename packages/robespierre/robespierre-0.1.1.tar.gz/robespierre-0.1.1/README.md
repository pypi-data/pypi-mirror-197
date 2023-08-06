# Robespierre
[Robespierre](https://gitlab.com/daufinsyd/robespierre) is a wrapper for [scorch](https://github.com/trapexit/scorch) to automate tests and send report per email.

## Installation
Simply install it from pip
```
pip3 install robespierre
```

## Usage
Copy the config.toml.example to config.toml and change the values according to your need.

Email section is mandatory if you wish to send reports per email.

```
robespierre --debug run --config path/to/config.toml --show-out
```

## Copyright
This program is distributed under the AGPL Licence. See LICENCE file.
Developer: Sydney Gems

All credits for scorch itself goes to [tapexit](https://github.com/trapexit) and contributors.
