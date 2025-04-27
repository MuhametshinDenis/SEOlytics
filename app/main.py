import json
import os
import subprocess
import time
import schedule

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel, QLineEdit, 
    QHBoxLayout, QRadioButton, QButtonGroup, QProgressBar, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal, QObject

from app.core.analyze_reports import analyze_reports
from app.reports.html_report import generate_html_report
from app.reports.xlsx_report import generate_xlsx_report
from app.utils.logger.application_logger import ApplicationLogger

"""
Класс AnalysisWorker отвечает за выполнение процесса анализа отчета в отдельном потоке.
Он принимает URL, имя файла и формат отчета, затем:
    - запускает внешний процесс через npm
    - анализирует собранные данные
    - формирует итоговый отчет в нужном формате
"""
class AnalysisWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    # Конструктор
    def __init__(self, url, filename, format_report):
        super().__init__()
        self.url = url
        self.filename = filename
        self.format_report = format_report

    # Основной метод выполнения анализа
    def run(self):
        try:
            os.makedirs("reports_output", exist_ok=True)

            self.progress.emit(10)
            command = f"npm start -- {self.url} --filename={self.filename}"
            subprocess.run(command, shell=True, check=True)
            self.progress.emit(50)

            with open(f'./reports_output/{self.filename}.json', 'r', encoding='UTF-8') as file:
                data = json.load(file)

            result = analyze_reports(data)
            self.progress.emit(75)

            if self.format_report == 'Excel':
                generate_xlsx_report(report=result, filename=self.filename)
            elif self.format_report == 'Html':
                generate_html_report(report=result, filename=self.filename)
            elif self.format_report == 'Оба':
                generate_xlsx_report(report=result, filename=self.filename)
                generate_html_report(report=result, filename=self.filename)

            self.progress.emit(100)
        except Exception as e:
            print(f"Ошибка при анализе: {e}")
        finally:
            self.finished.emit()

# Класс основного окна приложения, отвечающего за пользовательский интерфейс и основную логику
class App(QWidget):
    def __init__(self):
        super().__init__()

        self.logger = ApplicationLogger()
        self.init_ui()
        self.init_tray()
        self.schedule_thread = None
        self.schedule_running = False

    # Метод для настройки иконки приложения в системном трее и действий меню
    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("assets/logo.png"))

        tray_menu = QMenu()

        open_action = QAction("Открыть", self)
        open_action.triggered.connect(self.show_window)
        tray_menu.addAction(open_action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.tray_icon.show()

    # Метод для создания и настройки всех элементов пользовательского интерфейса
    def init_ui(self):
        self.setWindowTitle("SEOlytics")
        self.setFixedWidth(500)
        self.setWindowIcon(QIcon("assets/logo.png"))

        layout = QVBoxLayout(self)

        # Режим работы
        layout.addWidget(QLabel("Выберите режим работы программы:", self))
        self.operating_mode = QComboBox(self)
        self.operating_mode.addItems(["Единоразовый", "Регулярный"])
        layout.addWidget(self.operating_mode)

        # URL
        layout.addWidget(QLabel("Введите ссылку:", self))
        self.url_field = QLineEdit(self)
        self.url_field.setPlaceholderText("https://example.com")
        layout.addWidget(self.url_field)

        # Имя файла
        layout.addWidget(QLabel("Введите название файла:", self))
        self.filename_field = QLineEdit(self)
        self.filename_field.setPlaceholderText("Example")
        layout.addWidget(self.filename_field)

        # Период и время
        layout.addWidget(QLabel("Выберите период срабатывания:", self))
        layout_period = QHBoxLayout()

        self.date_field = QLineEdit(self)
        self.date_field.setPlaceholderText("08:00:00")

        self.comboBox_period = QComboBox(self)
        self.comboBox_period.addItems(["Каждый день", "Каждый понедельник", "Каждую среду", "Каждую пятницу"])

        layout_period.addWidget(self.date_field)
        layout_period.addWidget(self.comboBox_period)

        layout.addLayout(layout_period)

        # Формат отчета
        layout.addWidget(QLabel("Выберите формат генерации:", self))
        layout_format = QHBoxLayout()
        self.button_group = QButtonGroup(self)

        excel_radio = QRadioButton("Excel", self)
        html_radio = QRadioButton("Html", self)
        all_radio = QRadioButton("Оба", self)

        self.button_group.addButton(excel_radio)
        self.button_group.addButton(html_radio)
        self.button_group.addButton(all_radio)
        excel_radio.setChecked(True)

        layout_format.addWidget(excel_radio)
        layout_format.addWidget(html_radio)
        layout_format.addWidget(all_radio)

        layout.addLayout(layout_format)

        # Выбранный способ работы
        layout.addWidget(QLabel("Текущий режим работы:", self))
        self.current_mode_label = QLabel("Единоразовый", self)
        layout.addWidget(self.current_mode_label)

        # Обновляем режимы при изменении полей
        self.operating_mode.currentTextChanged.connect(self.update_current_mode_label)
        self.date_field.textChanged.connect(self.update_current_mode_label)
        self.comboBox_period.currentTextChanged.connect(self.update_current_mode_label)

        # Прогресс-бар
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Кнопка запуска
        run_button = QPushButton("Сгенерировать", self)
        run_button.clicked.connect(self.run_analysis)
        layout.addWidget(run_button)

        self.setLayout(layout)

    # Метод обработки клика на кнопку запуска анализа
    def run_analysis(self):
        if self.operating_mode.currentText() == "Единоразовый":
            self.start_analysis()
        else:
            self.start_regular_schedule()

    # Метод для запуска процесса анализа в отдельном потоке
    def start_analysis(self):
        url = self.url_field.text()
        filename = self.filename_field.text()
        format_report = self.button_group.checkedButton().text()

        self.analysis_thread = QThread()
        self.analysis_worker = AnalysisWorker(url, filename, format_report)
        self.analysis_worker.moveToThread(self.analysis_thread)

        self.analysis_thread.started.connect(self.analysis_worker.run)
        self.analysis_worker.finished.connect(self.analysis_thread.quit)
        self.analysis_worker.finished.connect(self.analysis_worker.deleteLater)
        self.analysis_thread.finished.connect(self.analysis_thread.deleteLater)
        self.analysis_worker.progress.connect(self.progress_bar.setValue)

        self.analysis_thread.start()

    # Метод для запуска планировщика задач при регулярном режиме работы
    def start_regular_schedule(self):
        period = self.comboBox_period.currentText()
        time_str = self.date_field.text()
        print("Запущен режим ожидания")

        if self.schedule_thread and self.schedule_thread.isRunning():
            self.schedule_running = False
            self.schedule_thread.quit()
            self.schedule_thread.wait()

        if period == "Каждый день":
            schedule.every().day.at(time_str).do(self.start_analysis)
        elif period == "Каждый понедельник":
            schedule.every().monday.at(time_str).do(self.start_analysis)
        elif period == "Каждую среду":
            schedule.every().wednesday.at(time_str).do(self.start_analysis)
        elif period == "Каждую пятницу":
            schedule.every().friday.at(time_str).do(self.start_analysis)

        self.schedule_running = True
        self.schedule_thread = QThread()
        self.schedule_thread.run = self.run_schedule_loop
        self.schedule_thread.start()

    # Метод выполнения цикла планировщика в отдельном потоке
    def run_schedule_loop(self):
        while self.schedule_running:
            schedule.run_pending()
            time.sleep(1)

    # Переопределенный метод закрытия окна — вместо выхода прячем приложение в трей
    def closeEvent(self, event):
        self.schedule_running = False
        if self.schedule_thread and self.schedule_thread.isRunning():
            self.schedule_thread.quit()
            self.schedule_thread.wait()

        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "SEOlytics свернут",
            "Программа продолжает работать в трее.",
            QSystemTrayIcon.Information,
            3000
        )

    # Метод разворачивания окна приложения при клике на "Открыть"
    def show_window(self):
        self.showNormal()
        self.activateWindow()

    # Метод обработки кликов на иконку в трее
    def on_tray_icon_activated(self, reason):
        if reason is not None and reason == QSystemTrayIcon.Trigger:
            self.show_window()

    # Метод для обновления надписи текущего режима работы на экране
    def update_current_mode_label(self):
        mode = self.operating_mode.currentText()
        if mode == "Единоразовый":
            self.current_mode_label.setText("Единоразовый")
        else:
            time_str = self.date_field.text() or "00:00:00"
            period = self.comboBox_period.currentText()
            self.current_mode_label.setText(f"Регулярный: {period} в {time_str}")
