from datetime import datetime
from colorama import Fore, Style

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