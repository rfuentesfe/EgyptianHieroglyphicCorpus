## MAAT prototype

This repository will also provide the MAAT local execution package associated with the submitted manuscript.

MAAT is intended to be executed locally using Docker, allowing reviewers and researchers to run the prototype on their own computers without relying on an external server.

The full dataset, trained models, and local execution package will be made publicly available upon acceptance of the manuscript.

See:

```text
maat/README.md

# Egyptian Hieroglyphic Corpus and MAAT

This repository contains the Egyptian Hieroglyphic Corpus and the MAAT prototype associated with the submitted manuscript.

The repository is currently provided for review purposes. The dataset, trained models, and full local execution package will be made publicly available upon acceptance of the manuscript.

## MAAT local execution

MAAT is designed to be executed locally using Docker.

```bash
git clone https://github.com/rfuentesfe/EgyptianHieroglyphicCorpus.git
cd EgyptianHieroglyphicCorpus
docker compose up --build
