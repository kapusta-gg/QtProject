from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QFileDialog, QListWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon, QImage
from PyQt6.QtMultimedia import QMediaPlayer
from tinytag import TinyTag
from math import floor
import subprocess
import os

MAIN_WINDOW_HEIGHT_PERCENT = 0.6
BUTTON_PLAYER_SIZES = (40, 40)


class LeftPanel(QFrame):
    def __init__(self, tracks_list):
        super().__init__()
        self.setObjectName("left_panel")
        self.setStyleSheet("#left_panel {border:1px solid rgb(0, 0, 0); }")
        self.tracks_list = tracks_list

        folder_button = QPushButton("Открыть папку c музыкой")
        folder_button.clicked.connect(self.open_folder)

        add_button = QPushButton("Добавить музыку")
        add_button.clicked.connect(self.add_music)

        layout = QVBoxLayout(self)
        layout.addWidget(add_button)
        layout.addWidget(folder_button)

    @staticmethod
    def open_folder():
        path = os.path.dirname(os.path.abspath(__file__)) + '\music\\here'
        subprocess.Popen(r'explorer /select,"' + path)

    def add_music(self):
        filename = QFileDialog.getOpenFileName(self, caption="Выберите файл", filter="*.mp3", directory="C:\\")
        try:
            os.replace(filename[0], os.path.dirname(os.path.abspath(__file__)) + '\music\\' + filename[0].split('/')[-1])
        except Exception:
            pass
        self.tracks_list.list_update()


class TrackPlayPanel(QFrame):
    def __init__(self, player: QMediaPlayer):
        super().__init__()
        self.setObjectName("player")
        self.setStyleSheet("#player {border:1px solid rgb(0, 0, 0); }")
        self.player = player
        self.isTrackPlayed = False
        
        self.label = QLabel()

        self.play_button = QPushButton()
        self.play_button.setFixedSize(*BUTTON_PLAYER_SIZES)
        self.play_button.setIcon(QIcon("stop.png"))
        self.play_button.clicked.connect(self.stop_track)


        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.play_button)

    def stop_track(self):
        if self.isTrackPlayed:
            self.player.pause()
            self.play_button.setIcon(QIcon("play.png"))
            self.isTrackPlayed = False
        else:
            self.player.play()
            self.play_button.setIcon(QIcon("stop.png"))
            self.isTrackPlayed = True

    def change_data(self, meta_data):
        self.isTrackPlayed = True
        self.label.setText(meta_data["name"])


class TracksPanel(QListWidget):
    def __init__(self, player: QMediaPlayer):
        super().__init__()

        self.player = player
        self.setStyleSheet("border:1px solid rgb(0, 0, 0); ")

        self.list_update()
        self.itemClicked.connect(self.get_item)

    def get_item(self, item):
        path = os.path.join(".\music", item.text() + ".mp3")

        url = QUrl(path)
        self.player.setSource(url)
        self.player.play()

        data = TinyTag.get(path)
        self.track_metadata = {
            "name": item.text(),
            "duration": floor(data.duration),
        }

    def list_update(self):
        self.clear()
        for i in os.walk("./music"):
            if i[0] != "./music":
                continue
            for file in i[2]:
                self.addItem(file.rstrip('.mp3'))

