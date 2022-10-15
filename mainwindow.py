from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QVBoxLayout
from PyQt6.QtCore import QSize
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from panels import LeftPanel, TrackPlayPanel, TracksPanel
from win32api import GetSystemMetrics


MAIN_WINDOW_HEIGHT_PERCENT = 0.6
MAIN_WINDOW_WIDTH_PERCENT = 0.6


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(int(GetSystemMetrics(0) * MAIN_WINDOW_HEIGHT_PERCENT), int(GetSystemMetrics(1) * MAIN_WINDOW_WIDTH_PERCENT)))
        self.setWindowTitle("QtPlayer")

        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.tracksChanged.connect(self.change_data)

        self.tracks_panel = TracksPanel(self.player)
        self.left_panel = LeftPanel(self.tracks_panel)
        self.left_panel.setFixedWidth(int(self.width()*0.2))
        self.play_panel = TrackPlayPanel(self.player)
        self.play_panel.setFixedHeight(int(self.width()*0.05))

        self.left_layout = QHBoxLayout()
        self.left_layout.addWidget(self.left_panel)

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.tracks_panel)
        self.right_layout.addWidget(self.play_panel)
        self.temp2 = QWidget()
        self.temp2.setLayout(self.right_layout)

        self.left_layout.addWidget(self.temp2)

        self.temp = QWidget()
        self.temp.setLayout(self.left_layout)
        self.setCentralWidget(self.temp)

    def change_data(self):
        self.play_panel.change_data(self.tracks_panel.track_metadata)