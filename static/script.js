// File input handling
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadBtn = document.getElementById('uploadBtn');
const fileInfo = document.getElementById('fileInfo');
const errorSection = document.getElementById('errorSection');
const resultsSection = document.getElementById('resultsSection');
const loading = document.getElementById('loading');
const musicToggle = document.getElementById('musicToggle');
const bgMusic = document.getElementById('bgMusic');

let selectedFile = null;

// Drag and drop handling
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    if (!file.name.endsWith('.csv')) {
        showError('Please select a CSV file');
        return;
    }

    selectedFile = file;
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = (file.size / 1024).toFixed(2) + ' KB';
    fileInfo.style.display = 'block';
    uploadBtn.disabled = false;
}

// Upload and predict
uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    loading.style.display = 'block';
    errorSection.style.display = 'none';
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            showError(data.error || 'An error occurred during analysis');
            return;
        }

        displayResults(data);
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        loading.style.display = 'none';
    }
});

function showError(message) {
    errorSection.style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
    resultsSection.style.display = 'none';
}

function displayResults(data) {
    resultsSection.style.display = 'block';
    errorSection.style.display = 'none';

    // Update quality score
    const qualityScore = data.quality_score;
    document.getElementById('qualityScore').textContent = qualityScore;
    document.getElementById('confidence').textContent = data.average_confidence;

    // Display stages breakdown
    const stagesGrid = document.getElementById('stagesGrid');
    stagesGrid.innerHTML = '';

    const stageInfo = data.stage_info;
    const totalWindows = data.total_windows;

    for (const [stage, count] of Object.entries(data.stage_counts)) {
        const percentage = ((count / totalWindows) * 100).toFixed(1);
        const info = stageInfo[stage] || { emoji: '❓', description: stage, color: '#999' };

        const stageBox = document.createElement('div');
        stageBox.className = 'stage-box';
        stageBox.innerHTML = `
            <div class="stage-emoji">${info.emoji}</div>
            <div class="stage-name">${stage}</div>
            <div class="stage-count">${count}</div>
            <div class="stage-percent">${percentage}%</div>
        `;
        stagesGrid.appendChild(stageBox);
    }

    // Display timeline
    const timeline = document.getElementById('timeline');
    timeline.innerHTML = '';

    data.stages.forEach((stage, index) => {
        const info = stageInfo[stage] || { color: '#999' };
        const block = document.createElement('div');
        block.className = 'timeline-block';
        block.style.backgroundColor = info.color;
        block.setAttribute('data-stage', `${stage} (${index + 1})`);
        block.title = `${stage} - Window ${index + 1}`;
        timeline.appendChild(block);
    });

    // Display analysis details
    const analysisDetails = document.getElementById('analysisDetails');
    analysisDetails.innerHTML = '';

    for (const [stage, count] of Object.entries(data.stage_counts)) {
        const percentage = ((count / totalWindows) * 100).toFixed(1);
        const row = document.createElement('div');
        row.className = 'table-row';
        row.innerHTML = `
            <div>${stageInfo[stage].emoji} ${stage}</div>
            <div>${count} windows (~${Math.round(count * 30)} seconds)</div>
            <div>${percentage}%</div>
        `;
        analysisDetails.appendChild(row);
    }

    // Generate recommendations
    generateRecommendations(data.stage_counts, qualityScore, totalWindows);

    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

function generateRecommendations(stageCounts, qualityScore, totalWindows) {
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = '';

    const recommendations = [];

    // Calculate sleep composition
    const deepSleepPercent = ((stageCounts['N3'] || 0) / totalWindows) * 100;
    const remPercent = ((stageCounts['REM'] || 0) / totalWindows) * 100;
    const lightSleepPercent = ((stageCounts['N1'] || 0) / totalWindows) * 100;
    const wakePercent = ((stageCounts['Wake'] || 0) / totalWindows) * 100;

    // Quality-based recommendations
    if (qualityScore >= 80) {
        recommendations.push('🌟 Excellent sleep quality! Keep maintaining your current sleep schedule.');
        recommendations.push('💪 Your sleep pattern shows healthy deep sleep and REM cycles.');
    } else if (qualityScore >= 60) {
        recommendations.push('😌 Good sleep quality. Consider slightly earlier bedtime for more rest.');
        recommendations.push('🎯 You could benefit from more consistent sleep patterns.');
    } else {
        recommendations.push('⚠️ Your sleep quality needs improvement. Try to increase deep sleep.');
        recommendations.push('😴 Aim for 7-9 hours of consistent sleep each night.');
    }

    // Deep sleep recommendations
    if (deepSleepPercent < 15) {
        recommendations.push('💤 Deep sleep is important for physical recovery. Reduce screen time 1 hour before bed.');
        recommendations.push('🛏️ Maintain a cool, dark bedroom (around 65-68°F / 18-20°C).');
    }

    // REM sleep recommendations
    if (remPercent < 20) {
        recommendations.push('🧠 REM sleep is crucial for memory. Manage stress and avoid caffeine after 2 PM.');
        recommendations.push('🎭 Ensure 7-9 hours of total sleep for adequate REM cycles.');
    }

    // Light sleep observations
    if (lightSleepPercent > 30) {
        recommendations.push('🔄 High light sleep may indicate frequent awakenings. Check your sleep environment.');
    }

    // Wake periods
    if (wakePercent > 5) {
        recommendations.push('👁️ Minimize awakenings by establishing a relaxing pre-sleep routine.');
    }

    // General recommendations
    if (qualityScore < 100) {
        recommendations.push('📱 Put your phone on silent and keep it away from bed.');
        recommendations.push('🍵 Avoid alcohol 4-6 hours before sleep as it disrupts sleep cycles.');
    }

    // Display recommendations
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendationsList.appendChild(li);
    });
}

// Music control
function toggleMusic() {
    if (bgMusic.paused) {
        bgMusic.play().catch(error => {
            console.log('Autoplay prevented:', error);
        });
        musicToggle.classList.add('active');
        musicToggle.textContent = '🔊 Music Playing';
    } else {
        bgMusic.pause();
        musicToggle.classList.remove('active');
        musicToggle.textContent = '🔇 Music Paused';
    }
}

// Try to play music on page load (may be blocked by browser autoplay policy)
window.addEventListener('load', () => {
    bgMusic.muted = false;
    bgMusic.play().catch(error => {
        console.log('Autoplay policy prevented music from playing. User can enable it manually.');
    });
});

// Allow unmuting on first user interaction
document.addEventListener('click', () => {
    if (bgMusic.muted) {
        bgMusic.muted = false;
    }
}, { once: true });
