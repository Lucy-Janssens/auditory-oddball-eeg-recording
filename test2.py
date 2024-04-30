import streamlit as st
import numpy as np
import sounddevice as sd
import time


# Function to generate a tone
def generate_tone(frequency, duration, sampling_rate=44100):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    waveform = np.sin(2 * np.pi * frequency * t)
    return waveform


# Function to play audio
def play_audio(data, sampling_rate=44100):
    sd.play(data, samplerate=sampling_rate)
    sd.wait()


# Streamlit app
def main():
    st.title("Auditory Oddball Experiment")
    st.write("Click the button below to start the experiment.")

    if st.button("Start Experiment"):
        tone_frequencies = [200, 400, 600, 800, 1000]  # Frequencies for the tones in Hz
        stim_dur = 0.8  # seconds
        isi = 1.0  # seconds
        n_trials = 40
        n_targets = 8

        # Present the stimuli
        for trial in range(n_trials):
            if trial < n_targets:
                # This is a target trial
                tone_frequency = tone_frequencies[trial % len(tone_frequencies)]
                tone = generate_tone(tone_frequency, stim_dur)
                play_audio(tone)
            else:
                # This is a control trial
                tone = generate_tone(tone_frequencies[0], stim_dur)  # Use the first frequency as control
                play_audio(tone)
            time.sleep(stim_dur + isi)  # wait for the duration of the stimulus and ISI


if __name__ == "__main__":
    main()
