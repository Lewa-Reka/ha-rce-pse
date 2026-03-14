# AGENTS.md

## Project overview

This repository is a **Home Assistant custom integration** for monitoring Polish electricity market prices (RCE – Rynkowa Cena Energii) from PSE (Polskie Sieci Elektroenergetyczne). Data is provided at 15-minute resolution; the integration polls the official PSE API every 30 minutes.

- Integration code: `custom_components/rce_pse/`
- Domain: `rce_pse`

## Setup and test commands

- Install test dependencies: `pip install -r requirements-test.txt`
- Run tests: `pytest tests/ -v`

CI runs HACS validation, hassfest, and MegaLinter (see `.github/workflows/validation.yml` and `.github/workflows/mega-linter.yml`). Dependabot (`.github/dependabot.yml`) opens PRs for pip and GitHub Actions updates. Agents may run these locally if needed; full setup is in the workflow files. To run MegaLinter locally: `npx mega-linter-runner --flavor python` (requires Node.js) or use the MegaLinter Docker image.

## Code style and conventions

- **No comments in code.** Code must be self-explanatory (clear names, structure).
- **All code in English** unless the user specifies otherwise.
- **Python only.** This is a Home Assistant custom integration.

## Testing

- Tests live in `tests/`. Shared fixtures (e.g. `sample_api_response`, `coordinator_data`, `mock_coordinator`) are in `tests/conftest.py`.
- **Add tests for every new feature.** Place them in the appropriate `tests/test_*.py` module.
- **When removing a feature, remove the tests that cover it.**
- Before finishing a task, run `pytest tests/ -v` and ensure all tests pass.

## Translations

- Translation files: `custom_components/rce_pse/translations/en.json` (English) and `custom_components/rce_pse/translations/pl.json` (Polish).
- For any change that affects UI, config flow, or entity names (new or changed keys under `config`, `options`, `entity.sensor`, or `entity.binary_sensor`), update **both** `en.json` and `pl.json` and keep the key structure identical.

### Removing or renaming entities

When removing or renaming an entity, update both translation files: remove or rename the corresponding keys under `entity.sensor` or `entity.binary_sensor` in `en.json` and `pl.json` so there are no orphaned entries.

## Documentation

When you change behavior or features described in `README.md` (installation, configuration, sensors, or general behavior), update `README.md` accordingly.

## Key paths

- Integration package: `custom_components/rce_pse/` (coordinator, config_flow, sensors, binary_sensors, shared_base, const, price_calculator).
- Domain and constants: `custom_components/rce_pse/const.py`.
- Entity names use `_attr_translation_key` set in `custom_components/rce_pse/shared_base.py`; each key must exist in both `translations/en.json` and `translations/pl.json` under `entity.sensor` or `entity.binary_sensor`.

## Validation (optional)

CI runs:

- **HACS:** `hacs/action` with category `integration`.
- **Hassfest:** `home-assistant/actions/hassfest@master`.
- **MegaLinter:** `oxsecurity/megalinter/flavors/python@v8` (Python, JSON, YAML, Markdown, GitHub Actions); config in `.mega-linter.yml`. For Python: Ruff (lint + format), Bandit (security), Mypy (type checking).
- **Dependabot:** weekly PRs for pip and GitHub Actions (`.github/dependabot.yml`).

See `.github/workflows/validation.yml` and `.github/workflows/mega-linter.yml` for the exact steps.
