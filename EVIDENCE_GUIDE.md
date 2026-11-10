# Where to put your assignment screenshots

Put every screenshot in the folder for its topic. You do not need to arrange them inside a Word document yet.

## 1. GitHub

Folder: `outputs/evidence/GitHub/`

- `01-actions-pass.png` — a successful GitHub Actions run.
- `02-actions-failure.png` — the intentional failing run.
- `03-actions-fix.png` — the successful run after the fix.

## 2. Snowflake

Folder: `outputs/evidence/Snowflake/`

- `01-baseline-results.png` — first pipeline results and row counts.
- `02-validation-results.png` — data quality and quarantine results.
- `03-scd2-results.png` — customer tier change and its effect on orders/points.
- `04-future-order-check.png` — the temporary future-date test showing the problem.
- `05-final-clean-run.png` — final successful run after removing the test order.

Use more screenshots if one image cannot show the required output clearly. Hide credentials and private account details.

## 3. RabbitMQ

Folder: `outputs/evidence/RabbitMQ/`

- `01-broker-overview.png` — the RabbitMQ page showing the local broker is running.
- `02-driver-routing.png` — driver terminals showing messages received and routing keys.
- `03-malformed-message.png` — terminal showing a malformed message discarded because `zone` is missing.
- `04-dispatcher.png` — dispatcher terminal publishing messages.

Capture terminal screenshots while the scripts are running, before stopping them.

## 4. Mage

Folder: `outputs/evidence/Mage/`

- `01-pipeline-graph.png` — Mage UI showing the Iris pipeline graph.
- `02-depth-runs.png` — results for the required `max_depth` runs (use multiple images if needed).
- `03-evaluation.png` — confusion matrix and evaluation metrics.
- `04-successful-test.png` — successful pipeline/test output.

## Current state

The screenshots currently supplied have been grouped, copied into the project evidence folders, and added to the report PDF. The report lists the remaining evidence that still needs to be captured. The Snowflake login screenshot was excluded because it showed account/user details. Do not upload passwords, tokens, or an unredacted executed notebook.

