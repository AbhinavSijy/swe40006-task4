# SWE40006 Task 4 – Container Application Deployment with Docker

**Student:** Abhinav Sijy (105337787)
**Unit:** SWE40006 Software Deployment and Evolution

| Folder | Task | Description | Docker Hub image |
|---|---|---|---|
| `flask-app/` | 4.2 | Basic Flask web app | [abhinav5690/swe40006-flask](https://hub.docker.com/r/abhinav5690/swe40006-flask) |
| `fastapi-app/` | 4.3 | FastAPI status page: optimised multi-stage Dockerfile, env-var config, non-root user, health check | [abhinav5690/swe40006-fastapi](https://hub.docker.com/r/abhinav5690/swe40006-fastapi) |
| `csv-report/` | 4.4 | Non-web CLI tool that summarises CSV files: bind mount + named volume, multi-platform (amd64/arm64) image | [abhinav5690/swe40006-csv-report](https://hub.docker.com/r/abhinav5690/swe40006-csv-report) |

**Live 4.3 deployment (Azure VM):** http://172.196.49.172

## 4.2 – Flask app

```bash
cd flask-app
docker build --platform linux/amd64 -t abhinav5690/swe40006-flask:1.0 .
docker run -d --name flask-app -p 8080:5000 abhinav5690/swe40006-flask:1.0
# open http://localhost:8080
```

## 4.3 – FastAPI app

Runtime configuration lives in `app.env` (not committed). Copy the example first:

```bash
cd fastapi-app
cp app.env.example app.env
docker build --platform linux/amd64 -t abhinav5690/swe40006-fastapi:1.0 .
docker run -d --name fastapi-app --env-file app.env -p 8000:8000 abhinav5690/swe40006-fastapi:1.0
# open http://localhost:8000  (also /api/info, /health, /docs)
```

Production deployment on the Azure VM:

```bash
docker network create swe40006-net
docker run -d --name fastapi-app --network swe40006-net --env-file app.env \
  -p 80:8000 --restart unless-stopped abhinav5690/swe40006-fastapi:1.0
```

## 4.4 – csv-report CLI tool

```bash
cd csv-report
docker build --platform linux/amd64,linux/arm64 -t abhinav5690/swe40006-csv-report:1.0 .
docker volume create csv-reports
docker run --rm -v "$PWD/data":/data/input:ro -v csv-reports:/data/output \
  abhinav5690/swe40006-csv-report:1.0
```

Options: `--input`, `--output`, `--log-level` (see `--help`).
Exit codes: `0` success · `1` finished with skipped files · `2` nothing to process.
