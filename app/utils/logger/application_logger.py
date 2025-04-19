from datetime import datetime
from colorama import Fore, Style


"""
Класс для логирования сообщений с различными уровнями важности (Info, Success, Debug, Warning).
Сообщения выводятся в консоль с временной меткой и соответствующим цветом для каждого типа сообщения.
	- info(message): Логирует информационное сообщение с синим цветом.
	- success(message): Логирует сообщение об успешной операции с зеленым цветом.
	- debug(message): Логирует сообщение для отладки с пурпурным цветом.
	- warn(message): Логирует предупреждение с красным цветом.
	- formatted_message(message, color, type): Форматирует сообщение с временной меткой и типом, затем выводит его в консоль.
"""
class ApplicationLogger:
	def info(self, message):
		self.formatted_message(message=message, color=Fore.CYAN, type="Info")

	def success(self, message):
		self.formatted_message(message=message, color=Fore.GREEN, type="Success")

	def debug(self, message):
		self.formatted_message(message=message, color=Fore.MAGENTA, type="Debug")

	def warn(self, message):
		self.formatted_message(message=message, color=Fore.RED, type="Warning")

	def formatted_message(self, message, color, type):
		now = datetime.now()
		message = f"[{now.strftime("%Y-%m-%d %H:%M:%S")}] {type} Application {message}"
		print(color + message + Style.RESET_ALL)