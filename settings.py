import os

DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
JWT_SECRET = os.getenv('JWT_TOKEN_SECRET')
JWT_EXPIRY_IN_MIN = int(os.getenv('JWT_EXPIRY', '60'))
JWT_ENCODING_ALGO = 'HS256'
