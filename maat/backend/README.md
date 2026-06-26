# MAAT Local Execution Package

MAAT is the local execution prototype associated with the Egyptian Hieroglyphic Corpus and the submitted manuscript.

The system is designed to run locally on the user's computer using Docker. It includes a frontend interface, a FastAPI backend, and the components required for hieroglyphic image processing, sign recognition, and translation.

## Current status

This repository is currently prepared for review purposes. The full MAAT package, trained models, and dataset will be made publicly available upon acceptance of the manuscript.

## Planned local execution

```bash
git clone https://github.com/rfuentesfe/EgyptianHieroglyphicCorpus.git
cd EgyptianHieroglyphicCorpus
docker compose up --build
