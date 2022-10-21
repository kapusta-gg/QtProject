from math import floor
from tinytag import TinyTag
import os


class Node:
    def __init__(self, music_name):
        path = os.path.join(".\music", music_name + ".mp3")
        data = TinyTag.get(path)
        self.data = {"name": music_name,
                     "path": path,
                     "duration": floor(data.duration)}
        self.next = None
        self.prev = None

    def __eq__(self, other):
        return self.data["name"] == other

    def __ne__(self, other):
        return self.data["name"] != other


class CirculeList:
    def __init__(self):
        self.head = self.tail = self.__current = None

    def add(self, music_name):
        node = Node(music_name)
        if self.head is None:
            self.head = self.tail = node
            self.head.next = self.head.prev = self.tail
            self.tail.next = self.tail.prev = self.head
            self.__current = node
        else:
            self.tail.next = node
            self.head.prev = node
            node.next = self.head
            node.prev = self.tail
            self.tail = node

    def clear(self):
        self.head = self.tail = self.__current = None

    def prev(self):
        self.__current = self.__current.prev
        #return self.__current.data

    def next(self):
        self.__current = self.__current.next
        #return self.__current.data

    def curr(self):
        return self.__current

