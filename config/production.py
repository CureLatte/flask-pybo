from config.default import *

SQLALCHEMY_DATABSE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'7\xdd\xdb\xf3W\x8b/8\xafh\x00/*\xca\x8f7'


