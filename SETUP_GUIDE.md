# Sleep Quality Assessment Web Application - Setup Guide 🌙

## What You've Built

A complete web-based sleep analysis system that:
- ✅ Accepts Heart Rate (HR) CSV data from users
- ✅ Uses your trained CNN-LSTM deep learning model
- ✅ Predicts sleep stages (Wake, N1, N2, N3, REM)
- ✅ Calculates sleep quality score (0-100%)
- ✅ Provides personalized sleep recommendations
- ✅ Displays beautiful dark-themed interface with soothing music
- ✅ Shows interactive timeline and detailed analytics

## Quick Start Guide

### Step 1: Install Dependencies

```bash
# Navigate to your project directory
cd "d:\IIT KHARAGPUR\Sem6\IS Project"

# Install required Python packages
pip install -r requirements.txt
```

**Dependencies included:**
- Flask - Web framework
- TensorFlow - Deep learning model
- Pandas & NumPy - Data processing
- Scikit-learn - Machine learning utilities

### Step 2: Run the Application

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 3: Open in Browser

Go to: **http://localhost:5000**

You should see the beautiful dark-themed sleep analysis website!

## Testing with Sample Data

A sample CSV file is included: `sample_data.csv`

1. On the website, click "Click to Browse" or drag-drop
2. Select `sample_data.csv`
3. Click "Analyze Sleep Data"
4. View the results!

## Using Your Own Data

Your CSV file needs:
- **Column name**: `HR` (exactly)
- **Minimum 1920 rows** (for one 30-second window)
- **CSV format**

Example CSV content:
```
HR
72.5
73.1
72.8
...
```

## Features Explained

### 🎯 Sleep Quality Score
- **80-100%**: Excellent sleep ⭐⭐⭐⭐⭐
- **60-79%**: Good sleep ⭐⭐⭐⭐
- **40-59%**: Fair sleep ⭐⭐⭐
- **Below 40%**: Poor sleep ⭐⭐

### 😴 Sleep Stages
| Stage | Emoji | Meaning | % of Sleep |
|-------|-------|---------|-----------|
| Wake | 👁️ | Awake | 0-5% |
| N1 | 😴 | Light sleep | 5-10% |
| N2 | 💤 | Moderate sleep | 45-55% |
| N3 | 😪 | Deep sleep | 10-20% |
| REM | 🎬 | Dream sleep | 20-25% |

### 🔊 Soothing Music
- Click "Enable Soothing Music" button to play background music
- Browser autoplay policies may require user interaction first
- Music helps create a calming assessment experience

## Project Structure

```
app.py                      ← Flask server (main backend)
requirements.txt            ← Python dependencies
sleep_model.h5              ← Your trained model
sample_data.csv             ← Test data
templates/
  └── index.html            ← Website interface
static/
  ├── style.css             ← Beautiful dark theme
  ├── script.js             ← Interactive features
  └── soothing-music.mp3    ← Background music (optional)
```

## Customization Options

### Add Your Own Background Music

1. Get a soothing MP3 file (Spotify, YouTube Music, etc.)
2. Convert to MP3 if needed
3. Place as `static/soothing-music.mp3`
4. Restart the app

### Change the Theme Colors

Edit `static/style.css` and modify the CSS variables:

```css
:root {
    --bg-primary: #0a0e27;      /* Dark background */
    --accent-primary: #6366f1;  /* Purple accent */
    --success: #4ecdc4;         /* Teal for good stages */
}
```

### Modify Sleep Recommendations

Edit `static/script.js`, find the `generateRecommendations()` function and customize the sleep tips.

## Troubleshooting

### Issue: Port 5000 already in use
**Solution**: Change port in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Issue: Module not found (Flask, TensorFlow, etc.)
**Solution**: 
```bash
pip install Flask TensorFlow pandas numpy scikit-learn
```

### Issue: Model loading fails
**Solution**: Make sure `sleep_model.h5` is in the same directory as `app.py`

### Issue: CSV upload error
**Solutions**:
- Check column name is exactly `HR` (capital)
- Ensure at least 1920 rows
- Make sure it's CSV format, not Excel

### Issue: Music not playing
**Solution**: 
- Click the music button to enable
- Add your MP3 file to `static/` folder
- Some browsers restrict autoplay - user click enables it

### Issue: Predictions look wrong
**Solution**: 
- Use HR data from the same format as training
- Ensure data is from 64Hz sampling rate
- Check values are realistic HR readings (60-100 BPM typical)

## How It Works (Technical Details)

### Data Flow
1. User uploads CSV with HR data
2. Backend reads and processes data
3. HR values are normalized (StandardScaler)
4. Data split into 1920-sample windows
5. Each window passed to CNN-LSTM model
6. Model predicts sleep stage for each window
7. Results processed and displayed

### Model Architecture
```
Input: (1920, 1)
  ↓
Conv1D(32) + ReLU + MaxPool
  ↓
Conv1D(64) + ReLU + MaxPool
  ↓
LSTM(64)
  ↓
Dense(32) + ReLU
  ↓
Dense(5) + Softmax ← Outputs probabilities for 5 sleep stages
```

### Quality Score Calculation
```
Deep Sleep (N3):  25 points per window
REM Sleep:        20 points per window
Moderate (N2):    15 points per window
Light (N1):       10 points per window
Wake:             0 points per window

Quality Score = (Total Points / Total Windows) × 1.5
Max: 100%
```

## Deployment Options

### Local Only (Current Setup)
- Access from: `http://localhost:5000`
- Only available on your computer
- Perfect for testing

### Share on Local Network
```python
# In app.py change:
app.run(debug=True, port=5000, host='0.0.0.0')
```
Then access from: `http://YOUR_IP:5000`

### Deploy Online
- **Heroku**: Free tier available
- **PythonAnywhere**: Easy Flask hosting
- **AWS/Google Cloud**: Scalable options

## File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask server - handles requests and model predictions |
| `templates/index.html` | Web interface - what users see |
| `static/style.css` | Dark theme styling and animations |
| `static/script.js` | Frontend logic - file upload, results display |
| `sleep_model.h5` | Trained CNN-LSTM model - makes predictions |
| `requirements.txt` | List of Python packages to install |
| `worl.ipynb` | Jupyter notebook with model training code |

## API Reference

### POST `/predict`

**Endpoint**: `http://localhost:5000/predict`

**Input**: 
- File: CSV with `HR` column

**Output**:
```json
{
  "success": true,
  "stages": ["N2", "N2", "REM", "N3", ...],
  "stage_counts": {
    "Wake": 5,
    "N1": 20,
    "N2": 150,
    "N3": 40,
    "REM": 50
  },
  "total_windows": 265,
  "quality_score": 85,
  "average_confidence": 94.3
}
```

## Next Steps

1. ✅ Run the application locally
2. ✅ Test with `sample_data.csv`
3. ✅ Upload your own HR data
4. ✅ Customize the theme and recommendations
5. ✅ Add your own background music
6. ✅ Share with others on your network
7. ✅ Deploy online if desired

## Support & Resources

- Flask Documentation: https://flask.palletsprojects.com/
- TensorFlow Guide: https://www.tensorflow.org/guide
- Sleep Science: https://en.wikipedia.org/wiki/Sleep

## Performance Tips

- For faster processing: Increase `batch_size` in model predictions
- For better accuracy: Train model with more sleep data
- For smoother UI: Use modern browser (Chrome, Firefox, Edge)

---

**Enjoy analyzing sleep quality!** 🌙💤

For questions or improvements, check the GitHub repository or create an issue.
