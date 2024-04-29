import numpy as np
import pyaudio
import time
import mne

# Initialize the EEG device
mne.setup_self_contained_bids_environment(data_path='./data')
# raw = mne.io.read_raw_fif('my_eeg_device.fif', preload=True)

# Set up the stimuli
tone_frequencies = [200, 400, 600, 800, 1000]  # Frequencies for the tones in Hz
stim_dur = 800  # ms
isi = 1000  # ms
n_trials = 40
n_targets = 8

# Prepare EEG recording
eeg_data = []

# Function to generate a tone
def generate_tone(frequency, duration, sampling_rate=44100):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    waveform = np.sin(2 * np.pi * frequency * t)
    return waveform

# Function to record EEG data
def record_eeg_data():
    # Record EEG data here and append it to eeg_data list
    pass  # Replace this with your EEG recording code

# Function to play audio
def play_audio(data, sampling_rate=44100):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sampling_rate,
                    output=True)
    stream.write(data.astype(np.float32).tostring())
    stream.close()
    p.terminate()

# Present the stimuli
for trial in range(n_trials):
    if trial < n_targets:
        # This is a target trial
        tone_frequency = tone_frequencies[trial % len(tone_frequencies)]
        tone = generate_tone(tone_frequency, stim_dur / 1000)  # Convert stim_dur to seconds
        play_audio(tone)
        record_eeg_data()
    else:
        # This is a control trial
        tone = generate_tone(tone_frequencies[0], stim_dur / 1000)  # Use the first frequency as control
        play_audio(tone)
        record_eeg_data()
    time.sleep((stim_dur + isi) / 1000)  # wait for the duration of the stimulus and ISI

# Save EEG data to a file
# with open('eeg_data.csv', 'w') as f:
#     for data_point in eeg_data:
#         f.write(f"{data_point}\n")
