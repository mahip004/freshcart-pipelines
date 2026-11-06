-- FreshCart assignment SQL patterns. Adapt table/column identifiers to the instructor notebook.
-- B3: append this expression inside ARRAY_CONSTRUCT_COMPACT in SQL_10_ORDERS_CLEAN:
IFF(UPPER(currency) NOT IN ('INR','USD'), 'unsupported_currency', NULL)

-- Dedupe: select the newest normalized copy per order; use a stable tie-breaker if timestamps tie.
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY updated_at DESC, source DESC) = 1

-- B4 idempotency pattern: hash business values and MERGE by stable order key.
-- Update only when the incoming row hash differs; insert when not matched.
-- Quarantine should MERGE by source record identity/reason, not blindly append on every run.

-- Student action: paste the instructor-provided complete SQL here only after verifying schema names.

