import re
import unittest
from src import commit_msg_regex_hook


class TestMessageEmpty(unittest.TestCase):
  def test_empty_message_should_fail(self):
    result = commit_msg_regex_hook.message_not_empty(" \n")()
    self.assertEqual(result.is_passing(), False)

  def test_full_message_should_pass(self):
    result = commit_msg_regex_hook.message_not_empty("I am a whole message")()
    self.assertEqual(result.is_passing(), True)


class TestMessagePatternMatch(unittest.TestCase):
  def test_pattern_not_match(self):
    pattern = re.compile(r'[A-Z]{3,4}-[0-9]{3,6} \| [\w\s]* \| .+')
    test_str = "asefagrragadsrgasr"
    result = commit_msg_regex_hook.message_pattern_match(test_str, pattern)()
    self.assertEqual(result.is_passing(), False)

  def test_pattern_match(self):
    pattern = re.compile(r'[A-Z]{3,4}-[0-9]{3,6} \| [\w\s]* \| .+')
    test_str = "ABC-123 | David | Commit message!"
    result = commit_msg_regex_hook.message_pattern_match(test_str, pattern)()
    self.assertEqual(result.is_passing(), True)
