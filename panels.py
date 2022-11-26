from PyQt5.QtWidgets import QFrame, QPushButton, QVBoxLayout, QFileDialog, QListWidget, QLabel, QHBoxLayout, QSlider
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from win32api import GetSystemMetrics
from circule_list import CirculeList
import subprocess
import os


INITIAL_VOLUME = 20
TRACK_NAME_LABEL_WIDTH = 200
MAIN_WINDOW_HEIGHT_PERCENT = 0.6
SLIDER_WIDTH_PERCENT = 0.3
BUTTON_PLAYER_SIZES = (40, 40)
IMAGE_SIZES = (40, 40)
MILISEC_IN_SEC = 1000
SEC_IN_MIN = 60
VOLUME_RANGE = (0, 100)
VOLUME_SLIDER_WIDTH = 100

metadata_list = CirculeList()


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
        self.player.mediaStatusChanged.connect(self.media_status)
        self.isTrackPlayed = False
        self.isNeedMoved = True

        self.track_name_label = QLabel()
        self.track_name_label.setFixedWidth(TRACK_NAME_LABEL_WIDTH)

        self.time_played_label = QLabel()

        self.volume_label = QLabel()
        volume_img = QPixmap("icons/volume.png")
        volume_img = volume_img.scaled(*IMAGE_SIZES)
        self.volume_label.setPixmap(volume_img)

        self.track_slider = QSlider(Qt.Orientation.Horizontal)
        self.track_slider.setFixedWidth(int(GetSystemMetrics(1) * SLIDER_WIDTH_PERCENT))
        self.track_slider.sliderMoved.connect(self.change_track_position)

        self.prev_track_butt = QPushButton()
        self.prev_track_butt.setFixedSize(*BUTTON_PLAYER_SIZES)
        self.prev_track_butt.setIcon(QIcon("icons/prev.png"))
        self.prev_track_butt.clicked.connect(self.prev)

        self.next_track_butt = QPushButton()
        self.next_track_butt.setFixedSize(*BUTTON_PLAYER_SIZES)
        self.next_track_butt.setIcon(QIcon("icons/next.png"))
        self.next_track_butt.clicked.connect(self.next)

        self.play_butt = QPushButton()
        self.play_butt.setFixedSize(*BUTTON_PLAYER_SIZES)
        self.play_butt.setIcon(QIcon("icons/stop.png"))
        self.play_butt.clicked.connect(self.stop_track)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(*VOLUME_RANGE)
        self.volume_slider.setFixedWidth(VOLUME_SLIDER_WIDTH)
        self.volume_slider.setValue(INITIAL_VOLUME)
        self.volume_slider.sliderMoved.connect(self.set_volume)

        layout = QHBoxLayout(self)
        layout.addWidget(self.track_name_label)
        layout.addWidget(self.prev_track_butt)
        layout.addWidget(self.play_butt)
        layout.addWidget(self.next_track_butt)
        layout.addWidget(self.track_slider)
        layout.addWidget(self.time_played_label)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)

    def media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.next()

    def next(self):
        metadata_list.next()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(metadata_list.curr().data["path"])))
        self.set_data()
        self.player.play()

    def prev(self):
        if self.player.position() // MILISEC_IN_SEC > 3:
            self.player.setPosition(0)
        else:
            metadata_list.prev()
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(metadata_list.curr().data["path"])))
            self.set_data()
            self.player.play()

    def set_data(self):
        self.isTrackPlayed = True
        self.track_name_label.setText(metadata_list.curr().data["name"])
        self.track_slider.setRange(0, metadata_list.curr().data["duration"])
        self.time_played_label.setText("0:00")

    def change_track_position(self, pos):
        self.isNeedMoved = False
        self.track_slider.setValue(pos)
        self.player.setPosition(pos * MILISEC_IN_SEC)
        self.set_time_played(pos * MILISEC_IN_SEC)
        self.isNeedMoved = True

    def change_slider(self, pos):
        if self.isNeedMoved:
            self.track_slider.setValue(pos // MILISEC_IN_SEC)
            self.set_time_played(pos)

    def set_time_played(self, pos):
        min = pos // MILISEC_IN_SEC // 60
        sec = pos // MILISEC_IN_SEC
        if min:
            sec -= min * SEC_IN_MIN
        if sec < 10:
            self.time_played_label.setText(f"{min}:0{sec}")
        else:
            self.time_played_label.setText(f"{min}:{sec}")

    def stop_track(self):
        if self.isTrackPlayed:
            self.player.pause()
            self.play_butt.setIcon(QIcon("icons/play.png"))
            self.isTrackPlayed = False
        else:
            self.player.play()
            self.play_butt.setIcon(QIcon("icons/stop.png"))
            self.isTrackPlayed = True

    def set_volume(self, pos):
        self.player.setVolume(pos)


class TracksPanel(QListWidget):
    def __init__(self, player: QMediaPlayer):
        super().__init__()

        self.player = player
        self.setStyleSheet("border:1px solid rgb(0, 0, 0); ")

        self.list_update()
        self.itemClicked.connect(self.get_item)

    def get_item(self, item):
        while metadata_list.curr() != item.text():
            metadata_list.next()
        data = metadata_list.curr().data
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(data["path"])))
        self.player.play()

    def list_update(self):
        self.clear()
        metadata_list.clear()
        for i in os.walk("./music"):
            if i[0] != "./music":
                continue
            for file in i[2]:
                file = file.rstrip('.mp3')
                self.addItem(file)
                metadata_list.add(file)

