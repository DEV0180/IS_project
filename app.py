from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import os
import traceback

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the trained model
try:
    model = tf.keras.models.load_model('sleep_model.h5')
    print("✓ Model loaded successfully")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    model = None

# Sleep stage descriptions
STAGE_INFO = {
    'Wake': {'emoji': '👁️', 'description': 'Awake', 'color': '#FF6B6B'},
    'N1': {'emoji': '😴', 'description': 'Light Sleep (N1)', 'color': '#4ECDC4'},
    'N2': {'emoji': '💤', 'description': 'Moderate Sleep (N2)', 'color': '#1A535C'},
    'N3': {'emoji': '😪', 'description': 'Deep Sleep (N3)', 'color': '#0A1128'},
    'REM': {'emoji': '🎬', 'description': 'REM Sleep', 'color': '#FF006E'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Please upload a CSV file'}), 400
        
        # Save and process file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Read CSV with chunking for large files
        try:
            df = pd.read_csv(filepath, usecols=['HR'])
        except Exception as e:
            os.remove(filepath)
            return jsonify({'error': f'CSV error: {str(e)}'}), 400
        
        # Normalize HR
        scaler = StandardScaler()
        df['HR_scaled'] = scaler.fit_transform(df[['HR']]).astype(np.float32)
        
        # Create windows
        WINDOW_SIZE = 1920
        windows = []
        num_windows = len(df) // WINDOW_SIZE
        
        if num_windows == 0:
            os.remove(filepath)
            return jsonify({'error': f'CSV must have at least {WINDOW_SIZE} rows'}), 400
        
        for i in range(num_windows):
            start = i * WINDOW_SIZE
            window = df['HR_scaled'].iloc[start : start + WINDOW_SIZE].values
            windows.append(window)
        
        X_input = np.array(windows).reshape(-1, WINDOW_SIZE, 1)
        
        # Make predictions
        predictions = model.predict(X_input, verbose=0)
        predicted_stages = np.argmax(predictions, axis=1)
        
        # Map numbers to stage names
        stage_map = {0: 'Wake', 1: 'N1', 2: 'N2', 3: 'REM'}
        readable_stages = [stage_map.get(p, 'Unknown') for p in predicted_stages]
        
        # Calculate statistics
        stage_counts = {}
        for stage in readable_stages:
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
        
        # Get confidence scores
        confidence_scores = np.max(predictions, axis=1)
        avg_confidence = float(np.mean(confidence_scores))
        
        # Calculate sleep quality score (0-100)
        # Deep sleep and REM are better than light sleep
        quality_score = 0
        for stage, count in stage_counts.items():
            if stage == 'N3':  # Deep sleep
                quality_score += count * 25
            elif stage == 'REM':  # REM sleep
                quality_score += count * 20
            elif stage == 'N2':  # Moderate sleep
                quality_score += count * 15
            elif stage == 'N1':  # Light sleep
                quality_score += count * 10
        
        total_windows = len(readable_stages)
        quality_score = min(100, int((quality_score / total_windows) * 1.5)) if total_windows > 0 else 0
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'stages': readable_stages,
            'stage_counts': stage_counts,
            'total_windows': total_windows,
            'quality_score': quality_score,
            'average_confidence': round(avg_confidence * 100, 2),
            'stage_info': STAGE_INFO
        })
    
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
