data = readtable("E:\Project Dataset\dreamt-dataset-for-real-time-sleep-stage-estimation-using-multisensor-wearable-technology-2.1.0\data_64Hz\S006_whole_df.csv");

time = data.TIMESTAMP;          % time column
hr   = data.HR;     % heart rate column

figure
plot(time, hr, 'r--o', 'LineWidth', 0.5,'MarkerIndices',0.7)

xlabel('Time')
ylabel('Heart Rate (bpm)')
title('Heart Rate vs Time')

grid on



Fs = 1/0.015625;                 % sampling frequency
t = (0:length(hr)-1)/Fs;

plot(t, hr)
xlabel('Time (seconds)')
ylabel('Heart Rate (bpm)')
grid on


