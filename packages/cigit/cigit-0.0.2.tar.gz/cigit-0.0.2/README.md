# Welcome to **Ci-Git**

**Scripting** build(s) for **C**ontinuous **I**ntegration and **C**ontinuous **D**elivery (**CI/CD**)

## **Installation**

```sh
python -m pip install cigit
```

## **Credentials**

```yaml
# Git Config
url: https://github.com/hlop3z/cigit.git
path: ./demo

# Auth Config
username: hlop3z
password: (P)ersonal-(A)ccess-(T)oken
```

## **Pipeline**

```yaml
# Define Stages
stages:
  - build
  - test
  - deploy

# Define { build } stage jobs
build:
  stage: build
  script:
    - echo "Build"

# Define { test } stage jobs
unit_tests:
  stage: test
  script:
    - echo "Unit-Tests"

integration_tests:
  stage: test
  script:
    - echo "Integration-Tests"

# Define { deploy } stage jobs
deploy_to_staging:
  stage: deploy
  script:
    - echo "Deploy-To-Staging"

deploy_to_production:
  stage: deploy
  script:
    - echo "Deploy-To-Production"
```
