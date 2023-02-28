[Back to content page](README.md)

------

## CI/CD pipeline

### Initial Setup and runner
We have set up a CI/CD pipeline in our repository and it is configured using the [tutorial provided by GitLab](https://docs.gitlab.com/ee/ci/quick_start/).

CI/CD is enabled at the visibility, project features, permissions tab in project settings. Since GitLab runner is already installed in group's virtual machine(VM), only step is to register the VM as a runner using the instructions provided at [repository's CI/CD Settings](https://git.ecdf.ed.ac.uk/psd2223/Patrick__Barrera_and_Collins/-/settings/ci_cd) at the runner tab.

Currently only one runner (named: s1754999\_VM) is registered with "docker" as the executor, which means the VM is processing jobs using a container. This choice is made because our team member has experence using docker, and running with a docker image that ensure a clean environment to run test.

We plan to create a docker image with all dependences installed, reducing the CI/CD minutes as much as possible.

There is only a single runner register for group's VM, hence tags are not currently being used, which can be added to any runner by either at registration or editing the `config.toml` file as the project grows and there is a need for more runner.

### Pipeline
There are two main parts that are implemented into the pipeline:
- [Continuous Integration](#continuous-integration)
- [Continuous Delivery](#continuous-delivery)

#### Continuous Integration
One stage is related to CI are currently deployed to our pipeline, which is test.

A before script is currently used to install pytest and output the Python version. Which can be checked at all jobs' pipleline output.

Test stage currently includes two jobs, an echo test and a pytest. Currently the echo test echos to the pipleline output and pytest output its version then runs an empty test and output the .xml as an artifact which can now be view under the tests tab of the pipeline, this test is designed to fail as it runs an empty test. This is put here to ensure pytest is installed and useable. 

#### Continuous Delivery
Our pipeline currently is set up to echo only, but further in development we will implement it to automatically delivery the project once all test cases are passed, this is done to ensure our code quailty throughout the development stage.

### Additional function
GitLab provides more functions that we found useful for later in the development stage, which has not been implemented into the pipeline at the currently, including test and pipeline recroding using artifact. They are convered in recording section of [test plan](test_plan).

------

[Next: Test plan, failure management/communication and record](test_plan.md)
