# Audit and integrity

`corpus_audit.json` records source SHA-256, normalization and split rules, runtime versions, counts, exact-pair intersections, and sizes and hashes for all five CSVs.

`SHA256SUMS.txt` hashes those five CSVs and the audit JSON, using repository-relative paths. It excludes itself to avoid self-reference, and excludes handwritten documentation and scripts. No timestamps or local absolute paths are recorded. Python version is recorded, so audit bytes depend on it.

Run the preparation script with `--check` to reconstruct in memory and verify every generated artifact without writing. These checks establish integrity, not rights clearance or model results.
