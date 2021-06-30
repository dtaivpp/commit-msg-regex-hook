"""This is an commit-msg stage hook.
It is made as a custom plugin under the https://pre-commit.com
hook framework and checks if commit message matches
the provided regex.
"""

import sys
import argparse
import re
from typing import Pattern

# Default commit message path
COMMIT_EDITMSG = ".git/COMMIT_EDITMSG"
PASS=True
FAIL=False


class Result():
  """Class for denoting pass/fail and why for test
  """
  def __init__(self, message, result):
    self.message = message
    self.result = result

  def is_passing(self):
    return self.result


def main():
    """Perform validations of the commit message.
    Parse passed in regex and verify message matches
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("message", nargs="?", type=process_file, default=COMMIT_EDITMSG,
                        help="File path for commit message")
    parser.add_argument("pattern", type=process_pattern, required=True)
    parser.add_argument(
      '--debug',
      action='store_true', 
      help='print debug messages to stderr'
    )

    args = parser.parse_args()

    checks = [
      message_not_empty(args.message),
      message_pattern_match(args.message, args.pattern)
    ]

    for check in checks:
      result = check()
      
      if not result.is_passing():
        print(f"Check Failed:\n {result.message}")
        sys.exit(1)

      if args.debug:
        print(result.message)

    sys.exit(0)


def process_file(path: str) -> str:
  """Extract commit message.  
  On failure the commit is aborted. 

  Args:
      path (str): The path of the file with commit message
  Returns:
      str: The commit message.
  """
  try:
    with open(path, "r", encoding="utf-8") as file:
      msg = file.read()
  except FileNotFoundError:
    raise argparse.ArgumentError(f"File does not exist: \n\t{path}")

  return msg


def process_pattern(pattern: str) -> Pattern:
  """Verify regex pattern and return the pattern object
  """
  try:
    pattern = re.compile(pattern)
  except Exception as e:
    raise argparse.ArgumentTypeError(
      f"'{pattern}' is not a valid regex pattern\n {e}"
    )

  return pattern


def message_not_empty(message: str) -> Result:
  """Verify the commit message is not empty
  """
  def check():
    if len(message.strip()) == 0:
      return Result(f"ֿError: commit message cannot be empty", FAIL)
    
    return Result(f"The commit message is not empty", PASS)
  return check


def message_pattern_match(msg: str, pattern: str) -> Result:
  """Verify the commit message matches the pattern
  """
  def check():
    if not re.match(pattern, msg):
      # Fail the commit message
      return Result(f"Commit Message does not match pattern\n\t{pattern}\n\t{msg}", FAIL)
    
    return Result(f"The commit message matches the regex", PASS)
  return check


if __name__=="__main__":
  exit(main())
