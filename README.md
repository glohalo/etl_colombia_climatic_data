
# 🌦️ ETL & Data Analysis Pipeline for Colombian Meteorological Data

This project builds an automated ETL (Extract, Transform, Load) pipeline to extract hydrometeorological data (e.g., maximum daily temperatures) from Colombia’s IDEAM/DHIME web portal.

It also includes a containerized setup (via Docker), virtual environment support, and advanced data exploration using statistical tests and visualization techniques.


## Project Structure

```
.
├── README.md
├── data/
│   ├── bronze/    ← Raw zipped files downloaded from DHIME
│   ├── silver/    ← Cleaned CSV files
│   └── gold/      ← (Optional) Further processed datasets
├── documents/
│   ├── rdmp.pdf   ← Data Management Plan 
├── notebooks/
│   └── exploratory_data_analysis.ipynb
├── src/
│   ├── orchestrator.py         ← Main pipeline controller
│   ├── data_extraction.py      ← Web scraping using Selenium
│   ├── preprocessing.py        ← Unzipping and cleaning data
│   ├── exploratory_functions.py← Custom EDA/statistics utilities
│   ├── chromedriver_config.py  ← Headless Chrome config for Selenium
│   └── variables.py            ← Dictionary of hydromet variables
├── requirements.txt
├── Dockerfile
└── tests/
    ├── test_extraction.py
    ├── test_orchestrator.py
    └── test_preprocessing.py
```


## Pipeline Overview

1. **Extraction** (`data_extraction.py`)
   - Uses Selenium to simulate interaction with the DHIME web platform.
   - Accepts parameters like `variable`, `station code`, `department`, and `date range`.

2. **Transformation** (`preprocessing.py`)
   - Unzips raw `.zip` files into `.csv`.
   - Cleans and filters relevant columns (e.g., `Fecha`, `Valor`).
   - Stores the output in `data/silver/dailymaxtemperature.csv`.

3. **Exploration** (`exploratory_data_analysis.ipynb`)
   - Utilizes advanced statistical diagnostics (KPSS, ADF, Box-Cox, Granger Causality).
   - Visual tools: histograms, seasonal decomposition, ACF/PACF, KDE plots.

4. **Automation** (`orchestrator.py`)
   - Controls the full ETL pipeline in one go.
   - Includes logging, retries, and error handling.


## 🐳 Docker Support

**Build:** From father repository
```sh
docker build -f dm_project_docker/Dockerfile -t dm_project_docker:latest dm_project
```

**Run:** from father repository
```sh
docker run -it --rm \
-v "$(pwd)":/workspace \
-w /workspace \
-e PYTHONPATH=/workspace/src \
dm_project_docker:latest \
python3 -m src.orchestrator
```

> Chrome runs in **headless mode** for containers. To visualize browser activity (e.g., debugging), disable headless mode in `src/chromedriver_config.py`.


## 🧪 Testing

**Unit Test Entry Points:**
- `test_extraction.py`
- `test_orchestrator.py`
- `test_preprocessing.py`

**Run tests:**
```sh
pytest -v tests/
```

## Setup Instructions (Local)

### 1. Python & Chrome Requirements

- Python 3.10
- Chrome (v133.0.6943.98 or matching)
- Compatible [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads)

### 2. Setup Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the ETL

Once set up:

```bash
python src/orchestrator.py
```

## Exploratory Data Analysis (EDA)

Open and run the notebook:

```bash
jupyter notebook notebooks/exploratory_data_analysis.ipynb
```

It contains:
- Temporal trends
- Seasonality detection
- Statistical stationarity checks
- Distribution diagnostics
- Granger causality tests

---

## 📎 Notes 

- The raw `.zip` file is saved under `data/bronze/`.
- The cleaned `.csv` file is stored under `data/silver/dailymaxtemperature.csv`.
- Additional processed outputs may be stored in `data/gold/` (planned extension).
- The exploratory functions in `exploratory_functions.py` are modular and reusable.

## 🧠 Credits & Context

Developed as part of a Data Management course project to explore the integration of hydrometeorological data from open government portals into reproducible scientific workflows. This includes Dockerization, CI compatibility, and advanced data exploration.
