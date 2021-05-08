import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="migrationserver.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="serveradmin@migrationserver" #TODO: Update value
    POSTGRES_PW="P@ssword"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://migrationproject.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=O7Zj808moifuZeHnuIhLoJMaxPvwtCk5abTv+Xvs/sw=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'srivatsava17@gmail.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = False


class ProductionConfig(BaseConfig):
    DEBUG = True
