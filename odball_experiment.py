import streamlit as st
import numpy as np
import pyaudio
import time
from pylsl import StreamInfo, StreamOutlet

# Function to generate a tone
def generate_tone(frequency, duration, sampling_rate=44100):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    waveform = np.sin(2 * np.pi * frequency * t)
    return waveform

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

# Streamlit app
def main():
    st.title("Auditory Oddball Experiment")
    st.write("Click the button below to start the experiment.")

    # Create a unique key for the stop button
    stop_button_key = "stop_button"

    # Add permanent stop button
    stop_experiment = st.button("Stop Experiment", key=stop_button_key)

    if st.button("Start Experiment"):
        # Create an EEG stream outlet
        eeg_info = StreamInfo('EEGStream', 'EEG', 8, 100, 'float32', 'my_eeg_stream')
        eeg_outlet = StreamOutlet(eeg_info)

        # Create a time code stream outlet
        time_code_info = StreamInfo('TimeCodeStream', 'TimeCode', 1, 0, 'int32', 'my_time_code_stream')
        time_code_outlet = StreamOutlet(time_code_info)

        tone_frequencies = [200, 400, 600, 800, 1000]  # Frequencies for the tones in Hz
        stim_dur = 0.8  # seconds
        isi = 1.0  # seconds
        n_trials = 40
        n_targets = 8

        # Present the stimuli
        for trial in range(n_trials):
            # Check if stop button is clicked
            if stop_experiment:
                break  # Exit the loop if stop button is pressed

            if trial < n_targets:
                # This is a target trial
                tone_frequency = tone_frequencies[trial % len(tone_frequencies)]
                tone = generate_tone(tone_frequency, stim_dur)
                play_audio(tone)

                # Send time code signal
                time_code_outlet.push_sample([trial])

            else:
                # This is a control trial
                tone = generate_tone(tone_frequencies[0], stim_dur)  # Use the first frequency as control
                play_audio(tone)

            # Send EEG data
            eeg_data = np.random.randn(8)  # Placeholder for EEG data
            eeg_outlet.push_sample(eeg_data)

            # Wait for the duration of the stimulus and ISI
            time.sleep(stim_dur + isi)

if __name__ == "__main__":
    main()
