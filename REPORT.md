# Report answers and evidence checklist

**Course:** Data Engineering  
**Assignment:** From Git to Gold  
**Student:** Mahima Pandey  
**Roll number:** 23BCS155  
**Repository:** https://github.com/mahip004/freshcart-pipelines

This report uses the assignment brief and the instructor-supplied FreshCart notebooks. The FreshCart notebook in `elt/` is a sanitized copy: instructor login details and instructor run outputs were removed, and the required currency rule and sixth quality check were added. GitHub Actions now has a verified green run, an intentional red run from the temporary 30% split, and a green fix run. Snowflake, Mage and RabbitMQ still need to be run in your own course accounts. Add the required Actions screenshots and replace the remaining result prompts before submission.

## A. Git and CI/CD

### A1. Repository

The public repository is live at `https://github.com/mahip004/freshcart-pipelines`. It has separate commits for the project overview, CI, Mage blocks, FreshCart notebook, stream scripts, and report. `git log --oneline` output at report preparation time:

```text
93ed60e Restore the 80/20 split after the failing CI demonstration
adbcea7 Demonstrate failing CI with a 30 percent test split
a5658bd Fix pytest module import path in CI
113419e Document remaining account-run evidence
dd3952f Add numbered assignment answers and evidence checklist
a0c4256 Add Mage pipeline metadata at the CLI pipeline path
6f87031 Place the exporter in Mage's data_exporters directory
dfdfc4a Place the loader in Mage's data_loaders directory
1c6319e Add topic-matched drivers with ACK and NACK handling
037fb86 Add the topic exchange order dispatcher
b862ff4 Document the RabbitMQ run procedure and ACK behavior
1daf67a Add the sanitized FreshCart notebook with validation checks
00a605e Add FreshCart SQL validation and idempotency patterns
5fdd327 Add the Iris pipeline inspection notebook
f3be08c Wire the Mage pipeline and evaluation branch
9c279cd Add the predictions exporter block
4edec14 Add the evaluation branch with metrics
1a25367 Add the tested decision tree block
abc6c5a Add the reproducible train-test split block
b23b6cc Add the dataset validation block
fc0e2f3 Add the Iris data loader block
55a46ae Initialize Mage exporter package
da5c5bf Initialize Mage transformer package
c2e6e72 Initialize Mage loader package
8a774cf Initialize the Iris project package
518e96d Run pytest on pushes and pull requests
b1a949a Add the Iris split regression test
dd495df Declare Python project dependencies
e7fa66d Ignore secrets and generated artifacts
c230113 Add project overview and setup instructions
```

### A2. Git command table

| Command | Where the change happens | What exactly happens |
|---|---|---|
| `git init` | Working folder and local Git metadata | Creates a `.git` repository so Git can track this folder. |
| `git add train.py` | Staging area | Stages the current file contents for the next commit. |
| `git commit -m "msg"` | Local repository | Saves a snapshot of staged changes as a local commit. |
| `git remote add origin URL` | Local Git configuration | Records the remote URL under the name `origin`. |
| `git push -u origin main` | Remote Git | Uploads local `main` commits and sets upstream tracking. |
| `git pull origin main` | Local working folder and local Git | Fetches remote commits and integrates them into the current branch. |

After `git commit`, a teammate cannot see the code on GitHub yet: the commit exists only in the local repository until pushed to a remote.

### A3. CI

`tests/test_prepare_data.py` checks the required 120/30 split and the workflow runs pytest on pushes and pull requests using Python 3.12. The green run passed after the import-path fix: [Actions run](https://github.com/mahip004/freshcart-pipelines/actions/runs/42240057166). The temporary `test_size=0.3` commit failed as expected with 105 training rows instead of 120: [intentional failing run](https://github.com/mahip004/freshcart-pipelines/actions/runs/42240222845). Restoring `0.2` passed: [fix run](https://github.com/mahip004/freshcart-pipelines/actions/runs/42240377107). **Still add screenshots** of the red and green run pages to the appendix.

## B. FreshCart ELT on Snowflake

The instructor notebook supplies the DDL, mock API fixtures and transformations. The expected values below are acceptance targets from the assignment/course material; they are not a claim that your Snowflake run occurred.

### B1. Baseline

| Check | Expected result from brief | Actual run |
|---|---:|---|
| Bronze raw orders | 8 | [run notebook and paste] |
| Silver clean | 6 | [paste] |
| Quarantine | 2: ORD-1004, ORD-1006 | [paste] |
| Deduplicated orders | 4 | [paste] |
| Gold aggregate | 4 orders; ₹7,785.00; 126 points | [paste] |
| Rejected share | 25% | [paste] |

**Evidence:** append screenshots of notebook cells and Snowflake output.

### B2. Record trace

ORD-1003's website bronze JSON uses flat keys such as `order_id`, `cust_email`, `cust_name`, `order_date`, `amount`, and `updated_at`; the mobile bronze JSON uses `orderId`, nested `customer.email` and `customer.name`, `orderDate`, nested `total.value` and `total.currency`, `deliveryPin`, and `updatedAt`. `SQL_10_ORDERS_CLEAN` maps these with `raw:order_id::STRING` etc. for web and `raw:orderId::STRING`, `raw:customer.email::STRING`, `raw:total.value::STRING` etc. for mobile. Both become normalized `order_id`, `email`, `name`, `order_date`, `amount`, `currency`, `pincode`, and `updated_at`; `LOWER(TRIM(...))`, `INITCAP`, `COALESCE(TRY_TO_DATE(...))`, and `TRY_TO_DECIMAL(REGEXP_REPLACE(...))` standardize them. `SQL_20_ORDERS_DEDUP` keeps the later mobile row using `QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY updated_at DESC, ingest_seq DESC) = 1`. Meera's order is INR 2,100, so the FX rate is 1; Platinum's multiplier is 3, giving `FLOOR(2100 / 100) × 3 = 21 × 3 = 63` points.

ORD-1005's date is 2026-09-03, when Priya's SCD2 tier becomes Gold. The order-date range join to `dim.customers_scd2` selects Gold, then `ref.tier_multiplier` joins on `m.tier = c.tier`; points are `FLOOR(899 / 100) × 2 = 8 × 2 = 16`. ORD-1001 is dated 2026-09-01, so the same point-in-time SCD2 join selects Silver, yielding `FLOOR(1250 / 100) × 1 = 12` points.

### B3. Currency validation

The submitted notebook adds `IFF(currency NOT IN ('INR', 'USD'), 'unsupported_currency', NULL)` to `ARRAY_CONSTRUCT_COMPACT(...)` in `SQL_10_ORDERS_CLEAN`. In the supplied mock data, ORD-1006 already has `bad_email` and `bad_pincode`; with the rule it also has `unsupported_currency` because its normalized currency is EUR. Its gold contribution remains zero because it was already excluded from `silver.orders_clean` and quarantined. The quarantine `INSERT` prevents another copy with the same source, null-safe order ID, and `updated_at` through its `NOT EXISTS` clause; a `QUALIFY ROW_NUMBER()` also retains one latest copy per source/order/version. Capture the reasons array before and after by commenting out the added rule for the first run, then restoring it and rerunning.

### B4. SCD2 and idempotency

**Prediction written before run:** CUST-02 currently has one Silver version from 2024-01-15. Adding Gold effective 2026-08-15 yields two SCD2 rows, with Silver ending 2026-08-14. ORD-1002 is dated 2026-09-01, so its tier becomes Gold. Its INR value is `42.50 × 83.20 = ₹3,536`; points rise from `FLOOR(3536/100) × 1 = 35` Silver points to `FLOOR(3536/100) × 2 = 70` Gold points. The expected total rises from 126 to 161 points, and one gold row (ORD-1002) should receive a changed `published_at` because its row hash changes. Record this prediction before running, then fill the actual column from Snowflake.

| Quantity | Prediction | Actual after run |
|---|---|---|
| CUST-02 rows in `dim.customers_scd2` | 2; Silver version closes 2026-08-14 | [measure] |
| Tier used for ORD-1002 | Gold | [measure] |
| ORD-1002 points | 70 (₹3,536 / 100 rounded down × Gold multiplier 2) | [measure] |
| Total gold points | 161 (126 + 35) | [measure] |
| Gold rows with changed `published_at` | 1: ORD-1002 | [measure] |

`row_hash` gives each output row a fingerprint of relevant business values. The `MERGE` matches on a stable business key and updates a target only when the source hash differs, while inserting previously unseen keys. This prevents a rerun from duplicating unchanged gold facts and lets `published_at` remain stable when content is unchanged. Bronze still grows by eight rows per run because extraction appends a fresh copy of the raw API sample unless the landing/load step itself deduplicates it.

### B5. Quality check and ELT

The notebook adds a sixth check for future orders: `SELECT COUNT_IF(order_date > CURRENT_DATE()) FROM silver.orders_dedup`; it should return 0. Add a temporary otherwise-valid mock web order dated 2099-01-01, rerun the pipeline and capture `PROBLEM`, then remove the mock and rerun to confirm 0. **Evidence:** include both outputs. ELT fits FreshCart because raw data can be loaded quickly into Snowflake and transformed there with SQL, keeping the original landing data available for reprocessing. Snowflake's warehouse can scale the transformations where the data already sits. ETL would win when transformations must happen before loading, such as when policy forbids transferring raw sensitive fields into the destination.

## C. Mage Iris pipeline

### C1. Graph and run

Graph: `load_iris (data_loader) → validate_iris (transformer) → prepare_data (transformer) → train_model (transformer) → {save_results (data_exporter), evaluate_model (transformer)}`. Each block includes an attached `@test`. The project's metadata and importable blocks are included. **Run evidence required:** use Mage's CLI `mage run iris_project iris_classifier --test` in the configured Mage environment and append its output; The Mage Iris class materials and runtime were not supplied here.

### C2. Test gate

The `train_model` test enforces accuracy >= 0.85. A failing block test marks the block run as failed, so downstream exporters are not scheduled from that failed output; `save_results` therefore does not write a prediction file. This gate prevents invalid artifacts from being mistaken for valid outputs and avoids having to detect and remove a bad file later.

| max_depth | Test accuracy | Test passed? | CSV created? |
|---:|---:|---|---|
| 1 | [run in Mage] | [measure] | [observe after deleting before run] |
| 2 | [run in Mage] | [measure] | [observe] |
| 3 | [run in Mage] | [measure] | [observe] |
| 4 | [run in Mage] | [measure] | [observe] |
| 5 | [run in Mage] | [measure] | [observe] |

Before each run delete `iris_predictions.csv`. Save the Mage run output and file state; do not substitute local expectations for the requested Mage evidence.

### C3. Evaluation branch

`metadata.yaml` includes the branch from `train_model` to `save_results` and `evaluate_model`. The block returns a confusion matrix and a classification metrics table. **Evidence required:** run the project in Mage, include the actual confusion matrix/metrics, and capture the Cloudflare-tunnel Mage UI graph. Mage Iris class materials and a live tunnel were not supplied.

### C4. Own block

`validate_iris` checks for no missing values and exactly three classes, with its own `@test`; it sits after `load_iris`. Commit it and verify CI remains green.

## D. Food-order stream

### D1. Topic routing

| # | Routing key | Receiving queues |
|---:|---|---|
| 1 | `bangalore.koramangala.food` | Ravi, Meena, Control |
| 2 | `bangalore.indiranagar.ride` | Priya, Arjun, Control |
| 3 | `bangalore.whitefield.ride` | Arjun, Control |
| 4 | `chennai.tnagar.food` | Karthik |
| 5 | `chennai.whitefield.ride` | dropped |
| 6 | `bangalore.koramangala` | Control only |

For key 6, `#` in `bangalore.#` matches zero or more words, so Control receives it. The driver patterns containing `*` require exactly one word after the zone or city and all city.zone.type patterns have three words; none can match the two-word key.

### D2. Build and run

`stream/dispatcher.py` publishes JSON every two seconds to the durable `rapido-dispatch` topic exchange. `stream/driver.py NAME PATTERN` creates a private exclusive queue, binds the topic, prints deliveries and ACKs valid messages. **Evidence required:** run at least three drivers and dispatcher for two minutes against your broker, then include console output showing a D1 route match. A broker was not available here.

### D3. ACK/NACK

A message without `zone` is rejected with `basic_nack(requeue=False)`; valid messages are ACKed. The dispatcher emits one malformed message every ten. If a driver crashes before ACK, the broker can redeliver the unacknowledged message after the connection closes. With `requeue=True`, a permanently malformed message may circulate continuously; reject without requeue or route it to a dead-letter queue.

## E. Integration and reflection

```text
Git working tree → commits → GitHub remote → Actions CI
                                  │
                                  ├── tests Mage blocks before saving model output
                                  ├── FreshCart raw API → bronze → silver/quarantine → gold in Snowflake
                                  └── RabbitMQ topic stream → driver queues → (bonus) landing → ELT → gold
```

The four pieces form one delivery path: Git records pipeline code, CI checks changes, FreshCart transforms batch order data into gold tables, Mage trains and evaluates a tested classifier, and RabbitMQ routes live order events by topic. The optional landing consumer would connect events to the same warehouse flow after the batch logic is adapted.

**Reflection (complete after real runs):** [Describe one actual failure, the evidence you used to locate its cause, and the code/configuration change that fixed it. Do not invent a failure story.]

## Bonus stream-to-lakehouse

Not implemented as a live end-to-end integration because the FreshCart notebook has not been run in the student's Snowflake account and a RabbitMQ broker is not connected. The consumer must batch one minute of RabbitMQ messages, write a landing file, load it, and reuse the same idempotent transform/MERGE; demonstrate equal gold totals after the second identical batch.

## Final evidence checklist

- [x] Add Mahima Pandey, roll number 23BCS155, and the GitHub repository URL to the cover.
- [x] Publish the repo with separate meaningful commits and include `git log --oneline`.
- [ ] Add GitHub green/red/fix screenshots.
- [ ] Run FreshCart baseline, validation, SCD2 and quality check in Snowflake; add outputs/screenshots.
- [ ] Run Mage matrix and evaluation branch; add actual metrics and UI screenshot.
- [ ] Run RabbitMQ for two minutes and include routing plus ACK/NACK evidence.
- [ ] Complete reflection from an actual failure.
- [ ] If claiming bonus, implement and rerun the stream-to-lakehouse consumer twice.

