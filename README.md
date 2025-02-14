# Docker Image

To build and run the Docker image:

```sh
docker build -t dm_project .

```
Test locally to ensure that images run correctly
```sh
docker run --rm -v $(pwd)/data:/data dm_project

```
- -rm: Automatically removes the container after it stops, keeping things clean.
- -v $(pwd)/data:/src/data: Mounts the data directory from your local machine into the container, allowing your scripts to read/write files.
- main_dir: The name of the Docker image you built.

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
***should ad to run multiple tests individually
```sh
.venv/bin/python -m pytest -v tests/test_extraction.py 
which python
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
### Directory tree

.
├── README.md
├── data
│   ├── bronze
│   │   ├── descargaDhime.csv
│   │   └── report.zip
│   ├── gold
│   └── silver
│       ├── dailymaxtemperature.csv
│       ├── temperature_processed.csv
│       └── temperature_stationary.csv
├── dockerfile
├── documents
│   ├── figures
│   ├── main.pdf
│   └── main.qmd
├── notebook
├── notebooks
│   ├── exploratory_data_analysis.ipynb
│   └── test_.ipynb
├── reports
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── auxiliar_functions.cpython-310.pyc
│   │   ├── data_extraction.cpython-310.pyc
│   │   ├── exploratory_functions.cpython-310.pyc
│   │   ├── extraction.cpython-310.pyc
│   │   ├── extraction.cpython-313.pyc
│   │   ├── orchestrator.cpython-310.pyc
│   │   ├── preprocessing.cpython-310.pyc
│   │   ├── test.cpython-39-pytest-7.1.1.pyc
│   │   ├── variables.cpython-310.pyc
│   │   └── variables.cpython-313.pyc
│   ├── data_extraction.py
│   ├── exploratory_functions.py
│   ├── generate_report.py
│   ├── orchestrator.py
│   ├── preprocessing.py
│   └── variables.py
└── tests
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-310.pyc
    │   ├── __init__.cpython-313.pyc
    │   ├── __init__.cpython-39.pyc
    │   ├── test.cpython-39-pytest-7.1.1.pyc
    │   ├── test_extraction.cpython-310-pytest-8.3.4.pyc
    │   ├── test_extraction.cpython-313-pytest-8.3.4.pyc
    │   ├── test_extraction.cpython-39-pytest-7.1.1.pyc
    │   ├── test_orchestrator.cpython-310-pytest-8.3.4.pyc
    │   └── test_preprocessing.cpython-310-pytest-8.3.4.pyc
    ├── test_extraction.py
    ├── test_orchestrator.py
    └── test_preprocessing.py

#pip ,list
## selenium standalone docker image 
pull
docker pull selenium/standalone-chromium

run the container
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" seleniarm/standalone-chromium

configure the runner---> tomorrow :v

runner token: glrt-h-HPfTxx4Fi6GU9Fst6m

activate runner: sudo CONFIG_FILE=/etc/gitlab-runner/config.toml gitlab-runner run
## ensure the credentiasl on the .gitlab-ci.yml
## dockerconfig.json

1. ensuring credentiasl to check that my ci has the things configured manually (done!!! :)
2. find the dcoker config find / -name .docker/config.json 2>/dev/null
