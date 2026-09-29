# Egyptian Hieroglyphic Corpus

Public corpus repository associated with the article accepted in *Applied Soft Computing*:

**A modular image-to-translation framework for Egyptian hieroglyphic images**

Raúl Fuentes-Ferrer, Jaime Duque-Domingo, Pedro Javier Herrera (2026).

This repository provides the Gardiner-code/English parallel corpus and reproducible preparation of controlled data splits. It does not include trained models or a complete reproduction of all article experiments. MAAT is not part of this public article repository.

## Corpus

CSV columns are `Gardiner Code` (a linear sequence of Gardiner sign codes) and `Translation English` (the corresponding English text). This representation is not a complete two-dimensional Manuel de Codage (MdC) encoding.

| Artifact | Pairs |
| --- | ---: |
| Normalized non-empty corpus | 123,624 |
| Deduplicated corpus | 123,304 |
| Train | 98,643 |
| Validation | 12,330 |
| Test | 12,331 |

The source has 123,658 records. Both fields use `" ".join(str(x).strip().split())`, with pandas missing values converted to empty strings. The 34 incomplete records are omitted. The full normalized corpus retains exact duplicates, representing the pipeline corpus after omission of incomplete records. Deduplication keeps the first occurrence of each exact pair: 312 duplicate groups contain 632 rows, and 320 repeated copies are removed.

Controlled splits use the deduplicated corpus with `df.sample(frac=1.0, random_state=42).reset_index(drop=True)`. Training takes the first `int(n * 0.8)` rows, validation the next `int(n * 0.1)`, and test the remainder. Exact Gardiner/English pairs do not overlap across splits. This does not establish separation by individual column, original document, or semantic similarity.

## Provenance

The corpus was manually constructed, reviewed, normalized and adapted for this research. The published Gardiner-code/English pairs were manually curated and adapted rather than automatically copied from reference resources.

Reference materials included Schweitzer, S. D. (2019), *AED – Ancient Egyptian Dictionary Version 1.0* (Zenodo); Erman, A., & Grapow, H. (1926–1963), *Wörterbuch der ägyptischen Sprache*; Gardiner's *Egyptian Grammar* and dictionary resources; and the authors' own notes and manual work on hieroglyphic stelae. The preparation script processes the resulting manually prepared source corpus. See [DATA_NOTICE.md](DATA_NOTICE.md) for the corpus-level provenance statement and the distinction between software and data.

## Reproduce

Reference environment: Python 3.8.10, pandas 1.4.0, NumPy 1.23.5. Install the pinned dependencies in an isolated environment:

```powershell
python -m pip install -r requirements.txt
python scripts/prepare_public_corpus.py --source "C:/EgyptianHieroglyphicCorpus/training/translator/data/input/tu_corpus_100k.csv"
python scripts/prepare_public_corpus.py --source "C:/EgyptianHieroglyphicCorpus/training/translator/data/input/tu_corpus_100k.csv" --check
```

Pass your original source location with `--source`. The source is read only and is not bundled here. Its required SHA-256 is:

```text
da9079e3c2e2dcd09392c982875f3f071171908705391652c031817017fa6cdb
```

The script validates the hash before parsing, enforces all counts, checks exact-pair separation and coverage, and generates the five CSVs, audit JSON and SHA-256 manifest. It aborts on mismatches. `--check` rebuilds in memory and compares all generated files without writing; `--output-dir` selects another destination. CSVs use UTF-8 and LF. The audit records the Python version; byte-for-byte audit/manifest reproduction requires the same Python version.

See [data](data/README.md), [splits](splits/README.md), and [results](results/README.md).

## Citation and rights

Use [CITATION.cff](CITATION.cff). The article is accepted; no definitive DOI, volume or pages are asserted.

[MIT](LICENSE) covers original scripts and software only, not the corpus or its splits. The separate [data notice](DATA_NOTICE.md) records corpus authorship and provenance. Cited third-party works remain the property of their respective rights holders.
