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

