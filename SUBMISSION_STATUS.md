# Submission status

Student: Mahima Pandey (23BCS155)

Repository: https://github.com/mahip004/freshcart-pipelines

## Prepared

- GitHub Actions red failure and green fix run recorded, with a commit/check summary screenshot.
- Snowflake baseline results recorded: 6 silver rows, 2 quarantined rows, 4 deduplicated/gold orders, INR 7,785.00 revenue, 126 points, and 25% rejected share.
- Snowflake and RabbitMQ were run in the student's own environments; the report includes the available run screenshots.
- Instructor credentials and run outputs remain removed from the sanitized notebook.
- The report includes the SCD2, future-order quality check, topic routing, ACK/NACK explanations, and supplied Mage run evidence (CLI, depth results, evaluation metrics, and graph).

## Remaining repository alignment

The supplied Mage evidence shows a `train_model` accuracy gate of 0.9 and a `save_metrics` exporter. The packaged repository currently has a 0.85 gate and does not include that exporter; align the code and pipeline metadata before claiming the repository reproduces that exact run.

The full report is `REPORT.md`; the PDF is in `report/23BCS155_Mahima_Pandey_Pipelines.pdf`. Never commit secrets or the excluded Snowflake login screenshot.
