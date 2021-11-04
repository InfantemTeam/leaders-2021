import os.path

CATEGORIES = (
	'Художественная литература',
	'Зарубежный детектив',
	'Проза',
	'Фантастика',
	'Технология общественного питания. Кулинария',
	'Литература для детей и юношества',
	'Сказки для детей и юношества',
	'Исторический любовный роман',
	'Фэнтэзи',
)

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(os.path.dirname(__file__), 'db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False

JSON_AS_ASCII = False

SECRET_KEY = 'l34d3r5_d3v_53cr37'

VK_SECRET = "YVeVC2D5G4Hd9fx8Dwhn"
TELEGRAM_TOKEN = "2051141677:AAGm2A1IWiqJJw8tw4WZ63bnYR5YxlDH5wM"
