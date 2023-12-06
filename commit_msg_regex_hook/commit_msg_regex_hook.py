"""This is an commit-msg stage hook.
It is made as a custom plugin under the https://pre-commit.com
hook framework and checks if commit message matches
the provided regex.
"""

import sys
import argparse
import re
import logging
from typing import Pattern


logger = logging.getLogger("__main__")
logger.setLevel(logging.ERROR)
consoleHandle = logging.StreamHandler()
consoleHandle.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
consoleHandle.setFormatter(formatter)
logger.addHandler(consoleHandle)


# Default commit message path
COMMIT_EDITMSG = ".git/COMMIT_EDITMSG"
PASS=True
FAIL=False


class Result():
  """Class for denoting pass/fail and why for test
  """
  def __init__(self, message, result, debug_data=None):
    self.message = message
    self.debug_data = debug_data
    self.result = result

  def is_passing(self):
    """Whether the result is a passing or failing result
    """
    return self.result


def main():
  """Perform validations of the commit message.
  Parse passed in regex and verify message matches
  """
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "message", 
    nargs="?", 
    type=process_file, 
    default=COMMIT_EDITMSG,
    help="File path for commit message")


  parser.add_argument(
    "--failure_message", 
    type=str, 
    default="Commit Message does not match pattern", 
    help="The message to display if the commit message doesn't match the Regex")


  parser.add_argument(
    "--pattern",
    type=process_pattern,
    help="Pattern to check the commit message against")


  parser.add_argument(
    "--debug",
    action="store_true",
    help="Flag to get debugging messages")


  args = parser.parse_args()

  if args.debug:
    logger.setLevel(logging.DEBUG)

  checks = [
    message_not_empty(args.message),
    message_pattern_match(args.message, args.pattern, args.failure_message)
  ]

  run_checks(checks)


def run_checks(checks: list):
  """Processs the checks and in the event of a failure
  kill the commit
  """
  for check in checks:
    result = check()

    if not result.is_passing():
      logger.error(f"Check Failed:\n {result.message}")
      logger.debug(result.debug_data)
      sys.exit(1)

    logger.debug(result.message)

  sys.exit(0)


def process_file(path: str) -> str:
  """Extract commit message.

  Args:
      path (str): The path of the file with commit message
  Returns:
      str: The commit message.
  """
  try:
    with open(path, "r", encoding="utf-8") as file:
      msg = file.read()
  except FileNotFoundError as file_not_found:
    raise argparse.ArgumentTypeError(f"File does not exist: \n\t{path}") from file_not_found

  return msg


def process_pattern(str_pattern: str) -> Pattern:
  """Convert string pattern to regex pattern object.

  Args:
      pattern_str (str): The path of the file with commit message
  Returns:
      pattern (Pattern): The compiled regex pattern.
  """
  try:
    pattern = re.compile(str_pattern[1:-1])
  except Exception as err:
    raise argparse.ArgumentTypeError(
      f"'{str_pattern}' is not a valid regex pattern\n {err}"
    )

  return pattern


def message_not_empty(message: str) -> Result:
  """Verify the commit message is not empty
  """
  def check():
    logger.debug(f"Current Message: {message}")

    if len(message.strip()) == 0:
      return Result("ֿError: commit message cannot be empty", FAIL)

    return Result("The commit message is not empty", PASS)
  return check


def message_pattern_match(message: str, pattern: Pattern, failure_message: str) -> Result:
  """Verify the commit message matches the pattern
  """
  def check():
    logger.debug(f"Pattern: {pattern}\nMessage: {message}")

    if not pattern.search(message):
      # Fail the commit message
      return Result(f"{failure_message}\n", 
                    FAIL, 
                    f"\tPattern: {pattern}\n\tMessage: {message}")

    return Result("The commit message matches the regex", PASS)
  return check


if __name__=="__main__":
  exit(main())
