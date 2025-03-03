import numpy as np
import pyaudio
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QTimer

class AudioVisualizerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Audio Visualizer")
        self.setFixedSize(500, 300)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        
        # Set up the UI
        self.setup_ui()
        
        # Audio data
        self.audio_data = np.zeros(128)
        
        # Start the visualizer timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_visualizer)
        self.timer.start(30)  # 30ms refresh rate
        
        # Setup for audio capture
        self.is_listening = False
        self.stream = None
        self.p = pyaudio.PyAudio()
    
    def update_visualizer(self):
        self.update()  # Triggers repaint to show updated data

        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Status label
        self.status_label = QLabel("Getting ready...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setStyleSheet("color: #333; margin: 10px;")
        layout.addWidget(self.status_label)
        
        # Visualizer frame
        self.visualizer_frame = QFrame()
        self.visualizer_frame.setFrameShape(QFrame.StyledPanel)
        self.visualizer_frame.setStyleSheet("background-color: #1a1a1a; border-radius: 8px;")
        self.visualizer_frame.setMinimumHeight(180)
        layout.addWidget(self.visualizer_frame)
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.close_button.clicked.connect(self.stop_listening)
        self.close_button.clicked.connect(self.close)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def start_listening(self):
        self.is_listening = True
        self.status_label.setText("Listening... Speak something in English")
        self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold; margin: 10px;")
        
        # Start audio stream
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
            stream_callback=self.audio_callback
        )
        self.stream.start_stream()
        
    def stop_listening(self):
        self.is_listening = False
        self.status_label.setText("Stopped listening")
        self.status_label.setStyleSheet("color: #e74c3c; margin: 10px;")
        
        # Stop audio stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
    def audio_callback(self, in_data, frame_count, time_info, status):
        # Convert audio data to numpy array
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        
        # Get the magnitude of the audio data
        magnitude = np.abs(audio_data)
        
        # Normalize and scale for visualization
        magnitude = magnitude * 500
        
        # Downsample to 128 points (for visualization)
        if len(magnitude) >= 128:
            self.audio_data = magnitude[:128]
        else:
            # Pad with zeros if not enough data
            self.audio_data = np.pad(magnitude, (0, 128 - len(magnitude)), 'constant')
                    
        return (in_data, pyaudio.paContinue)
    
    def paintEvent(self, event):
        if not self.is_listening:
            # Just call the base class implementation if not listening
            super().paintEvent(event)
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get the geometry of the visualizer frame
        rect = self.visualizer_frame.geometry()
        
        # Draw on the visualizer frame
        painter.fillRect(rect, QColor('#1a1a1a'))
        
        # Number of bars in the visualizer
        num_bars = min(64, len(self.audio_data))
        
        # Calculate bar width
        bar_width = rect.width() / num_bars
        
        # Draw each bar
        for i in range(num_bars):
            # Calculate bar height (clamped to maximum height)
            height = min(self.audio_data[i] * rect.height() / 100, rect.height())
            
            # Calculate color based on height (green to red gradient)
            r = min(255, int(height * 2.55))
            g = min(255, int(255 - height * 1.2))
            b = 100
            
            # Set the pen color
            pen = QPen(QColor(r, g, b))
            pen.setWidth(int(bar_width * 0.8))
            painter.setPen(pen)
            
            # Calculate x position
            x = rect.left() + i * bar_width + bar_width / 2
            
            # Draw the bar
            y_start = rect.bottom() - height
            painter.drawLine(int(x), int(rect.bottom()), int(x), int(y_start))
    
    def closeEvent(self, event):
        self.stop_listening()
        event.accept()