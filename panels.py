from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QFileDialog, QListWidget, QLabel, QHBoxLayout, QSlider
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtMultimedia import QMediaPlayer
from win32api import GetSystemMetrics
from circule_list import CirculeList
import subprocess
import os

MAIN_WINDOW_HEIGHT_PERCENT = 0.6
SLIDER_WIDTH_PERCENT = 0.3
BUTTON_PLAYER_SIZES = (40, 40)
METADATA_LIST = CirculeList()


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
        self.player.positionChanged.connect(self.change_slider)
        self.isTrackPlayed = False
        self.isNeedMoved = True

        self.label = QLabel()
        self.test_label = QLabel()

        self.track_slider = QSlider(Qt.Orientation.Horizontal)
        self.track_slider.setFixedWidth(int(GetSystemMetrics(1) * SLIDER_WIDTH_PERCENT))
        self.track_slider.sliderMoved.connect(self.change_track_position)

        self.prev_track_but = QPushButton()
        self.prev_track_but.setFixedSize(*BUTTON_PLAYER_SIZES)
        self.prev_track_but.clicked.connect(self.prev)

        self.next_track_but = QPushButton()
        self.next_track_but.setFixedSize(*BUTTON_PLAYER_SIZES)
        self.next_track_but.clicked.connect(self.next)

        self.play_button = QPushButton()
        self.play_button.setFixedSize(*BUTTON_PLAYER_SIZES)
        self.play_button.setIcon(QIcon("stop.png"))
        self.play_button.clicked.connect(self.stop_track)


        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.prev_track_but)
        layout.addWidget(self.play_button)
        layout.addWidget(self.next_track_but)
        layout.addWidget(self.track_slider)
        layout.addWidget(self.test_label)

    def prev(self):
        if self.player.position() // 1000 > 3:
            self.player.setPosition(0)
        else:
            METADATA_LIST.prev()
            self.player.setSource(QUrl(METADATA_LIST.curr().data["path"]))
            self.change_data()
            self.player.play()

    def next(self):
        METADATA_LIST.next()
        self.player.setSource(QUrl(METADATA_LIST.curr().data["path"]))
        self.change_data()
        self.player.play()

    def change_track_position(self, pos):
        self.isNeedMoved = False
        self.track_slider.setValue(pos)
        self.player.setPosition(pos * 1000)
        self.isNeedMoved = True

    def stop_track(self):
        if self.isTrackPlayed:
            self.player.pause()
            self.play_button.setIcon(QIcon("play.png"))
            self.isTrackPlayed = False
        else:
            self.player.play()
            self.play_button.setIcon(QIcon("stop.png"))
            self.isTrackPlayed = True

    def change_data(self):
        self.isTrackPlayed = True
        self.label.setText(METADATA_LIST.curr().data["name"])
        self.track_slider.setRange(0, METADATA_LIST.curr().data["duration"])

    def change_slider(self, pos):
        if self.isNeedMoved:
            self.track_slider.setValue(pos // 1000)


class TracksPanel(QListWidget):
    def __init__(self, player: QMediaPlayer):
        super().__init__()

        self.player = player
        self.setStyleSheet("border:1px solid rgb(0, 0, 0); ")

        self.list_update()
        self.itemClicked.connect(self.get_item)

    def get_item(self, item):
        while METADATA_LIST.curr() != item.text():
            METADATA_LIST.next()
        data = METADATA_LIST.curr().data
        self.player.setSource(QUrl(data["path"]))
        self.player.play()


    def list_update(self):
        self.clear()
        METADATA_LIST.clear()
        for i in os.walk("./music"):
            if i[0] != "./music":
                continue
            for file in i[2]:
                file = file.rstrip('.mp3')
                self.addItem(file)
                METADATA_LIST.add(file)
        print()

