function generateTone(frequency, duration) {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);
    oscillator.connect(audioCtx.destination);
    oscillator.start();
    setTimeout(() => {
        oscillator.stop();
    }, duration);
}

function startExperiment() {
    const toneFrequencies = [200, 400, 600, 800, 1000];
    const stimDur = 800;  // ms
    const isi = 1000;  // ms
    const nTrials = 40;
    const nTargets = 8;

    // Function to record EEG data
    function recordEegData() {
        // Record EEG data here
    }

    // Present the stimuli
    for (let trial = 0; trial < nTrials; trial++) {
        if (trial < nTargets) {
            // This is a target trial
            const toneFrequency = toneFrequencies[trial % toneFrequencies.length];
            generateTone(toneFrequency, stimDur);
            recordEegData();
        } else {
            // This is a control trial
            generateTone(toneFrequencies[0], stimDur);  // Use the first frequency as control
            recordEegData();
        }
        setTimeout(() => {
            // Wait for the duration of the stimulus and ISI
        }, stimDur + isi);
    }
}
