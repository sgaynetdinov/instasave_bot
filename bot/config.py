import os

SECRET_KEY = os.environ.get('SECRET_KEY')
CONFIRMATION_KEY = os.environ.get('CONFIRMATION_KEY')
GROUP_ID = int(os.environ.get('GROUP_ID'))
GROUP_TOKEN = os.environ.get('GROUP_TOKEN')
BOTAN_TOKEN = os.environ.get('BOTAN_TOKEN')
