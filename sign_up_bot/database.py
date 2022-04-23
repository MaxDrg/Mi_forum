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

	async def add_user(self, user_id: int, first_name: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""INSERT INTO forum_user (telegr_id, first_name) VALUES (%s, %s);""", (user_id, first_name, ))
		self.conn.commit()

	async def update_user_data(self, user_id: int, user_name: str, password: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""UPDATE forum_user SET user_name = %s, passw = %s WHERE telegr_id = %s;""", (user_name, password, user_id, ))
		self.conn.commit()

	async def check_user(self, user_id: int):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT EXISTS(SELECT id FROM forum_user WHERE telegr_id = %s);""", (user_id, ))
			return cursor.fetchone()[0]

	async def get_subscription(self, user_id: int):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT subscription FROM forum_user WHERE telegr_id = %s);""", (user_id, ))
			return cursor.fetchone()[0]

	async def create_transaction(self, user_id: int, days: int):
		with self.conn.cursor() as cursor:
			cursor.execute("""INSERT INTO forum_transaction (user_id, days) VALUES ((SELECT id FROM forum_user WHERE telegr_id = %s), %s) RETURNING id;""", (user_id, days, ))
			id = cursor.fetchone()[0]
		self.conn.commit()
		return id

	async def update_transaction(self, transaction_id: int, message_id: int, signature: str):
		with self.conn.cursor() as cursor:
			cursor.execute("""UPDATE forum_transaction SET message_id = %s, signature = %s WHERE id = %s;""", (message_id, signature, transaction_id, ))
		self.conn.commit()

	async def get_message(self, user_id: int,):
		with self.conn.cursor() as cursor:
			cursor.execute("""SELECT id, message_id FROM forum_transaction WHERE telegr_id = (SELECT id FROM forum_user WHERE telegr_id = %s));""", (user_id, ))
			return cursor.fetchone()
		
	async def delete_transaction(self, transaction_id: int):
		with self.conn.cursor() as cursor:
			cursor.execute("""DELETE FROM forum_transaction WHERE id = %s;""", (transaction_id, ))
		self.conn.commit()