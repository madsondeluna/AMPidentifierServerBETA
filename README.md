# AMPidentifier — Web Server (BETA)

> **This is the web portal / server version of AMPidentifier.**
> It is currently in **beta** and under active development.
> For the stable command-line tool, see the [original AMPidentifier repository](https://github.com/madsondeluna/AMPIdentifier).

[![Live](https://img.shields.io/badge/live-ampidentifierserver.onrender.com-success)](https://ampidentifierserver.onrender.com)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![INPI](https://img.shields.io/badge/INPI-BR%2051%202025%20005859--4-green.svg)](https://www.gov.br/inpi)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)]()

---

## Live application

**[https://ampidentifierserver.onrender.com](https://ampidentifierserver.onrender.com)**

> **Note on availability:** To conserve computational resources, the server enters a sleep state after 15 minutes of inactivity. When a new request is made, it automatically wakes up and redeploys — typically becoming fully functional within **1–2 minutes**. No manual action is required.

---

## What is this?

This repository hosts the **Flask-based web interface** for AMPidentifier, allowing users to submit FASTA sequences and receive AMP predictions directly in a browser — no installation required.

The prediction engine is the same ensemble ML pipeline (RF + SVM + Gradient Boosting) from the CLI version, running on a cloud server.

---

## Features

| Feature | Description |
|---|---|
| **Sequence input** | Paste one or multiple sequences in FASTA format directly into the browser |
| **Model selection** | Choose between Ensemble (RF + SVM + GB), Random Forest, SVM, or Gradient Boosting individually |
| **AMP / non-AMP classification** | Each sequence is classified as antimicrobial peptide or non-AMP |
| **Probability score** | Displays the predicted probability of each sequence being an AMP |
| **Results table** | Interactive table with ID, sequence, classification, and probability |
| **CSV download** | Export results as a `.csv` file with one click |
| **Load example** | Pre-loads 10 curated sequences (5 known AMPs + 5 non-AMPs) for quick testing |

---

## How to use

1. Open **[https://ampidentifierserver.onrender.com](https://ampidentifierserver.onrender.com)**
2. Paste your sequences in **FASTA format** into the text area, or click **load example** to use the built-in dataset
3. Select a **model** from the dropdown (Ensemble is recommended)
4. Click **Run**
5. View the results table — each sequence will show its classification (**AMP** or **non-AMP**) and probability score
6. Click **download CSV** to export the results

### FASTA format example

```
>SequenceID|Protein_name|Organism|Description
AMINOACIDSEQUENCE
```

---

## Original CLI project

The command-line version of AMPidentifier is maintained separately at:

**[github.com/madsondeluna/AMPIdentifier](https://github.com/madsondeluna/AMPIdentifier)**

Use the CLI version if you need:
- Local execution with no internet dependency
- Batch processing of large files
- Custom model comparison (external `.pkl` files)
- Full parameter control and pipeline integration

---

## Technology stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, Flask 3.0 |
| **ML models** | scikit-learn (Random Forest, SVM, Gradient Boosting) |
| **Feature extraction** | modlAMP — physicochemical descriptors |
| **Sequence parsing** | Biopython |
| **Data handling** | pandas, numpy |
| **Web server** | Gunicorn |
| **Hosting** | Render.com |

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

## Issues and feedback

Found a bug or have a suggestion? Open an issue at:
**[github.com/madsondeluna/AMPidentifierServerBETA/issues](https://github.com/madsondeluna/AMPidentifierServerBETA/issues)**

Developer: [madsondeluna@gmail.com](mailto:madsondeluna@gmail.com)

---

## Ownership

This application is a property of the **Universidade Federal de Pernambuco (UFPE)** and the **Laboratory of Plant Genetics and Biotechnology (LGBV)**.

---

## Citation

Luna-Aragão, M. A., da Silva, R. L., Pacífico, J., Santos-Silva, C. A. & Benko‑Iseppon, A. M. (2025).
AMPidentifier: A Python toolkit for predicting antimicrobial peptides using ensemble machine learning and physicochemical descriptors.
GitHub repository. https://github.com/madsondeluna/AMPIdentifier

---

## License

MIT
