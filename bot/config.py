import os

VK_SECRET_KEY = os.environ.get('SECRET_KEY')
VK_CONFIRMATION_KEY = os.environ.get('CONFIRMATION_KEY')
VK_GROUP_ID = int(os.environ.get('GROUP_ID'))
VK_GROUP_TOKEN = os.environ.get('GROUP_TOKEN')

OPBEAT_ORGANIZATION_ID = os.environ.get('OPBEAT_ORGANIZATION_ID')
OPBEAT_APP_ID = os.environ.get('OPBEAT_APP_ID')
OPBEAT_SECRET_TOKEN = os.environ.get('OPBEAT_SECRET_TOKEN')
