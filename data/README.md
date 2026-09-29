# Parallel corpus

Both UTF-8 CSVs contain `Gardiner Code` and `Translation English`. Codes are linear sequences, not full two-dimensional MdC.

- `gardiner_english_corpus.csv`: 123,624 normalized non-empty pairs in source order, retaining exact duplicates.
- `gardiner_english_corpus_deduplicated.csv`: 123,304 unique exact pairs, keeping the first occurrence in source order.

Whitespace is collapsed in both fields; 34 incomplete records are excluded. The external source remains unmodified. See the root README for regeneration and DATA_NOTICE.md for rights.
