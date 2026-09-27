FROM python:3.12-alpine

LABEL org.opencontainers.image.title="csv-report" \
      org.opencontainers.image.description="CLI tool that summarises numeric columns in CSV files" \
      org.opencontainers.image.authors="Abhinav Sijy" \
      org.opencontainers.image.source="https://github.com/AbhinavSijy/swe40006-task4"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN adduser -D -u 10001 appuser \
 && mkdir -p /data/input /data/output \
 && chown appuser:appuser /data/output

WORKDIR /app
COPY --chown=appuser:appuser app/csv_report.py .

USER appuser
VOLUME ["/data/output"]

ENTRYPOINT ["python", "/app/csv_report.py"]
CMD ["--log-level", "INFO"]
