# Whisper-Dictation
Done as part of the CSI5180[W] Virtual Assistants 20241 course.

This is a Python script that utilizes a fast-whisper model for real-time speech recognition and converts it into text. The recognized text is then used to simulate keyboard typing.

## Requirements

- Python 3.x
- PyTorch
- NumPy
- SpeechRecognition
- pynput
- faster_whisper (included in this repository)

## Installation

1. Clone or download this repository to your local machine.
2. Install the required dependencies using pip:
`pip install torch numpy SpeechRecognition pynput`

## How it WOrks

### Audio Handling
1. It sets up a queue (`audio_queue`) to hold audio data.
2. Initializes a `Recognizer` object from `speech_recognition` library for recording audio.
3. Adjusts the energy threshold and dynamic energy threshold for recording.
4. Configures a microphone as the audio source and adjusts for ambient noise.

### Recording
1. Defines functions to handle pushing and popping audio data to and from the queue.
2. Listens in the background for audio input and pushes it to the queue.
3. This enables continuous recording of audio in the background.

### Audio Processing Loop
1. Continuously pops audio data from the queue.
2. Calculates the loudness of the audio frame.
3. If the loudness is below a certain threshold (`hallucinate_threshold`), it skips the current iteration.
4. Otherwise, it flattens and converts the audio frame to float32 format.
5. Uses the initialized speech recognition model to transcribe the audio data into segments.
6. Concatenates the text from the segments.
7. If there is transcribed text, it types it using keyboard inputs.

### Endless Loop
The code runs in an infinite loop, continuously listening for audio input and transcribing it to text.


## Usage

1. Run the script by executing `python whisper_typing_assistant.py` in your terminal.
2. Speak into your microphone. The script will recognize your speech and type the corresponding text.

### Customization

- You can adjust the `hallucinate_threshold` variable to change the sensitivity of speech detection.
- The `phrase_time_limit` parameter in `recorder.listen_in_background` sets the maximum time for a phrase to be recorded. You can adjust this as needed.
- Modify the `model_root` variable to change the directory where the Whisper model will be stored.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
