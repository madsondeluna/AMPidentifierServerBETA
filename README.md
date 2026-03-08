# AMPidentifier Web Server (BETA)

> **This is the web portal / server version of AMPidentifier.**
> It is currently in **beta** and under active development.
> For the stable command-line tool, see the [original AMPidentifier repository](https://github.com/madsondeluna/AMPIdentifier).

[![Live](https://img.shields.io/badge/live-ampidentifierserver.onrender.com-success)](https://ampidentifierserver.onrender.com)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![INPI](https://img.shields.io/badge/INPI-BR%2051%202025%20005859--4-green.svg)](https://www.gov.br/inpi)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)]()

![AMPidentifier workflow](img/workflow.png)

## Live application

**[https://ampidentifierserver.onrender.com](https://ampidentifierserver.onrender.com)**

> **Note on availability:** To conserve computational resources, the server enters a sleep state after 15 minutes of inactivity. When a new request is made, it automatically wakes up and redeploys, typically becoming fully functional within **1 to 2 minutes**. No manual action is required.

## What is this?

This repository hosts the **Flask-based web interface** for AMPidentifier, allowing users to submit FASTA sequences and receive AMP predictions directly in a browser, with no installation required.

The prediction engine is the same ensemble ML pipeline (RF + SVM + Gradient Boosting) from the CLI version, running on a cloud server.

## Features

| Feature | Description |
|---|---|
| **Sequence input** | Paste one or multiple sequences in FASTA format directly into the browser |
| **File upload** | Upload a `.fasta` file directly, no copy-paste needed |
| **Sequence counter** | Real-time count of sequences detected as the user types |
| **FASTA validation** | Format is validated before submission, with informative error messages |
| **Model selection** | Choose between Ensemble (RF + SVM + GB), Random Forest, SVM, or Gradient Boosting |
| **AMP / non-AMP classification** | Each sequence is classified as antimicrobial peptide or non-AMP |
| **Probability score** | Predicted probability displayed with a visual color-coded bar |
| **Results filter** | Filter the results table by All, AMP only, or non-AMP only |
| **CSV download** | Export results as a `.csv` file with one click |
| **Copy table** | Copy results to clipboard as tab-separated values |
| **Load example** | Pre-loads 6 curated sequences for quick testing |
| **Server status** | Live indicator (green/red dot) showing whether the server is online |

## How to use

1. Open **[https://ampidentifierserver.onrender.com](https://ampidentifierserver.onrender.com)**
2. Paste sequences in **FASTA format** into the text area, upload a `.fasta` file, or click **load example**
3. Select a **model** from the dropdown (Ensemble is recommended)
4. Click **Run**
5. View the results table with classification (**AMP** or **non-AMP**), probability score, and visual bar
6. Use the **filter buttons** to show only AMP or non-AMP predictions
7. Click **download CSV** to export, or **copy table** to copy results to the clipboard

### FASTA format example

```
>SequenceID|Protein_name|Organism|Description
AMINOACIDSEQUENCE
```

## Interpretation note and known limitations

Predictions are computed from **physicochemical and compositional descriptors** derived from the primary amino acid sequence. For higher predictive power, use **Ensemble mode (RF + SVM + GB)**, which combines three independent classifiers by majority vote and achieves:

| Metric | Value |
|---|---|
| **Accuracy** | 87.47% |
| **Sensitivity** | 85.96% |
| **Specificity** | 88.98% |

> Bear in mind that proteins whose primary function is not antimicrobial activity may still harbour potential antimicrobial features in specific sequence regions.

### Special cases and possible errors

| Case | Expected behavior |
|---|---|
| Very short sequences (< 5 residues) | Rejected at input validation — FASTA must contain at least 5 amino acids per sequence |
| Non-standard amino acid characters | Sequences with characters outside the standard 20-letter code may trigger a validation error or produce unreliable predictions |
| Long proteins (> ~50 residues) | Descriptors are computed over the full sequence; AMP features concentrated in sub-regions may be diluted, leading to false negatives |
| Highly disordered or repetitive sequences | May yield extreme probability scores that do not reflect true antimicrobial potential |
| Multimeric or chimeric constructs | Not supported; each FASTA entry is treated as a standalone peptide/protein |
| Batch size | No hard limit is enforced, but very large batches may cause the server to time out; use the [CLI version](https://github.com/madsondeluna/AMPIdentifier) for large-scale runs |

## Original CLI project

The command-line version of AMPidentifier is maintained separately at:

**[github.com/madsondeluna/AMPIdentifier](https://github.com/madsondeluna/AMPIdentifier)**

Use the CLI version if you need:
- Local execution with no internet dependency
- Batch processing of large files
- Custom model comparison (external `.pkl` files)
- Full parameter control and pipeline integration

## Technology stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, Flask 3.0 |
| **ML models** | scikit-learn (Random Forest, SVM, Gradient Boosting) |
| **Feature extraction** | modlAMP, physicochemical descriptors |
| **Sequence parsing** | Biopython |
| **Data handling** | pandas, numpy |
| **Web server** | Gunicorn |
| **Hosting** | Render.com |

## Running locally

```bash
git clone https://github.com/madsondeluna/AMPidentifierServerBETA.git
cd AMPidentifierServerBETA
pip install -r requirements.txt
python wsgi.py
```

Then open `http://localhost:5000`.

## Issues and feedback

Found a bug or have a suggestion? Open an issue at:
**[github.com/madsondeluna/AMPidentifierServerBETA/issues](https://github.com/madsondeluna/AMPidentifierServerBETA/issues)**

Developer: [madsondeluna@gmail.com](mailto:madsondeluna@gmail.com)

## Ownership

This application is a property of the **Universidade Federal de Pernambuco (UFPE)** and the **Laboratório de Genética e Biotecnologia Vegetal (LGBV)**.

## Citation

Luna-Aragão, M. A., da Silva, R. L., Pacífico, J., Santos-Silva, C. A. & Benko-Iseppon, A. M. (2025).
AMPidentifier: A Python toolkit for predicting antimicrobial peptides using ensemble machine learning and physicochemical descriptors.
GitHub repository. https://github.com/madsondeluna/AMPIdentifier

## License

This software is protected under Brazilian intellectual property law with registration at the **Instituto Nacional da Propriedade Industrial (INPI)**, registration no. **BR 51 2025 005859-4**.

Unauthorized reproduction, distribution, or commercial use without explicit permission from the authors is prohibited.
