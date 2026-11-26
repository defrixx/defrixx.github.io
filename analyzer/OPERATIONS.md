# Analyzer operations

[Back to the quick start](README.md)

## Data and updates

The named `app_data` Docker volume stores the database and artifacts. The local `config/`, `exports/`, and `backups/` directories are private and excluded from Git. **Never use `docker compose down -v` for an update.**

A fresh installation can optionally import a versioned `config/settings-bundle.json` once. It does not import credentials or grants; imported connections and bindings start disabled. Use the UI for later settings imports.

To stop without deleting data:

```sh
docker compose stop app
```

Before updating, finish or cancel active runs and create a backup. Then build the intended source revision and restart:

```sh
docker compose up -d --build app
docker compose ps
docker compose exec app python -m spec_enricher.cli bootstrap-url
```

Re-enter session credentials. If backend methodology changed, create a new analysis rather than resuming an incompatible run. Existing history remains readable.

## Backup and restore

Backups contain documents, prompts, and model outputs. **They are not encrypted.** Protect them as sensitive files. Session credentials and tokens are excluded.

After finishing or cancelling active runs:

```sh
docker compose exec app python -m spec_enricher.cli backup --output /backups/backup-local.tar.gz
```

The archive appears in `./backups`. Choose a new filename for each backup; existing files are not overwritten. The app coordinates database writes and records per-file hashes. Copying a live SQLite file is not an equivalent backup.

To restore into an empty installation using a compatible app version, place the archive in `backups/`, then:

```sh
docker compose stop app
docker compose run --rm --no-deps app python -m spec_enricher.cli restore --input /backups/backup-local.tar.gz
docker compose up -d app
docker compose exec app python -m spec_enricher.cli bootstrap-url
```

Restore rejects an active service, invalid archives, or a non-empty target. Intentional replacement requires `--replace-existing` and first creates a pre-restore backup. Restore disables connections and grants until reviewed again. Re-enter credentials and verify endpoints, models, and scopes. Older generations and external backups are not deleted by a project purge.

## Optional checks

Useful unit, API, security, migration, and localization tests are kept separately from the runtime image. They use synthetic inputs, an isolated temporary filesystem, and no external network or real model:

```sh
docker compose -f compose.test.yaml run --rm --build tests
```

The backend checks need no host Python/Node or additional development dependencies. Separate focused UI checks require an existing Node.js installation:

```sh
node tests/ui-files.test.mjs
node tests/ui-review-mode.test.mjs
node tests/ui-skill-import.test.mjs
```

Set `SDD_TEST_LANG=ru` to repeat the file-upload checks in Russian. The optional `tests/ui-navigation.test.cjs` also needs an installed Playwright package and Chromium/Chrome; `PLAYWRIGHT_MODULE` and `CHROME_BINARY` can point to existing installations. It launches a fresh isolated browser with a local mock API, not a live model or product. Screenshots go to a temporary directory, or to `UI_SCREENSHOT_DIR` when supplied.

These checks are not proof of model accuracy, full accessibility, or Windows compatibility.
