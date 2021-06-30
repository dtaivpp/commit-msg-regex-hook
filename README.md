# commit-msg-regex-hook

Before the readme, big shoutout to @dimaka-wix who's repo [commit-msg-hook](https://github.com/dimaka-wix/commit-msg-hook) was the basis for this repository. Go check out his repo for more information. 

This hook is designed to be used with the [pre-commit](https://pre-commit.com/) hook framework. It will check your commit string against the provided regex. 

### Utilizing

First you will need to setup [pre-commit](https://pre-commit.com/) using their documentation. Then you will be able to add this repository under it with the following:

```
- repo: https://github.com/dimaka-wix/commit-msg-hook.git
  rev: v0.3.1
  hooks:
    - id: commit-msg-hook
      args: ["regex='[A-Z]{3,4}-[0-9]{3,6} \| [\w\s]* \| .+'"]
      stages: [commit-msg]
```

#### To enable commit-msg hook with pre-commit run:
`pre-commit install --hook-type commit-msg`

#### Update to the latest release (optional)
`pre-commit autoupdate --repo https://github.com/dtaivpp/commit-msg-regex-hook.git`