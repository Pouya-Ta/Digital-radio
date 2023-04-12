import numpy as np
import scipy.signal as sps
import sounddevice as sd

# Define constants
fs = 10e3  # Sampling frequency
f_shift = 5e3  # Desired frequency shift for audio playback
n_samples = 48000  # Number of samples in input file

# Read input signal from file
with open('input.txt', 'r') as f:
    input_signal = np.array([float(line.strip()) for line in f])

# Define radio frequencies and networks
networks = {
    "AWA-96": {"economy": 144e3, "conversation": 288e3, "culture": 240e3},
    "Radio Free Europe": {"news": 144e3, "music": 288e3, "talk": 240e3},
    "Voice of America": {"english": 144e3, "spanish": 288e3, "french": 240e3}
}

while True:
    # Print available radio networks
    print("Available radio networks:")
    for i, network in enumerate(networks):
        print(f"{i+1}. {network}")
    print()

    try:
        # Ask user for radio network selection
        choice = int(input("Enter the number corresponding to the desired radio network or 0 to quit: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    if choice == 0:
        break

    # Check if choice is within valid range
    if not 1 <= choice <= len(networks):
        print(f"Choice must be between 1 and {len(networks)}. Please try again.")
        continue

    # Extract selected network and associated frequencies
    network = list(networks.keys())[choice-1]
    frequencies = networks[network]

    # Print available frequencies for selected network
    print(f"Available frequencies for {network}:")
    for i, freq in enumerate(frequencies):
        print(f"{i+1}. {freq} ({frequencies[freq]/1e3} kHz)")
    print()

    try:
        # Ask user for frequency selection
        freq_choice = int(input("Enter the number corresponding to the desired frequency or 0 to go back: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    if freq_choice == 0:
        continue

    # Check if freq_choice is within valid range
    if not 1 <= freq_choice <= len(frequencies):
        print(f"Choice must be between 1 and {len(frequencies)}. Please try again.")
        continue

    # Extract selected frequency
    freq_pass = frequencies[list(frequencies.keys())[freq_choice-1]]

    # Design low-pass filter to reject frequencies above pass frequency
    f_pass_norm = freq_pass / (fs / 2)
    order = 6  # Filter order
    b, a = sps.butter(order, f_pass_norm)

    # Apply filter to input signal
    filtered_signal = sps.filtfilt(b, a, input_signal)

    # Shift frequency domain to bring signal into hearing range
    t = np.arange(n_samples) / fs
    shift = np.exp(-1j * 2 * np.pi * f_shift * t)
    audio_signal = np.real(shift * filtered_signal)

    # Normalize audio signal and convert to int16 format for playback
    max_value = np.max(np.abs(audio_signal))
    audio_signal_norm = audio_signal / max_value
    audio_signal_int = np.int16(audio_signal_norm * 32767)

    # Play audio signal using sounddevice library
    sd.play(audio_signal_int, fs)

# Clean up resources
sd.stop()
sd.default.device = None
sd.default.dtype = None
sd.default.latency = None
