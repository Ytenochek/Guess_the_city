import sys
from random import choice

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from requests import get

CITIES = [
    "Москва",
    "Пекин",
    "Новосибирск",
    "Чикаго",
    "Филадельфия",
    "Париж",
    "Будапешт",
    "Люксембург",
    "Рига",
]

STATIC_MAPS_URL = "https://static-maps.yandex.ru/1.x/"
SEARCH_URL = "https://search-maps.yandex.ru/v1/"


def spn_counter(sizes):
    return list(map(str, [sizes[1][0] - sizes[0][0], sizes[1][1] - sizes[0][1]]))


class SlideShow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.search_params = {
            "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
            "lang": "ru_RU",
        }
        self.pics = []
        self.find_city()

        self.next_pic()
        self.next.clicked.connect(self.next_pic)

    def next_pic(self):
        self.image.setPixmap(choice(self.pics))

    def find_city(self):
        for city in CITIES:
            self.search_params["text"] = city
            response = get(SEARCH_URL, params=self.search_params)
            data = response.json()

            spn = spn_counter(data["features"][0]["properties"]["boundedBy"])
            points = list(map(str, data["features"][0]["geometry"]["coordinates"]))
            response = get(
                STATIC_MAPS_URL,
                params={"ll": ",".join(points), "spn": ",".join(spn), "l": "sat"},
            )
            qp = QPixmap()
            qp.loadFromData(response.content)
            self.pics.append(qp)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    s = SlideShow()
    s.show()
    sys.exit(app.exec())
