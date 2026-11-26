FROM python:3.13-alpine3.24@sha256:1e1f6334529d1fb26a2ef619d7cffb30a7c7d7cc1cc7338ebee283a58d1aeaca AS dependencies
COPY requirements.lock /requirements.lock
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir --only-binary=:all: --require-hashes -r /requirements.lock

FROM python:3.13-alpine3.24@sha256:1e1f6334529d1fb26a2ef619d7cffb30a7c7d7cc1cc7338ebee283a58d1aeaca AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH=/opt/venv/bin:$PATH
WORKDIR /app
COPY --chown=10001:10001 requirements.lock /app/requirements.lock
COPY --chown=10001:10001 LICENSE NOTICE /app/
COPY --from=dependencies /opt/venv /opt/venv
RUN /opt/venv/bin/python -m pip uninstall -y pip \
    && /usr/local/bin/python -m pip uninstall -y pip \
    && addgroup -g 10001 app \
    && adduser -D -H -u 10001 -G app app \
    && mkdir -p /var/lib/spec-enricher /backups /exports /config /sources \
    && chown 10001:10001 /var/lib/spec-enricher /backups /exports \
    && chmod 700 /var/lib/spec-enricher /backups /exports
COPY --chown=10001:10001 spec_enricher /app/spec_enricher
COPY --chown=10001:10001 catalog/requirements.schema.json catalog/requirements.full.json /app/catalog/
COPY --chown=10001:10001 templates /app/templates
COPY --chown=10001:10001 sources /app/sources
COPY --chown=10001:10001 qa /app/qa
USER 10001:10001
ENV APP_HOST=0.0.0.0 APP_PORT=8080 APP_DATA_DIR=/var/lib/spec-enricher APP_ALLOWED_ORIGIN=http://127.0.0.1:8080
EXPOSE 8080
CMD ["python", "-m", "spec_enricher.cli", "serve"]
