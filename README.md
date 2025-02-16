# Data Management Project README

## Important Files

1. The directory **documents** contains the report for the *Data Management Plan, ETL for Maximum Daily Temperature in the Atlántico region, Colombia*. main.pdf

2. The document *main.pdf* second page, we are able to find the #Class Problems given in the first part of the course focused on: `touch`, `chmod`, `sh`, `|` , and `>` commands on the terminal interface

3. If you are planning to run the web scrapping on yor local, and see the process: you should have installed a [chrome driver](https://developer.chrome.com/docs/chromedriver/downloads?hl=es-419) compatible with your chrome browser version.

4. Selenium is running in *headless* mode with the container, you should comment this lines and and uncoment the lines to see it on head mode: src/chromedriver_config.py

5. The data downloaded in this process is format zip, and is called: Reporte de información Hidrometeorológica de DHIME generado.zip stored on data/bronze. This data is transformed as follows:
    a. The After downloaded the orchestrator invoques the module preprocessing.py which contations the functions: 

        ```
        extract_zip_file(file_path, output_path_bronze)
        get_csv_files(file_path, output_path_bronze)
        load_csv_data(output_path_bronze, file_path)
        filtering_data(output_path_bronze:str, output_path_silver, file_path:str)
        ```
        
    b. The final product is a CSV file with Fecha and temperature columns. This data is stored on data/silver/dailymaxtemperature.csv

6. The file src/orchestrator.py, orchestrates the entire ETL process

7. Last, but not least...It is added, an additional exploratory data analysis focused on the statistical nature of the data; this can be found on notebooks/exploratory_data_analysis.ipynb.


# Prerequisites

- Python 3.10
- ChromeDriver (`133.0.6943.98`) or similar version than your browser
- Google Chrome (`133.0.6943.98`)

```sh
    curl -o url/chromedriver.zip
    unzip chromedriver.zip
    sudo mv chromedriver /usr/local/bin/
```

## Docker Image

### Build and Run the Docker Image:
1. **Build the Docker Image**
    ```sh
    docker build -t dm_project .
    ```

2. **Run the Docker Image Locally**
    ```sh
    docker run --rm -v $(pwd)/data:/data dm_project
    ```
    - `--rm`: Automatically removes the container after it stops, keeping the environment clean.
    - `-v $(pwd)/data:/data`: Mounts the local `data` directory into the container to allow reading/writing files.
    - `dm_project`: The name of the Docker image you built.

## Setting Up and Running Tests

### 1. Create a Virtual Environment:
```sh
cd /path/to/your/project_root
python -m venv .venv
```

### 2. Activate the Virtual Environment:
- **On Unix/macOS:**
    ```sh
    source .venv/bin/activate
    ```
- **On Windows:**
    ```sh
    .venv\Scripts\activate
    ```

### 3. Install Dependencies:
```sh
    pip install -r requirements.txt
```

## Extract, load and transform (ETL) excecution

The module that **orchestrates** the ETL process is located on src/orchestrator.py

To run this module, from your main folder and with the environment activated

```sh
    python path/src/orchestrator.py
```

## Optional Steps:

###  Run Tests:
To run individual tests:
```sh
.venv/bin/python -m pytest -v tests/test_extraction.py
```

To check the Python interpreter being used:
```sh
which python
```

### Removing the Virtual Environment
```sh
deactivate
rm -rf .venv
```

## Installing and Using `pyenv`

### 1. Install `pyenv`:
```sh
curl https://pyenv.run | bash
```

### 2. Add `pyenv` to Your Shell:
```sh
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### 3. Install and Set Python 3.10 (Project's Python Version):
```sh
pyenv install 3.10
pyenv local 3.10
```

## Directory Structure:
```
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
├── notebooks
│   ├── exploratory_data_analysis.ipynb
│   └── test_.ipynb
├── reports
├── requirements.txt
├── src
│   ├── data_extraction.py
│   ├── preprocessing.py
│   └── other_source_files.py
└── tests
    ├── test_extraction.py
    ├── test_orchestrator.py
    └── test_preprocessing.py
```
