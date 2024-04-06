import sys
from multiprocessing import Process

import requests
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication


class MyBrowserWindow(QWebEngineView):
    def closeEvent(self, event):
        response = requests.get(f"http://127.0.0.1:{self.port}/close")
        super().closeEvent(event)


class BrowerProcess(Process):
    def __init__(self, port, name=None):
        super(BrowerProcess, self).__init__(name=name)
        self.port = port

    def run(self):
        print('%s多进程' % self.name)
        self.start_process()

    def start_process(self):
        app = QApplication(sys.argv)
        view = MyBrowserWindow()
        view.port = self.port
        view.setWindowTitle("海棠叶")
        port = int(self.port)
        # 加载空白页面
        view.setHtml('')
        view.load(QUrl(f"http://127.0.0.1:{port}/"))
        view.show()
        sys.exit(app.exec())
