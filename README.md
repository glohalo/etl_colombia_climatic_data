# Docker Image

To build and run the Docker image:

```sh
docker build -t notebooks-dev .
```
```sh
docker run -p 8888:8888 notebooks-dev
```

# Set up and Run Tests
1. Create virtual environment
```sh
    cd /path/to/your/project_root
```
```sh
    python -m venv .venv
```
2. Activate the virtual environment

    -  On Unix/macOs
        ```sh
            source .venv/bin/activate
        ```
    - On windows
        ```sh
            .venv\Scripts\activate
        ```
3. Install Dependencies:
```sh
    pip install -r requirements.txt
```
4. Excecute tests
```sh
.venv/bin/python -m pytest -v tests/test_extraction.pywhich python
```

### Explanation:

1. **Docker Image**:
    - Instructions to build and run the Docker image.

2. **Set Up and Run Tests**:
    - Step-by-step instructions to create, activate, and remove a virtual environment.
    - Instructions to install dependencies and run tests.

3. **Installing pyenv**:
    - Instructions to install `pyenv`, add it to your shell, and install the required Python version.

By following these steps, you can set up your development environment, run tests, and manage Python versions using `pyenv`. Adjust the paths and commands as needed for your specific project.

### Nice-to-have

#### Remove Virtual Environment
```sh
deactivate
```
```sh
rm -rf -venv
```
#### Installing pyenv
1. Install pyenv

```sh
curl https://pyenv.run | bash
```

2. Add pyenv to you shell
```sh
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

#Install the python version (this project is developed with python 3.10)
    pyenv install 3.10
```

3. Set the python version globally for the specific directory
```sh
pyenv local 3.10
```
