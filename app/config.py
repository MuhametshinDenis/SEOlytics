import configparser


"""
Класс для загрузки и работы с конфигурационным файлом .ini

Args:
	config (ConfigParse): объект конфигурации

Methods:
	get(key, value): возвращает значения по ключу из секции
	set(key, value): устанавливает значения в секции
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