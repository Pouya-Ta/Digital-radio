import numpy as np
import scipy.signal as sps
import sounddevice as sd

# Define constants
fs = 10e3  # Sampling frequency
f_shift = 5e3  # Desired frequency shift for audio playback
n_samples = 48000  # Number of samples in input file

def read_input_signal(file_path):
    """Reads the input signal from a file."""
    try:
        with open(file_path, 'r') as f:
            input_signal = np.array([float(line.strip()) for line in f])
        return input_signal
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        exit(1)
    except ValueError:
        print("Error: Invalid data in the input file.")
        exit(1)

def design_filter(freq_pass, fs):
    """Designs a low-pass filter with the given pass frequency."""
    f_pass_norm = freq_pass / (fs / 2)
    order = 6  # Filter order
    b, a = sps.butter(order, f_pass_norm)
    return b, a

def apply_filter(input_signal, b, a):
    """Applies the low-pass filter to the input signal."""
    return sps.filtfilt(b, a, input_signal)

def shift_frequency(filtered_signal, f_shift, n_samples, fs):
    """Shifts the filtered signal to the desired frequency range."""
    t = np.arange(n_samples) / fs
    shift = np.exp(-1j * 2 * np.pi * f_shift * t)
    return np.real(shift * filtered_signal)

def normalize_signal(audio_signal):
    """Normalizes the audio signal and converts it to int16 format."""
    max_value = np.max(np.abs(audio_signal))
    audio_signal_norm = audio_signal / max_value
    return np.int16(audio_signal_norm * 32767)

def play_audio(audio_signal, fs):
    """Plays the audio signal using sounddevice library."""
    sd.play(audio_signal, fs)

def stop_audio():
    """Stops the audio playback."""
    sd.stop()

def main():
    # Read input signal from file
    input_signal = read_input_signal('input.txt')

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
            stop_audio()
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

        # Design and apply filter
        b, a = design_filter(freq_pass, fs)
        filtered_signal = apply_filter(input_signal, b, a)

        # Shift frequency and play audio
        audio_signal = shift_frequency(filtered_signal, f_shift, n_samples, fs)
        audio_signal_int = normalize_signal(audio_signal)
        play_audio(audio_signal_int, fs)

if __name__ == "__main__":
    main()
