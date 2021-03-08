## Creating a new experiment

- Create a new repository under the [faasm org](
  https://github.com/faasm) called `experiment-<name>`.
- Create a Dockerfile
- Create benchmark scripts to run both the Faasm and native versions

The directory structure should look like: 

```bash
|-experiment-base/
|-experiment-newname/
|---README.md
|---Dockerfile
|---bin/
|------build_native.sh
|------build_faasm.sh
|---run/
|------faasm.sh
|------native.sh
```
