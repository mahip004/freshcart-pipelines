# FreshCart Pipelines

Course project for **From Git to Gold**. The repo contains a sanitized FreshCart notebook based on the instructor's supplied course material, an Iris Mage-style pipeline scaffold, RabbitMQ stream scripts, and report answers/evidence checklist. The notebook uses prompts for your own Snowflake login; course credentials and instructor run outputs were removed.

## Local setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

Never commit `.env`, Snowflake credentials, broker URLs, or generated CSV/PKL outputs. Keep account secrets in Colab Secrets or local environment variables.

## Contents

- `tests/test_prepare_data.py`, `.github/workflows/ci.yml`: A3 CI test/workflow.
- `iris_project/`: importable Iris blocks with Mage decorator fallbacks, metadata and evaluation branch.
- `stream/`: RabbitMQ dispatcher/driver and run instructions.
- `elt/freshcart_elt.ipynb`: supplied course flow, with instructor credentials and outputs removed; includes the B3 currency rule and B5 quality check.
- `REPORT.md`: numbered assignment answers, captured non-Mage results, evidence appendix, and explicit remaining evidence checklist.
- `report/23BCS155_Mahima_Pandey_Pipelines.pdf`: current report PDF; Mage and some Snowflake/RabbitMQ scenario evidence remain pending.

## GitHub Actions

The repository is `https://github.com/mahip004/freshcart-pipelines`. Its Actions workflow runs pytest on pushes and pull requests using Python 3.12. Run links and the available check-summary screenshot are recorded in `REPORT.md`.

## Snowflake

Open `elt/freshcart_elt.ipynb` in Colab, enter your own credentials when prompted, and run the cells in order. Use screenshots and results from your own account in the submission.

## RabbitMQ

Set `RABBITMQ_URL` locally if using a hosted broker; leave it blank for localhost. Run three drivers in separate terminals and the dispatcher in another for the required two-minute observation. See `stream/README.md`.

