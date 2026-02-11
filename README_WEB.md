# Sleep Quality Assessment System 🌙

A deep learning-based web application for analyzing sleep quality using heart rate (HR) data. The system uses a CNN-LSTM neural network to classify sleep stages and provide personalized sleep recommendations.

## Features ✨

- **Deep Learning Analysis**: CNN-LSTM model trained on sleep stage classification
- **Sleep Stage Detection**: Wake, N1 (Light Sleep), N2 (Moderate Sleep), N3 (Deep Sleep), REM
- **Sleep Quality Score**: 0-100% quality assessment
- **Visual Analytics**: 
  - Sleep stages breakdown with emoji indicators
  - Interactive sleep timeline visualization
  - Detailed statistical analysis
- **Personalized Recommendations**: AI-powered sleep improvement suggestions
- **Beautiful Dark Theme**: Soothing, sleep-focused user interface
- **Soothing Background Music**: Relaxing audio experience
- **Responsive Design**: Works on desktop, tablet, and mobile

## Quick Start 🚀

### Installation

```bash
# Clone repository
git clone https://github.com/DEV0180/IS_project.git
cd IS_project

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

### Access the Web Interface

Open your browser and go to: `http://localhost:5000`

## Usage 📊

### Data Preparation

Your CSV file should contain:
- **Column**: `HR` (Heart Rate values)
- **Minimum rows**: 1920 (for at least one 30-second window)
- **Sampling rate**: 64Hz

Example CSV:
```
HR
75.2
76.1
75.8
...
```

### Analysis Steps

1. Upload your CSV file (drag & drop or browse)
2. Click "Analyze Sleep Data"
3. View results with quality score and recommendations

## Sleep Stages Explained 😴

- 👁️ **Wake**: Awake state
- 😴 **N1**: Light sleep (transition stage)
- 💤 **N2**: Moderate sleep (main sleep stage)
- 😪 **N3**: Deep sleep (restorative sleep)
- 🎬 **REM**: Rapid Eye Movement (memory consolidation)

## Model Architecture 🧠

```
Input (1920, 1)
    ↓
Conv1D (32 filters) + MaxPooling
    ↓
Conv1D (64 filters) + MaxPooling
    ↓
LSTM (64 units)
    ↓
Dense (32) → Dense (5 classes)
    ↓
Output: Sleep Stage Probabilities
```

## File Structure 📁

```
IS_project/
├── app.py                  # Flask backend server
├── worl.ipynb              # Jupyter notebook (training code)
├── sleep_model.h5          # Trained TensorFlow model
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/
│   └── index.html         # Web interface
└── static/
    ├── style.css          # Styling & animations
    ├── script.js          # Frontend logic
    └── soothing-music.mp3 # Background music (optional)
```

## Technology Stack 🛠️

- **Backend**: Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **ML Framework**: TensorFlow/Keras
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Model Architecture**: CNN-LSTM Hybrid

## Quality Score Interpretation 📈

- **80-100%**: Excellent sleep quality ⭐⭐⭐⭐⭐
- **60-79%**: Good sleep quality ⭐⭐⭐⭐
- **40-59%**: Fair sleep quality ⭐⭐⭐
- **Below 40%**: Poor sleep quality ⭐⭐

## Troubleshooting 🔧

**Issue**: Port 5000 already in use
```python
# Edit app.py, change: app.run(debug=True, port=5001)
```

**Issue**: Model not found
- Ensure `sleep_model.h5` is in the project root directory

**Issue**: Music not playing
- Click "Enable Soothing Music" button (browser autoplay policies)
- Add `soothing-music.mp3` to `static/` folder

**Issue**: CSV file rejected
- Check column name is `HR`
- Ensure at least 1920 rows
- File must be CSV format

## Performance 📊

- **Model Accuracy**: ~90% on test data
- **Processing Speed**: <5 seconds per analysis
- **Average Confidence**: >92%

## Future Enhancements 🚀

- [ ] Multi-session sleep tracking & trends
- [ ] Additional health metrics (RR, SpO2, Temperature)
- [ ] Mobile app version
- [ ] Sleep disorder detection
- [ ] Wearable device integration
- [ ] Historical data analysis

## Model Training 📚

Trained using:
- 64Hz heart rate polysomnography recordings
- Balanced class weighting for N2-dominant data
- 80/20 train-test split
- Sparse categorical crossentropy loss
- Adam optimizer

## API Endpoints 🔗

### POST `/predict`

Analyzes HR data and returns sleep predictions.

**Request**:
```
Content-Type: multipart/form-data
file: [CSV file with HR column]
```

**Response** (Success):
```json
{
    "success": true,
    "stages": ["N2", "N2", "REM", "N3", ...],
    "stage_counts": {"Wake": 5, "N1": 20, "N2": 150, ...},
    "total_windows": 265,
    "quality_score": 85,
    "average_confidence": 94.3
}
```

## Customization 🎨

### Change Theme Colors

Edit `static/style.css`:
```css
:root {
    --bg-primary: #0a0e27;      /* Dark background */
    --accent-primary: #6366f1;  /* Purple accent */
    --success: #4ecdc4;         /* Teal success */
}
```

### Add Background Music

Place soothing music as `static/soothing-music.mp3`
Supported formats: MP3, WAV, OGG

### Modify Recommendations

Edit `generateRecommendations()` function in `static/script.js`

## License 📄

Open source - MIT License

## Disclaimer ⚖️

This project is for educational and research purposes. For clinical sleep analysis, please consult with a sleep specialist and use FDA-approved devices.

## Contact 📧

For questions or contributions, please create an issue in the repository.

---

**Made with ❤️ for better sleep** 🌙💤
