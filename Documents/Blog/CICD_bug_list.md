# CI/CD bug encountered during implementation

### gitlab-runner version
```
Version:        15.7.2
Git revision:   0e7679e6
Git branch:     15-7-stable
GO version:     go1.18.9
Built:          2023-01-13T23:55:39+0000
OS/Arch:        linux/amd64
```

Two bug were encountered during early stage of implementing CI/CD runner with shell and docker as executor. Both bug were fixed using the following links:

- [CI/CD not working with shell](https://gitlab.com/gitlab-org/gitlab-runner/-/issues/26605)

- [CI/CD Not working with docker](https://gitlab.com/gitlab-org/gitlab-runner/-/issues/27975)
