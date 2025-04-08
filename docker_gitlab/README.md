# 🐳 dm_project_repository

> Reproducible ETL pipeline for maximum daily temperature in Atlántico, Colombia — containerized with Selenium + Chromium and ready for GitLab CI/CD deployment.

---

## Repository Contents

- `Dockerfile` – container setup using `seleniarm/standalone-chromium` as base image
- `.gitlab-ci.yml` – CI/CD for building and pushing Docker images
- `requirements.txt` – Python + Jupyter + Selenium + Stats stack

## Dockerfile Highlights

Real base image:  
```Dockerfile
FROM seleniarm/standalone-chromium:latest
```

### Key layers:
- Installs essential Linux libs (`libgtk-3-0`, `libnss3`, etc.)
- Adds Python 3, `venv`, `pip`
- Installs [**Quarto CLI**](https://quarto.org/) for report rendering
- Sets up virtual environment & installs `requirements.txt`
- Adds `src/`, `notebooks/`, `data/`, `documents/`, `tests/`
- Entry point: 
```Dockerfile
CMD ["python3", "-m", "src.orchestrator.py"]
```

> Uses `USER root` for installs, switches back to Selenium user for safety.


## GitLab CI/CD Workflow

`.gitlab-ci.yml` performs:

- `clone` → fetch from `$APP_REPO`
- `rsync` → clean sync without `documents/`
- `docker build` → fresh build with short SHA tag
- `docker push` → pushes to `$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA`

Set these vars in GitLab:

```
GIT_USERNAME
GIT_PASSWORD
CI_REGISTRY
CI_REGISTRY_USER
CI_REGISTRY_PASSWORD
```

## Run Locally

```bash
# Build (optional, no cache)
docker build --no-cache -f dm_project_docker/Dockerfile -t dm_project_docker:latest dm_project

# Run, repository dm_project
docker run -it --rm \
-v "$(pwd)":/workspace \
-w /workspace \
-e PYTHONPATH=/workspace/src \
dm_project_docker:latest \
python3 -m src.orchestrator
```

## Clean Up

```bash
docker system prune -f
```

---
## Credits

Developed for academic use at Leipzig University.  
Hydrometeorological data courtesy of [IDEAM – DHIME](http://dhime.ideam.gov.co/).



