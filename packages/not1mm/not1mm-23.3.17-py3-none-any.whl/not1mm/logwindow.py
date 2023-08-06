#!/usr/bin/env python3
"""
Display current log
"""
# pylint: disable=no-name-in-module, unused-import, no-member
# QTableWidget
# focusedLog, generalLog
import logging
import os
import pkgutil
import queue
import socket
import sys
import time
import threading

from json import JSONDecodeError, loads, dumps
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets, uic, Qt
from PyQt5.QtCore import QDir, QItemSelectionModel
from PyQt5.QtGui import QFontDatabase

from not1mm.lib.database import DataBase

# from not1mm.lib.n1mm import N1MM

loader = pkgutil.get_loader("not1mm")
WORKING_PATH = os.path.dirname(loader.get_filename())

if "XDG_DATA_HOME" in os.environ:
    DATA_PATH = os.environ.get("XDG_DATA_HOME")
else:
    DATA_PATH = str(Path.home() / ".local" / "share")
DATA_PATH += "/not1mm"

if "XDG_CONFIG_HOME" in os.environ:
    CONFIG_PATH = os.environ.get("XDG_CONFIG_HOME")
else:
    CONFIG_PATH = str(Path.home() / ".config")
CONFIG_PATH += "/not1mm"

MULTICAST_PORT = 2239
MULTICAST_GROUP = "224.1.1.1"
INTERFACE_IP = "0.0.0.0"
# NODE_RED_SERVER_IP = "127.0.0.1"
# NODE_RED_SERVER_PORT = 12062

# n1mm_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


class MainWindow(QtWidgets.QMainWindow):
    """
    The main window
    """

    # dbname = DATA_PATH + "/ham.db"
    dbname = sys.argv[1] if len(sys.argv) > 1 else DATA_PATH + "/ham.db"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._udpwatch = None
        self.udp_fifo = queue.Queue()
        self.database = DataBase(self.dbname, WORKING_PATH)
        self.contact = self.database.empty_contact
        data_path = WORKING_PATH + "/data/logwindow.ui"
        uic.loadUi(data_path, self)
        self.generalLog.setColumnCount(11)
        icon_path = WORKING_PATH + "/data/"
        self.checkmark = QtGui.QPixmap(icon_path + "check.png")
        self.checkicon = QtGui.QIcon()
        self.checkicon.addPixmap(self.checkmark)
        self.generalLog.setHorizontalHeaderItem(
            0, QtWidgets.QTableWidgetItem("YYYY-MM-DD HH:MM:SS")
        )
        self.generalLog.verticalHeader().setVisible(False)
        self.generalLog.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Call"))
        self.generalLog.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Freq"))
        self.generalLog.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Snt"))
        self.generalLog.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("Rcv"))
        self.generalLog.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem("M1"))
        self.generalLog.setHorizontalHeaderItem(6, QtWidgets.QTableWidgetItem("ZN"))
        self.generalLog.setHorizontalHeaderItem(7, QtWidgets.QTableWidgetItem("M2"))
        self.generalLog.setHorizontalHeaderItem(8, QtWidgets.QTableWidgetItem("PFX"))
        self.generalLog.setHorizontalHeaderItem(9, QtWidgets.QTableWidgetItem("PTS"))
        self.generalLog.setHorizontalHeaderItem(10, QtWidgets.QTableWidgetItem("UUID"))
        self.generalLog.setColumnWidth(0, 200)
        self.generalLog.setColumnWidth(3, 50)
        self.generalLog.setColumnWidth(4, 50)
        self.generalLog.setColumnWidth(5, 25)
        self.generalLog.setColumnWidth(6, 50)
        self.generalLog.setColumnWidth(7, 25)
        self.generalLog.setColumnWidth(8, 50)
        self.generalLog.setColumnWidth(9, 50)
        self.generalLog.cellDoubleClicked.connect(self.double_clicked)
        self.generalLog.cellChanged.connect(self.cell_changed)
        self.generalLog.setColumnHidden(10, True)
        self.get_log()
        self.multicast_port = 2239
        self.multicast_group = "224.1.1.1"
        self.interface_ip = "0.0.0.0"
        self.server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_udp.bind(("", int(self.multicast_port)))
        mreq = socket.inet_aton(self.multicast_group) + socket.inet_aton(
            self.interface_ip
        )
        self.server_udp.setsockopt(
            socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, bytes(mreq)
        )
        self.server_udp.settimeout(0.01)
        if self._udpwatch is None:
            self._udpwatch = threading.Thread(
                target=self.watch_udp,
                daemon=True,
            )
            self._udpwatch.start()
        # self.n1mm = N1MM(
        #     ip_address=self.preference.get("n1mm_ip"),
        #     radioport=self.preference.get("n1mm_radioport"),
        #     contactport=self.preference.get("n1mm_contactport"),
        # )

    def double_clicked(self, _row, _column):
        """Slot for doubleclick event"""
        if self.table_loading:
            return
        logger.debug("DoubleClicked")

    def cell_changed(self, row, column):
        """Slot for changed cell"""
        if self.table_loading:
            return
        db_record = {
            "TS": self.generalLog.item(row, 0).text(),
            "Call": self.generalLog.item(row, 1).text().upper(),
            "Freq": self.generalLog.item(row, 2).text(),
            "SNT": self.generalLog.item(row, 3).text(),
            "RCV": self.generalLog.item(row, 4).text(),
            "ZN": self.generalLog.item(row, 6).text(),
            "WPXPrefix": self.generalLog.item(row, 8).text().upper(),
            "Points": self.generalLog.item(row, 9).text(),
            "ID": self.generalLog.item(row, 10).text(),
        }
        self.database.change_contact(db_record)
        self.get_log()
        self.generalLog.scrollToItem(self.generalLog.item(row, column))

    def dummy(self):
        """the dummy"""
        ...

    def get_log(self):
        """Get Log, Show it."""
        self.generalLog.cellChanged.connect(self.dummy)
        self.table_loading = True
        current_log = self.database.fetch_all_contacts_asc()
        self.generalLog.setRowCount(0)
        for log_item in current_log:
            number_of_rows = self.generalLog.rowCount()
            self.generalLog.insertRow(number_of_rows)
            time_stamp = log_item.get("TS", "YY-MM-DD HH:MM:SS")
            first_item = QtWidgets.QTableWidgetItem(time_stamp)
            self.generalLog.setItem(number_of_rows, 0, first_item)
            self.generalLog.setCurrentItem(first_item, QItemSelectionModel.NoUpdate)
            self.generalLog.item(number_of_rows, 0).setTextAlignment(0x0004)
            self.generalLog.setItem(
                number_of_rows,
                1,
                QtWidgets.QTableWidgetItem(str(log_item.get("Call", ""))),
            )
            freq = log_item.get("Freq", "")
            self.generalLog.setItem(
                number_of_rows,
                2,
                QtWidgets.QTableWidgetItem(str(round(float(freq), 2))),
            )
            self.generalLog.setItem(
                number_of_rows,
                3,
                QtWidgets.QTableWidgetItem(str(log_item.get("SNT", ""))),
            )
            self.generalLog.setItem(
                number_of_rows,
                4,
                QtWidgets.QTableWidgetItem(str(log_item.get("RCV", ""))),
            )
            item = QtWidgets.QTableWidgetItem()
            if log_item.get("IsMultiplier1", False):
                item.setIcon(self.checkicon)
            self.generalLog.setItem(
                number_of_rows,
                5,
                item,
            )
            self.generalLog.setItem(
                number_of_rows,
                6,
                QtWidgets.QTableWidgetItem(str(log_item.get("ZN", ""))),
            )
            item = QtWidgets.QTableWidgetItem()
            if log_item.get("IsMultiplier2", False):
                item.setIcon(self.checkicon)
            self.generalLog.setItem(
                number_of_rows,
                7,
                item,
            )
            self.generalLog.setItem(
                number_of_rows,
                8,
                QtWidgets.QTableWidgetItem(str(log_item.get("WPXPrefix", ""))),
            )
            self.generalLog.setItem(
                number_of_rows,
                9,
                QtWidgets.QTableWidgetItem(str(log_item.get("Points", ""))),
            )
            self.generalLog.setItem(
                number_of_rows,
                10,
                QtWidgets.QTableWidgetItem(str(log_item.get("ID", ""))),
            )
        self.table_loading = False
        self.generalLog.cellChanged.connect(self.cell_changed)

    def watch_udp(self):
        """Puts UDP datagrams in a FIFO queue"""
        while True:
            try:
                datagram = self.server_udp.recv(1500)
                logger.debug(datagram.decode())
            except socket.timeout:
                time.sleep(1)
                continue
            if datagram:
                self.udp_fifo.put(datagram)

    def check_udp_traffic(self):
        """Checks UDP Traffic"""
        while not self.udp_fifo.empty():
            datagram = self.udp_fifo.get()
            try:
                debug_info = f"*************\n{datagram.decode()}\n********************"
                logger.debug(debug_info)
                json_data = loads(datagram.decode())
            except UnicodeDecodeError as err:
                the_error = f"Not Unicode: {err}\n{datagram}"
                logger.debug(the_error)
                continue
            except JSONDecodeError as err:
                the_error = f"Not JSON: {err}\n{datagram}"
                logger.debug(the_error)
                continue
            if json_data.get("cmd") == "UPDATELOG":
                logger.debug("External refresh command.")
                self.get_log()


def load_fonts_from_dir(directory: str) -> set:
    """
    Well it loads fonts from a directory...
    """
    font_families = set()
    for _fi in QDir(directory).entryInfoList(["*.ttf", "*.woff", "*.woff2"]):
        _id = QFontDatabase.addApplicationFont(_fi.absoluteFilePath())
        font_families |= set(QFontDatabase.applicationFontFamilies(_id))
    return font_families


def main():
    """main entry"""
    timer.start(1000)
    sys.exit(app.exec())


logger = logging.getLogger("__main__")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    datefmt="%H:%M:%S",
    fmt="[%(asctime)s] %(levelname)s %(module)s - %(funcName)s Line %(lineno)d:\n%(message)s",
)
handler.setFormatter(formatter)
logger.addHandler(handler)

if Path("./debug").exists():
    logger.setLevel(logging.DEBUG)
    logger.debug("debugging on")
else:
    logger.setLevel(logging.WARNING)
    logger.warning("debugging off")

app = QtWidgets.QApplication(sys.argv)
font_path = WORKING_PATH + "/data"
_families = load_fonts_from_dir(os.fspath(font_path))
window = MainWindow()
window.setWindowTitle("Log Display")
window.show()
timer = QtCore.QTimer()
timer.timeout.connect(window.check_udp_traffic)

if __name__ == "__main__":
    main()
