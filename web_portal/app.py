"""
AMPidentifier Web Portal
Flask application for antimicrobial peptide prediction
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import tempfile
import pandas as pd
from datetime import datetime
import io

# Add parent directory to path to import amp_identifier modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from amp_identifier.core import run_prediction_pipeline
from amp_identifier.data_io import load_fasta_sequences

app = Flask(__name__, template_folder='.')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Example FASTA sequence
EXAMPLE_FASTA = """>sp|P0C8L5|AMP1_HUMAN Antimicrobial peptide 1
KRIVQRIKDFLRNLVPRTES
>sp|P81534|DEF1_PHAVU Defensin-1
RTCESQSHKFKGQCRDDFCYTKQCVVNKACHVGGRCVKPFCCK
>sp|P0DJI8|DEF1_HUMAN Defensin-1
DCYCRIPACIAGERRYGTCIYQGRLWAFCC"""


@app.route('/')
def index():
    """Home page with information about AMPidentifier"""
    return render_template('index.html')


@app.route('/predict')
def predict_page():
    """Prediction interface page"""
    return render_template('predict.html', example_fasta=EXAMPLE_FASTA)


@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for running predictions"""
    try:
        # Get input data
        fasta_text = request.form.get('fasta_sequence', '').strip()
        model_choice = request.form.get('model', 'ensemble')

        if not fasta_text:
            return jsonify({'error': 'No FASTA sequence provided'}), 400

        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save FASTA to temporary file
            fasta_path = os.path.join(temp_dir, 'input.fasta')
            with open(fasta_path, 'w') as f:
                f.write(fasta_text)

            # Validate FASTA format
            try:
                sequences, seq_ids = load_fasta_sequences(fasta_path)
                if not sequences:
                    return jsonify({'error': 'Invalid FASTA format or empty file'}), 400
            except Exception as e:
                return jsonify({'error': f'FASTA parsing error: {str(e)}'}), 400

            # Set up output directory
            output_dir = os.path.join(temp_dir, 'results')
            os.makedirs(output_dir, exist_ok=True)

            # Run prediction based on model choice
            use_ensemble = model_choice == 'ensemble'
            internal_model_type = 'rf' if use_ensemble else model_choice

            run_prediction_pipeline(
                input_file=fasta_path,
                output_dir=output_dir,
                internal_model_type=internal_model_type,
                use_ensemble=use_ensemble,
                external_model_paths=[]
            )

            # Read results
            features_path = os.path.join(output_dir, 'physicochemical_features.csv')
            predictions_path = os.path.join(output_dir, 'prediction_comparison_report.csv')

            features_df = pd.read_csv(features_path)
            predictions_df = pd.read_csv(predictions_path)

            # Prepare response data
            response_data = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'model': model_choice,
                'num_sequences': len(sequences),
                'predictions': predictions_df.to_dict(orient='records'),
                'features': features_df.to_dict(orient='records'),
                'features_columns': list(features_df.columns),
                'predictions_columns': list(predictions_df.columns)
            }

            return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500


@app.route('/api/download/<data_type>', methods=['POST'])
def download(data_type):
    """Download results as CSV or PDF"""
    try:
        data = request.json.get('data', [])

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        df = pd.DataFrame(data)
        output = io.BytesIO()

        if data_type == 'csv':
            df.to_csv(output, index=False)
            output.seek(0)
            return send_file(
                output,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'ampidentifier_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            )
        else:
            return jsonify({'error': 'Invalid download type'}), 400

    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500


@app.route('/about')
def about():
    """About page with detailed information"""
    return render_template('about.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
