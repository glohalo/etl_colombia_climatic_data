# Docker image

docker build -t notebooks-dev .
docker run -p 8888:8888 notebooks-dev

## Set up and Run Tests
1. Create virtual environment
    cd /path/to/your/project_root
    python -m venv .venv

2. Activate the virtual environment

    -  On Unix/macOs
        source .venv/bin/activate
    - On windows
        .venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Excecute...
- .venv/bin/python -m pytest -v tests/test_extraction.pywhich python

Remove venv
- deactivate
- rm -rf -venv

installing pyenv
- curl https://pyenv.run | bash
Add pyenv to you shell
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
Install the python version (this project is developed with python 3.10)
-   pyenv install 3.10

# set the python version globally for the specific directory
- pyenv local 3.10