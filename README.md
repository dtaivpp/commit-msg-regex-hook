# commit-msg-regex-hook

This hook is designed to be used with the [pre-commit](https://pre-commit.com/) hook framework. It will check your commit string against the provided regex. 


### Using the commit-msg-regex-hook

First you will need to setup [pre-commit](https://pre-commit.com/) using their documentation. 

Next you will need to enable commit message hooks: 
`pre-commit install --hook-type commit-msg`

Finally you can add this to your .pre-commit-config.yaml:

```
- repo: https://github.com/dtaivpp/commit-msg-regex-hook
  rev: v0.2.0
  hooks:
    - id: commit-msg-regex-hook
      args: ["--pattern='[A-Z]{3,4}-[0-9]{3,6} \\| [\\w\\s]* \\| .+'",
             "--failure_message='Commits should match the pattern: Card-ID | Name | Message'"]
      stages: [commit-msg]
```

**note: the backslashes in regex need to be escaped need to be escaped
**double note: if you are having issues you can run with the --debug argument as well for additional logging.

With this you can achieve so many things. A good example is verifing deveopers have signed the DCO before allowing a commit. 

```
- repo: https://github.com/dtaivpp/commit-msg-regex-hook
  rev: v0.2.0
  hooks:
    - id: commit-msg-regex-hook
      args: ["--pattern='Signed-off-by: .* <(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|'(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*')@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])>'",
             "--failure_message='Ensure you are signing the DCO'"]
      stages: [commit-msg]
```

### Developing this project

If you would like to contribute to this project I am happy to accept contributions. Small note I use two spaces for indents and am not looking to swap. 

Here is how you can contribute: 

1. Fork the repo
2. Create a virtual envrionment `python -m venv venv`
3. Activate the virtual environment:
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`
4. Install the reqirements `python -m pip install -r requirements.txt`
5. Install our hooks:
  - `pre-commit install`

And you are off to the races!

Before committing I would reccomend checking your build against unittest and the linter. If it doesn't pass it wont pass! 
- `python -m unittest test/test.py`
- `python -m pylint commit_msg_regex_hook`

Make sure if you add a check to add a test case!