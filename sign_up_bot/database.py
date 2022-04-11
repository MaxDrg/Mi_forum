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

	async def add_user(self, user_id, img):
		with self.conn.cursor() as cursor:
			cursor.execute("""INSERT INTO forum_user (telegr_id, image) VALUES (%s, %s);""", (user_id, img, ))
		self.conn.commit()

	async def show_photo(self):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT image FROM forum_user where telegr_id = 334338195;""")
			return cursor.fetchone()[0]