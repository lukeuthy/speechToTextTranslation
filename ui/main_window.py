import threading
import speech_recognition as sr
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
                            QWidget, QTextEdit, QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

from language_processing.translator import translate_to_malay, analyze_text
from ui.audio_visualizer import AudioVisualizerDialog

class TranslatorApp(QMainWindow):
    update_translation_signal = pyqtSignal(str, str, dict)
    
    def __init__(self):
        super().__init__()
        
        # Set up window properties
        self.setWindowTitle("English-Malay Translator")
        self.setMinimumSize(800, 600)
        
        # Initialize the UI components
        self.setup_ui()
        
        # Initialize the recognizer
        self.recognizer = sr.Recognizer()
        
        # Initialize audio visualizer dialog
        self.audio_dialog = None
        
        # Connect signal
        self.update_translation_signal.connect(self.update_translation)
        
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("English-Malay Translator")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Speak English and get Malay translations")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        main_layout.addWidget(subtitle_label)
        
        # English section
        english_label = QLabel("English:")
        english_label.setFont(QFont("Arial", 12, QFont.Bold))
        english_label.setStyleSheet("color: #2980b9;")
        main_layout.addWidget(english_label)
        
        self.english_text = QTextEdit()
        self.english_text.setFont(QFont("Arial", 12))
        self.english_text.setStyleSheet("""
            QTextEdit {
                background-color: #ecf0f1;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                color: #2c3e50;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.english_text.setPlaceholderText("Your English text will appear here...")
        self.english_text.setMinimumHeight(120)
        main_layout.addWidget(self.english_text)
        
        # Malay section
        malay_label = QLabel("Malay Translation:")
        malay_label.setFont(QFont("Arial", 12, QFont.Bold))
        malay_label.setStyleSheet("color: #16a085;")
        main_layout.addWidget(malay_label)
        
        self.malay_text = QTextEdit()
        self.malay_text.setFont(QFont("Arial", 12))
        self.malay_text.setReadOnly(True)
        self.malay_text.setStyleSheet("""
            QTextEdit {
                background-color: #e8f8f5;
                border: 2px solid #a3e4d7;
                border-radius: 8px;
                padding: 10px;
                color: #16a085;
            }
        """)
        self.malay_text.setPlaceholderText("Malay translation will appear here...")
        self.malay_text.setMinimumHeight(120)
        main_layout.addWidget(self.malay_text)
        
        # Analysis section
        analysis_label = QLabel("Linguistic Analysis:")
        analysis_label.setFont(QFont("Arial", 12, QFont.Bold))
        analysis_label.setStyleSheet("color: #8e44ad;")
        main_layout.addWidget(analysis_label)
        
        self.analysis_text = QTextEdit()
        self.analysis_text.setFont(QFont("Arial", 11))
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5eef8;
                border: 2px solid #d7bde2;
                border-radius: 8px;
                padding: 10px;
                color: #8e44ad;
            }
        """)
        self.analysis_text.setPlaceholderText("Linguistic analysis will appear here...")
        self.analysis_text.setMinimumHeight(120)
        main_layout.addWidget(self.analysis_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Translate button
        self.manual_translate_btn = QPushButton("Translate Text")
        self.manual_translate_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.manual_translate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 6px;
                padding: 12px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        self.manual_translate_btn.clicked.connect(self.on_manual_translate)
        button_layout.addWidget(self.manual_translate_btn)
        
        # Speech to text button
        self.speech_btn = QPushButton("Start Speech Recognition")
        self.speech_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.speech_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 6px;
                padding: 12px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.speech_btn.clicked.connect(self.on_speech_recognition)
        button_layout.addWidget(self.speech_btn)
        
        # Clear button
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 6px;
                padding: 12px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a33025;
            }
        """)
        self.clear_btn.clicked.connect(self.on_clear)
        button_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("color: #7f8c8d; margin-top: 10px;")
        main_layout.addWidget(self.status_label)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def on_manual_translate(self):
        english_text = self.english_text.toPlainText()
        if not english_text:
            self.status_label.setText("Please enter some English text first")
            self.status_label.setStyleSheet("color: #e74c3c;")
            return
            
        # Translate
        malay_translation = translate_to_malay(english_text)
        
        # Update analysis
        analysis_dict = analyze_text(english_text)
        
        # Update UI
        self.update_translation(english_text, malay_translation, analysis_dict)
        self.status_label.setText("Translation completed")
        self.status_label.setStyleSheet("color: #27ae60;")
    
    def on_speech_recognition(self):
        # Create and show audio visualizer dialog
        if not self.audio_dialog:
            self.audio_dialog = AudioVisualizerDialog(self)
        
        self.audio_dialog.show()
        self.audio_dialog.start_listening()
        
        # Update status
        self.status_label.setText("Listening for speech...")
        self.status_label.setStyleSheet("color: #2ecc71;")
        
        # Start recognition in a separate thread
        threading.Thread(target=self.recognize_speech, daemon=True).start()
    
    def recognize_speech(self):
        try:
            # Use the microphone as source for input
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for the user's input
                audio = self.recognizer.listen(source)
                
                # Stop visualizer's listening status
                if self.audio_dialog and self.audio_dialog.isVisible():
                    self.audio_dialog.status_label.setText("Processing speech...")
                
                try:
                    # Using Google Speech Recognition to convert audio to text
                    english_text = self.recognizer.recognize_google(audio)
                    
                    # Translate the English text to Malay
                    malay_translation = translate_to_malay(english_text)
                    
                    # Generate analysis
                    analysis_dict = analyze_text(english_text)
                    
                    # Update UI using signal (thread-safe)
                    self.update_translation_signal.emit(english_text, malay_translation, analysis_dict)
                    
                except sr.UnknownValueError:
                    self.update_translation_signal.emit("", "", {})
                    # Update status
                    self.status_label.setText("Could not understand audio")
                    self.status_label.setStyleSheet("color: #e74c3c;")
                    
                except sr.RequestError:
                    self.update_translation_signal.emit("", "", {})
                    # Update status
                    self.status_label.setText("Could not request results; check your internet connection")
                    self.status_label.setStyleSheet("color: #e74c3c;")
                    
        finally:
            # Close audio dialog when finished
            if self.audio_dialog and self.audio_dialog.isVisible():
                self.audio_dialog.stop_listening()
    
    def update_translation(self, english_text, malay_translation, analysis_dict):
        # Update text fields
        self.english_text.setText(english_text)
        self.malay_text.setText(malay_translation)
        
        # Update analysis field
        if analysis_dict:
            analysis_html = f"""
                <b>Tokens:</b> {', '.join(analysis_dict.get('tokens', []))}
                <br><br>
                <b>Sentence structure:</b> {', '.join(analysis_dict.get('structure', []))}
                <br><br>
                <b>Sentence type:</b> {analysis_dict.get('type', 'unknown')}
                <br><br>
                <b>DFA validation:</b> {'Valid' if analysis_dict.get('valid', False) else 'Invalid'}
            """
            self.analysis_text.setHtml(analysis_html)
        else:
            self.analysis_text.clear()
            
        # Update status
        if english_text and malay_translation:
            self.status_label.setText("Translation completed")
            self.status_label.setStyleSheet("color: #27ae60;")
    
    def on_clear(self):
        self.english_text.clear()
        self.malay_text.clear()
        self.analysis_text.clear()
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("color: #7f8c8d;")
    
    def closeEvent(self, event):
        # Close audio dialog when main window is closed
        if self.audio_dialog:
            self.audio_dialog.close()
        event.accept()