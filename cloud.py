from webdav3.client import Client
from dotenv import load_dotenv
load_dotenv()

data = {
 'webdav_hostname': "https://webdav.cloud.mail.ru",
 'webdav_login':    f"{os.getenv('MAILRU_LOGIN')}@mail.ru",
 'webdav_password': os.getenv('MAILRU_CLOUD_PASSWORD')
}
client = Client(data)

my_files = client.list()
print(my_files)
