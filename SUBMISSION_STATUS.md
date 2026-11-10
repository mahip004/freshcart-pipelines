# Submission status

Student: Mahima Pandey (23BCS155)

Repository: https://github.com/mahip004/freshcart-pipelines

## Prepared

- GitHub Actions red failure and green fix run recorded, with a commit/check summary screenshot.
- Snowflake baseline results recorded: 6 silver rows, 2 quarantined rows, 4 deduplicated/gold orders, INR 7,785.00 revenue, 126 points, and 25% rejected share.
- RabbitMQ broker, dispatcher publishing, and management UI activity captured.
- Instructor credentials and run outputs remain removed from the sanitized notebook.
- The report PDF includes the available screenshots and labels all unmeasured results honestly.

## Still needed before a fully evidenced submission

- Mage runs, metrics, and UI evidence (intentionally left pending for now).
- Snowflake currency-rule before/after reason arrays, SCD2 post-change measurements, and the future-order injection plus clean rerun.
- RabbitMQ driver console output proving a concrete route match and malformed-message discard/NACK.
- Optional but recommended: separate GitHub Actions screenshots showing the failing run details and corrected passing run details.

The full report is `REPORT.md`; the PDF is in `report/23BCS155_Mahima_Pandey_Pipelines.pdf`. Never commit secrets or the excluded Snowflake login screenshot.

