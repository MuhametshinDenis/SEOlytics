import configparser


"""
Класс для работы с конфигурационным файлом (по умолчанию "config.ini").
Позволяет читать, изменять и сохранять параметры конфигурации.
	- get(section, key): Возвращает значение параметра по секции и ключу, или None, если параметр не найден.
	- set(section, key, value): Устанавливает значение для указанного ключа в указанной секции.
	- save(): Сохраняет изменения обратно в конфигурационный файл.
"""
class ApplicationConfig:
	def __init__(self, config_path = "config.ini"):
		self.config_path = config_path
		self.config = configparser.ConfigParser()
		self.config.read(self.config_path, encoding="UTF-8")

	def get(self, section, key):
		if not self.config.has_option(section, key):
			return None

		return self.config.get(section, key)
	
	def set(self, section, key, value):
		self.config.set(section, key, value=value)

	def save(self):
		with open(self.config_path, 'w', encoding="UTF-8") as config_file:
			self.config.write(config_file)