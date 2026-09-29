# Controlled splits

These partition the 123,304 deduplicated pairs. pandas 1.4.0 and NumPy 1.23.5 use `df.sample(frac=1.0, random_state=42).reset_index(drop=True)`.

| File | Pairs |
| --- | ---: |
| train.csv | 98,643 |
| validation.csv | 12,330 |
| test.csv | 12,331 |

Training takes the first `int(n * 0.8)` rows, validation the next `int(n * 0.1)`, and test the remainder. Columns match the corpus. The script verifies zero exact-pair intersections and complete coverage. Individual codes, translations, source documents or semantically related pairs may overlap; those forms of overlap are not tested. See ../DATA_NOTICE.md for rights.
