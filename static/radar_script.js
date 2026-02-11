let chart = null;
let recordingStartTime = null;
let updateInterval = null;

// Initialize chart
function initChart() {
    const ctx = document.getElementById('liveChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'unwrapPhasePeak_mm',
                data: [],
                borderColor: '#00bfff',
                backgroundColor: 'rgba(0, 191, 255, 0.1)',
                borderWidth: 2,
                tension: 0.1,
                fill: true,
                pointRadius: 2,
                pointBackgroundColor: '#00bfff',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#e0e0e0' }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#a0a0a0' },
                    grid: { color: 'rgba(0, 191, 255, 0.1)' }
                },
                y: {
                    ticks: { color: '#a0a0a0' },
                    grid: { color: 'rgba(0, 191, 255, 0.1)' }
                }
            }
        }
    });
}

async function startRecording() {
    const port = document.getElementById('comPort').value;
    const duration = parseInt(document.getElementById('duration').value);

    if (!port) {
        showError('Please enter a COM port');
        return;
    }

    if (duration <= 0) {
        showError('Duration must be greater than 0');
        return;
    }

    try {
        const response = await fetch('/start-recording', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ port, duration })
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.error || 'Failed to start recording');
            return;
        }

        recordingStartTime = Date.now();
        showStatus(`Recording: ${data.message}`);
        
        document.getElementById('startBtn').disabled = true;
        document.getElementById('stopBtn').disabled = false;
        document.getElementById('sheetStatus').className = 'status-badge status-syncing';
        document.getElementById('sheetStatus').textContent = 'Syncing...';

        // Update live data every 500ms
        updateInterval = setInterval(updateLiveData, 500);

        // Auto-stop after duration
        setTimeout(() => {
            if (!document.getElementById('startBtn').disabled) {
                stopRecording();
            }
        }, duration * 1000);

    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

async function stopRecording() {
    try {
        if (updateInterval) clearInterval(updateInterval);

        const response = await fetch('/stop-recording', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.error || 'Failed to stop recording');
            return;
        }

        showStatus(`Recording stopped. Total points: ${data.total_points}`);
        
        document.getElementById('startBtn').disabled = false;
        document.getElementById('stopBtn').disabled = true;
        document.getElementById('sheetStatus').className = 'status-badge status-waiting';
        document.getElementById('sheetStatus').textContent = 'Synced ✓';

        // Get final statistics
        updateStats();

    } catch (error) {
        showError('Network error: ' + error.message);
    }
}

async function updateLiveData() {
    try {
        const response = await fetch('/get-live-data');
        const data = await response.json();

        if (!response.ok) return;

        const { data_points, is_recording } = data;

        // Update point count
        document.getElementById('pointCount').textContent = data_points.length;

        // Update current value
        if (data_points.length > 0) {
            const lastPoint = data_points[data_points.length - 1];
            document.getElementById('currentValue').textContent = lastPoint.value.toFixed(2);
        }

        // Update recording time
        if (is_recording && recordingStartTime) {
            const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            document.getElementById('recordTime').textContent = 
                `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        }

        // Update chart
        if (chart && data_points.length > 0) {
            chart.data.labels = data_points.map(p => p.time.toFixed(1));
            chart.data.datasets[0].data = data_points.map(p => p.value);
            chart.update('none');
        }

        // Update table (last 10 rows)
        updateDataTable(data_points);

        // Update stats
        await updateStats();

    } catch (error) {
        console.log('Update error:', error);
    }
}

function updateDataTable(data_points) {
    const tbody = document.getElementById('dataTableBody');
    const lastRows = data_points.slice(-10);

    tbody.innerHTML = lastRows.map(point => `
        <tr>
            <td>${point.time.toFixed(3)}</td>
            <td>${point.value.toFixed(2)}</td>
        </tr>
    `).join('');
}

async function updateStats() {
    try {
        const response = await fetch('/get-stats');
        
        if (!response.ok) return;

        const stats = await response.json();

        document.getElementById('statMean').textContent = stats.mean;
        document.getElementById('statMin').textContent = stats.min;
        document.getElementById('statMax').textContent = stats.max;
        document.getElementById('statStd').textContent = stats.std;

    } catch (error) {
        console.log('Stats error:', error);
    }
}

function showStatus(message) {
    const statusBox = document.getElementById('status');
    document.getElementById('statusMessage').textContent = message;
    statusBox.style.display = 'block';
    document.getElementById('errorBox').style.display = 'none';
}

function showError(message) {
    const errorBox = document.getElementById('errorBox');
    document.getElementById('errorMessage').textContent = message;
    errorBox.style.display = 'block';
    document.getElementById('status').style.display = 'none';
}

// Initialize on page load
window.addEventListener('load', () => {
    initChart();
});
