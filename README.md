# AMPidentifier — Web Server (BETA)

> **This is the web portal / server version of AMPidentifier.**
> It is currently in **beta** and under active development.
> For the stable command-line tool, see the [original AMPidentifier repository](https://github.com/madsondeluna/AMPIdentifier).

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![INPI](https://img.shields.io/badge/INPI-BR%2051%202025%20005859--4-green.svg)](https://www.gov.br/inpi)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)]()

---

## What is this?

This repository hosts the **Flask-based web interface** for AMPidentifier, allowing users to submit FASTA sequences and receive AMP predictions directly in a browser — no installation required.

The prediction engine is the same ensemble ML pipeline (RF, SVM, Gradient Boosting) from the CLI version.

---

## Original project

The CLI version of AMPidentifier is maintained separately at:

**[github.com/madsondeluna/AMPIdentifier](https://github.com/madsondeluna/AMPIdentifier)**

Use the CLI version if you need:
- Local execution
- Batch processing of large files
- Integration with scripts or pipelines
- External model comparison (`.pkl`)

---

## Running locally

```bash
git clone https://github.com/madsondeluna/AMPidentifierServerBETA.git
cd AMPidentifierServerBETA
pip install -r requirements.txt
python wsgi.py
```

Then open `http://localhost:5000`.

---

## Deployment

Configured for [Render.com](https://render.com) via `Procfile` and `runtime.txt`.

Build command: `pip install -r requirements.txt`
Start command: `gunicorn wsgi:app`

---

## Citation

Luna-Aragão, M. A., da Silva, R. L., Pacífico, J., Santos-Silva, C. A. & Benko-Iseppon, A. M. (2025).
AMPidentifier: A Python toolkit for predicting antimicrobial peptides using ensemble machine learning.
GitHub: https://github.com/madsondeluna/AMPIdentifier

---

## License

MIT
