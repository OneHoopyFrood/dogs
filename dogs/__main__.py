import sys

from dogs.cli import cli
from dogs.cli_app import CLIApp

if __name__ == "__main__":
  # If params were passed, run the cli
  # Otherwise, run the interactive shell
  if (sys.argv[1:]):
    cli()
  else:
    CLIApp().run()
