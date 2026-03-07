"""
AMPidentifier Web Portal — minimal single-page app
"""
import os
import sys
import tempfile
from datetime import datetime

from flask import Flask, request, jsonify, render_template_string, send_file
import pandas as pd
import io

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from amp_identifier.core import run_prediction_pipeline
from amp_identifier.data_io import load_fasta_sequences

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AMPidentifier</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Courier New', monospace; background: #0f0f0f; color: #e0e0e0; min-height: 100vh; padding: 48px 24px; }
  .wrap { max-width: 760px; margin: 0 auto; }
  h1 { font-size: 1.4rem; font-weight: normal; letter-spacing: 0.1em; color: #fff; margin-bottom: 4px; }
  .sub { font-size: 0.78rem; color: #666; margin-bottom: 16px; }
  .notice { font-size: 0.75rem; color: #555; border-left: 2px solid #2a2a2a; padding: 8px 12px; margin-bottom: 32px; line-height: 1.6; }
  .notice a { color: #888; text-decoration: underline; }
  .notice a:hover { color: #ccc; }
  footer { margin-top: 56px; padding-top: 24px; border-top: 1px solid #1e1e1e; font-size: 0.7rem; color: #444; line-height: 1.8; }
  footer a { color: #555; text-decoration: underline; }
  footer a:hover { color: #aaa; }
  label { font-size: 0.75rem; color: #888; letter-spacing: 0.08em; text-transform: uppercase; display: block; margin-bottom: 8px; }
  textarea {
    width: 100%; height: 180px; background: #1a1a1a; border: 1px solid #2a2a2a;
    color: #e0e0e0; font-family: 'Courier New', monospace; font-size: 0.82rem;
    padding: 14px; resize: vertical; outline: none; border-radius: 4px;
  }
  textarea:focus { border-color: #444; }
  .row { display: flex; gap: 12px; margin-top: 12px; align-items: center; flex-wrap: wrap; }
  select {
    background: #1a1a1a; border: 1px solid #2a2a2a; color: #e0e0e0;
    font-family: 'Courier New', monospace; font-size: 0.82rem; padding: 10px 14px;
    border-radius: 4px; outline: none;
  }
  button {
    background: #e0e0e0; color: #0f0f0f; border: none; padding: 10px 28px;
    font-family: 'Courier New', monospace; font-size: 0.82rem; cursor: pointer;
    border-radius: 4px; font-weight: bold; letter-spacing: 0.05em;
  }
  button:hover { background: #fff; }
  button:disabled { background: #444; color: #666; cursor: not-allowed; }
  #status { font-size: 0.78rem; color: #666; margin-top: 20px; min-height: 18px; }
  #results { margin-top: 32px; }
  .summary { background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 4px; padding: 20px; margin-bottom: 20px; }
  .summary-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 12px; }
  .stat { text-align: center; }
  .stat-val { font-size: 1.8rem; color: #fff; }
  .stat-label { font-size: 0.7rem; color: #666; margin-top: 2px; }
  table { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
  th { text-align: left; color: #666; font-weight: normal; padding: 8px 10px; border-bottom: 1px solid #2a2a2a; letter-spacing: 0.06em; text-transform: uppercase; }
  td { padding: 10px 10px; border-bottom: 1px solid #1a1a1a; color: #ccc; word-break: break-all; }
  .amp { color: #6ee7b7; }
  .non { color: #f87171; }
  .dl { margin-top: 16px; }
  .dl button { background: transparent; color: #888; border: 1px solid #2a2a2a; font-size: 0.72rem; padding: 6px 16px; }
  .dl button:hover { color: #fff; border-color: #444; background: transparent; }
  .err { color: #f87171; font-size: 0.8rem; margin-top: 16px; }
  .example-btn { background: transparent; color: #555; border: 1px solid #222; font-size: 0.72rem; padding: 5px 12px; margin-left: auto; }
  .example-btn:hover { color: #aaa; border-color: #444; background: transparent; }
</style>
</head>
<body>
<div class="wrap">
  <h1>AMPidentifier</h1>
  <p class="sub">AMPidentifier: A Python toolkit for predicting antimicrobial peptides using ensemble machine learning and physicochemical descriptors.</p>
  <p class="notice">For advanced parameter control — custom models, batch processing, and pipeline integration — use the <a href="https://github.com/madsondeluna/AMPIdentifier" target="_blank">CLI version</a>.</p>

  <label>FASTA sequences</label>
  <textarea id="fasta" placeholder=">SequenceID
KRIVQRIKDFLRNLVPRTES"></textarea>

  <div class="row">
    <select id="model">
      <option value="ensemble">Ensemble (RF + SVM + GB)</option>
      <option value="rf">Random Forest</option>
      <option value="svm">SVM</option>
      <option value="gb">Gradient Boosting</option>
    </select>
    <button id="runBtn" onclick="runPrediction()">Run</button>
    <button class="example-btn" onclick="loadExample()">load example</button>
  </div>

  <div id="status"></div>
  <div id="results"></div>

  <footer>
    <p>Luna-Aragão, M. A., da Silva, R. L., Pacífico, J., Santos-Silva, C. A. &amp; Benko&#8209;Iseppon, A. M. (2025).
    AMPidentifier: A Python toolkit for predicting antimicrobial peptides using ensemble machine learning and physicochemical descriptors.
    GitHub repository. <a href="https://github.com/madsondeluna/AMPIdentifier" target="_blank">https://github.com/madsondeluna/AMPIdentifier</a></p>
    <p style="margin-top:8px;">This application is a property of the <strong style="color:#555;">Universidade Federal de Pernambuco (UFPE)</strong> and the <strong style="color:#555;">Laboratory of Plant Genetics and Biotechnology (LGBV)</strong>.</p>
    <p style="margin-top:8px;">Developer: <a href="mailto:madsondeluna@gmail.com">madsondeluna@gmail.com</a> &nbsp;·&nbsp; <a href="https://github.com/madsondeluna/AMPidentifierServerBETA/issues" target="_blank">Report an issue</a></p>
  </footer>
</div>

<script>
const EXAMPLE = `>AMP_1|Magainin-2|Xenopus_laevis|Cationic_amphipathic_helix
GIGKFLHSAKKFGKAFVGEIMNS
>AMP_2|LL-37|Homo_sapiens|Cathelicidin_family
LLGDFFRKSKEKIGKEFKRIVQRIKDFLRNLVPRTES
>AMP_3|Melittin|Apis_mellifera|Venom_peptide
GIGAVLKVLTTGLPALISWIKRKRQQ
>AMP_4|Cecropin_A|Hyalophora_cecropia|Antimicrobial_peptide
KWKLFKKIEKVGQNIRDGIIKAGPAVAVVGQATQIAK
>AMP_5|Indolicidin|Bos_taurus|Trp_Pro_rich
ILPWKWPWWPWRR
>Non_AMP_1|Insulin_Chain_B|Homo_sapiens|Peptide_hormone
FVNQHLCGSHLVEALYLVCGERGFFYTPKT
>Non_AMP_2|Serum_Albumin|Homo_sapiens|Globular_transport_protein
MKWVTFISLLFLFSSAYSRGVFRRDAHKSEVAHRFKDLGEENFKALVLIAFAQYLQQCPFEDHVKLVNEVTEFAKTCVADESAENCDKSLHTLFGDKLCTVATLRETYGEMADCCAKQEPERNECFLQHKDDNPNLPRLVRPEVDVMCTAFHDNEETFLKKYLYEIARRHPYFYAPELLFFAKRYKAAFTECCQAADKAACLLPKLDELRDEGKASSAKQRLKCASLQKFGERAFKAWAVARLSQRFPKAEFAEVSKLVTDLTKVHTECCHGDLLECADDRADLAKYICENQDSISSKLKECCEKPLLEKSHCIAEVENDEMPADLPSLAADFVESKDVCKNYAEAKDVFLGMFLYEYARRHPDYSVVLLLRLAKTYETTLEKCCAAADPHECYAKVFDEFKPLVEEPQNLIKQNCELFEQLGEYKFQNALLVRYTKKVPQVSTPTLVEVSRNLGKVGSKCCKHPEAKRMPCAEDYLSVVLNQLCVLHEKTPVSDRVTKCCTESLVNRRPCFSALEVDETYVPKEFNAETFTFHADICTLSEKERQIKKQTALVELVKHKPKATKEQLKAVMDDFAAFVEKCCKADDKETCFAEEGKKLVAASQAALGL
>Non_AMP_3|Hemoglobin_Subunit_Alpha|Homo_sapiens|Oxygen_transport
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR
>Non_AMP_4|Cytochrome_c|Saccharomyces_cerevisiae|Electron_transport
TEFKAGSAKKGATLFKTRCLQCHTVEKGGPHKVGPNLHGIFGRHSGQAEGYSYTDANIKKNVLWDENNMSEYLTNPKKYIPGTKMAFGGLKKEKDRNDLITYLKKACE
>Non_AMP_5|Ubiquitin|Homo_sapiens|Protein_degradation_tag
MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG`;

let lastData = null;

function loadExample() {
  document.getElementById('fasta').value = EXAMPLE;
}

async function runPrediction() {
  const fasta = document.getElementById('fasta').value.trim();
  const model = document.getElementById('model').value;
  const btn = document.getElementById('runBtn');
  const status = document.getElementById('status');
  const results = document.getElementById('results');

  if (!fasta) { status.innerHTML = '<span class="err">Paste at least one FASTA sequence.</span>'; return; }

  btn.disabled = true;
  status.textContent = 'Running prediction...';
  results.innerHTML = '';

  const form = new FormData();
  form.append('fasta_sequence', fasta);
  form.append('model', model);

  try {
    const res = await fetch('/predict', { method: 'POST', body: form });
    const data = await res.json();

    if (data.error) {
      status.innerHTML = '<span class="err">Error: ' + data.error + '</span>';
    } else {
      lastData = data.predictions;
      status.textContent = '';
      renderResults(data);
    }
  } catch (e) {
    status.innerHTML = '<span class="err">Request failed: ' + e.message + '</span>';
  } finally {
    btn.disabled = false;
  }
}

function renderResults(data) {
  const preds = data.predictions;
  const ampKey = Object.keys(preds[0]).find(k => k.startsWith('pred_') || k === 'ensemble_prediction');
  const probKey = Object.keys(preds[0]).find(k => k.includes('prob'));

  const amps = preds.filter(r => r[ampKey] === 1 || r[ampKey] === true).length;
  const total = preds.length;

  let rows = preds.map(r => {
    const isAmp = r[ampKey] === 1 || r[ampKey] === true;
    const prob = probKey ? (r[probKey] * 100).toFixed(1) + '%' : '—';
    const label = isAmp ? '<span class="amp">AMP</span>' : '<span class="non">non-AMP</span>';
    return `<tr><td>${r.ID || r.id || '—'}</td><td>${r.sequence || '—'}</td><td>${label}</td><td>${prob}</td></tr>`;
  }).join('');

  document.getElementById('results').innerHTML = `
    <div class="summary">
      <label>Results — ${data.model}</label>
      <div class="summary-grid">
        <div class="stat"><div class="stat-val">${total}</div><div class="stat-label">sequences</div></div>
        <div class="stat"><div class="stat-val" style="color:#6ee7b7">${amps}</div><div class="stat-label">predicted AMP</div></div>
        <div class="stat"><div class="stat-val" style="color:#f87171">${total - amps}</div><div class="stat-label">predicted non-AMP</div></div>
      </div>
    </div>
    <table>
      <thead><tr><th>ID</th><th>Sequence</th><th>Prediction</th><th>Prob. AMP</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
    <div class="dl"><button onclick="downloadCSV()">download CSV</button></div>`;
}

function downloadCSV() {
  if (!lastData) return;
  const keys = Object.keys(lastData[0]);
  const csv = [keys.join(','), ...lastData.map(r => keys.map(k => JSON.stringify(r[k] ?? '')).join(','))].join('\\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
  a.download = 'ampidentifier_' + new Date().toISOString().slice(0,10) + '.csv';
  a.click();
}
</script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        fasta_text = request.form.get('fasta_sequence', '').strip()
        model_choice = request.form.get('model', 'ensemble')

        if not fasta_text:
            return jsonify({'error': 'No FASTA sequence provided'}), 400

        with tempfile.TemporaryDirectory() as tmp:
            fasta_path = os.path.join(tmp, 'input.fasta')
            with open(fasta_path, 'w') as f:
                f.write(fasta_text)

            sequences, seq_ids = load_fasta_sequences(fasta_path)
            if not sequences:
                return jsonify({'error': 'Invalid FASTA format or empty file'}), 400

            output_dir = os.path.join(tmp, 'out')
            os.makedirs(output_dir)

            use_ensemble = model_choice == 'ensemble'
            run_prediction_pipeline(
                input_file=fasta_path,
                output_dir=output_dir,
                internal_model_type='rf' if use_ensemble else model_choice,
                use_ensemble=use_ensemble,
                external_model_paths=[]
            )

            predictions_df = pd.read_csv(os.path.join(output_dir, 'prediction_comparison_report.csv'))

            return jsonify({
                'model': model_choice,
                'num_sequences': len(sequences),
                'predictions': predictions_df.to_dict(orient='records')
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
