import paramiko
import psycopg2
from config import Config
cfg = Config()

class Database: 
	def __init__(self):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(cfg.host, port=cfg.port, username=cfg.username, password=cfg.passw)

			print("A connection to the server has been established")
			self.conn = psycopg2.connect(
  			database = cfg.database,
			user = cfg.user_data,
			password = cfg.password_data,
			host = cfg.host_data,
			port = cfg.port_data
			)
			print ("Database connection established")
		except Exception as err:
			print(str(err))

	async def add_user(self, user_id: int):
		with self.conn.cursor() as cursor:
			cursor.execute("""INSERT INTO forum_user (telegr_id) VALUES (%s);""", (user_id, ))
		self.conn.commit()

	async def update_user_data(self, user_id: int, user_name: str, password: str, image: memoryview):
		with self.conn.cursor() as cursor:
			cursor.execute("""UPDATE forum_user SET user_name = %s, passw = %s, image = %s WHERE telegr_id = %s;""", (user_name, password, image, user_id, ))
		self.conn.commit()

	async def check_user(self, user_id: int):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT EXISTS(SELECT id FROM forum_user WHERE telegr_id = %s);""", (user_id, ))
			return cursor.fetchone()[0]