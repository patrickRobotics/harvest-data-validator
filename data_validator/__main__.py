"""Python Harvest Data Validator entry point script."""
# data_validator/__main__.py

from data_validator import cli, __app_name__


def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
