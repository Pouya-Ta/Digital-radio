# Digital Radio Tuner

`digital_radio.py` is a Python script that emulates a digital radio tuner, allowing users to select from various radio networks and frequencies to listen to audio broadcasts. The script reads an input signal from a file, filters the signal based on the selected frequency, and plays the audio using the `sounddevice` library.

## Features

- **User Interface**: Command-line interface for selecting radio networks and frequencies.
- **Signal Processing**: Uses `scipy` for designing and applying a low-pass filter to the input signal.
- **Frequency Shifting**: Shifts the filtered signal to a desired frequency range for audio playback.
- **Audio Playback**: Plays the processed audio signal using the `sounddevice` library.
- **Error Handling**: Handles file reading errors and invalid user inputs gracefully.
- **Modular Code**: Organized into functions for better readability and maintainability.

## Radio Networks and Frequencies

The script supports the following radio networks and frequencies:

- **AWA-96**
  - Economy: 144 kHz
  - Conversation: 288 kHz
  - Culture: 240 kHz
- **Radio Free Europe**
  - News: 144 kHz
  - Music: 288 kHz
  - Talk: 240 kHz
- **Voice of America**
  - English: 144 kHz
  - Spanish: 288 kHz
  - French: 240 kHz

## How It Works

1. **Reading the Input Signal**: The script reads the input signal from a text file (`input.txt`). Error handling ensures the program exits gracefully if the file is not found or contains invalid data.
2. **Selecting a Network and Frequency**: The user selects a radio network and frequency from the available options presented in a command-line interface.
3. **Filtering the Signal**: The script designs a low-pass filter based on the selected frequency and applies it to the input signal.
4. **Frequency Shifting**: The filtered signal is shifted in the frequency domain to bring it into the hearing range.
5. **Normalizing and Playing the Audio**: The shifted signal is normalized, converted to `int16` format, and played using the `sounddevice` library. The playback stops when the user exits the program.

## Usage

1. Ensure you have the required libraries installed:
    ```bash
    pip install numpy scipy sounddevice
    ```
2. Create an `input.txt` file containing the input signal data.
3. Run the script:
    ```bash
    python digital_radio.py
    ```
4. Follow the prompts to select a radio network and frequency.

## Example

Here is a brief example of how the script can be used:

```bash
$ python digital_radio.py
Available radio networks:
1. AWA-96
2. Radio Free Europe
3. Voice of America

Enter the number corresponding to the desired radio network or 0 to quit: 1
Available frequencies for AWA-96:
1. economy (144.0 kHz)
2. conversation (288.0 kHz)
3. culture (240.0 kHz)

Enter the number corresponding to the desired frequency or 0 to go back: 2
```


