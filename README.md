# speechToTextTranslation
# Project Structure
#
# translator_app/
# ├── main.py                  # Entry point of the application
# ├── word_bank.py             # Contains the English-Malay word bank
# ├── language_processing/
# │   ├── __init__.py          # Makes the directory a Python package
# │   ├── cfg.py               # Context-Free Grammar implementation
# │   ├── dfa.py               # Deterministic Finite Automaton implementation
# │   └── translator.py        # Translation logic
# └── ui/
#     ├── __init__.py          # Makes the directory a Python package
#     ├── main_window.py       # Main application window
#     └── audio_visualizer.py  # Audio visualizer dialog

# For Windows
pip install pyqt5 pyaudio numpy SpeechRecognition

# For macOS
pip3 install pyqt5 pyaudio numpy SpeechRecognition

# For Linux
sudo apt-get install python3-pyqt5 portaudio19-dev python3-dev
pip3 install pyqt5 pyaudio numpy SpeechRecognition