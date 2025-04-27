import sys
from app.main import App
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = App()
	window.show()
	sys.exit(app.exec_())