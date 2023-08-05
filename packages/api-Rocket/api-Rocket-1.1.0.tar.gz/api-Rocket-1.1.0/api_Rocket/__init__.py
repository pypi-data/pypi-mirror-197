import requests
import random
import json
class Client:
	def __init__(self, token):
		self.headers = {
			"accept": "application/json",
			"Rocket-Pay-Key": token,
			"Content-Type": "application/json",
		}
	#готов
	def api_version(self):
		url = "https://pay.ton-rocket.com/version"
		responce = requests.get(url)
		print(responce.status_code)

		if responce.status_code != 200:
			x = "Error! contact:\n" + str(responce.text)

		else:
			x = json.loads(responce.text)
		return x
		
	#готов
	def info(self):
		
		url = "https://pay.ton-rocket.com/app/info"
		responce = requests.get(url, headers=self.headers)
		if responce.status_code != 200:
			x = "Error! contact:\n" + str(responce.text)
		else:
			x = json.loads(responce.text)
		return x
		
	#готов
	def transfer(self, data):
		rand = random.randint(1000, 5000000000)
		responce = requests.post('https://pay.ton-rocket.com/app/transfer', headers = self.headers,
		json = {
			"tgUserId": data["userid"],
			"currency": data["currency"],
			"amount": data["amount"],
			"transferId": str(rand),
			"description": data["comment"]
		}
		)
		
		if responce.status_code != 201:
			x = "Error! contact:\n" + str(responce.text)

		else:
			x = json.loads(responce.text)
		return x
		
	#готов
	def create_multi_Cheques(self, data):
		responce = requests.post('https://pay.ton-rocket.com/multi-cheques', headers = self.headers,
			json = {
				"currency": data["currency"],
				"chequePerUser": data["PerUser"], #int
				"usersNumber": data["usersNumber"], #int
				"refProgram": data["refProgram"],
				"password": data["password"],
				"description": "This cheque is the best",
				"sendNotifications": True,
				"enableCaptcha": True,
				"telegramResourcesIds": [
					data["telegramResurce"]
					],
				"forPremium": False,
				"linkedWallet": False,
				"disabledLanguages": [
				"NL",
				"FR"
				]
			}
		)
		if responce.status_code != 201:
			x = "Error! contact:\n" + str(responce.text)

		else:
			x = json.loads(responce.text)
		return x
	
	#готовy
	def check_multi_Cheques(self, limit = 100, offset = 0):
		responce = requests.get(f"https://pay.ton-rocket.com/multi-cheques?limit={limit}&offset={offset}", headers= self.headers)
		x = json.loads(responce.text)
		return x
		
	def info_multi_Cheques(self, id):
		responce = requests.get(f"https://pay.ton-rocket.com/multi-cheques/{id}", headers=self.headers)
		x = json.loads(responce.text)
		return x
		
	def edit_multi_Cheques(self, id, data):
		responce = requests.get(f"https://pay.ton-rocket.com/multi-cheques/{id}", headers=self.headers,
				json = {
					"password": data["password"],
					"telegramResourcesIds": [
						data["telegramResurce"]
					]
				}
		)
		
		if responce.status_code != 200:
			x = "Error! contact:\n" + str(responce.text)

		else:
			x = json.loads(responce.text)
		return x
		
	def delete_multi_Cheques(self, id):
		responce = requests.delete(f"https://pay.ton-rocket.com/multi-cheques/{id}", headers=self.headers)
		
		if responce.status_code != 200:
			x = "Error! contact:\n" + str(responce.text)

		else:
			x = json.loads(responce.text)
		return x

	def check_currency(self):
		responce = requests.get("https://pay.ton-rocket.com/currencies/available", headers=self.headers)
		if responce.status_code != 200:
			x = "Error! contact:\n" + str(responce.text)

		else:
			x = json.loads(responce.text)
		return x


	def create_invoice(self, data):

		responce = requests.post("https://pay.ton-rocket.com/tg-invoices", headers=self.headers,
								json = {
									"amount": float(data["amount"]),
									"numPayments": int(data["numPayments"]),
									"currency": data["currency"],
									"description": data["description"],
									"hiddenMessage": data["message"],
									"callbackUrl": data["url"],
									"payload": "load",
									"expiredIn": data["expired"]
								}
			)

		if responce.status_code != 201:
			x = "Error! contact:\n" + str(responce.text)

		else:
			x = json.loads(responce.text)
		return x

	def check_invoices(self, limit=100, offset=0):
		responce = requests.get(f"https://pay.ton-rocket.com/tg-invoices?limit={limit}&offset={offset}", headers=self.headers)

		if responce.status_code != 200:
			x = "Error! contact:\n" + str(responce.text)

		else:
			x = json.loads(responce.text)
		return x

	def get_invoice(self, id=0):
		responce = requests.get(f"https://pay.ton-rocket.com/tg-invoices/{id}", headers=self.headers)

		if responce.status_code != 200:
			x = "Error! contact:\n" + str(responce.text)

		else:
			x = json.loads(responce.text)
		return x

	def delete_invoice(self, id=0):
		responce = requests.delete(f"https://pay.ton-rocket.com/tg-invoices/{id}", headers=self.headers)

		if responce.status_code != 200:
			x = "Error! contact:\n" + str(responce.text)

		else:
			x = json.loads(responce.text)
		return x


#information
__title__ = "api-Rocket"

__author__ = "Redpiar"

__license__ = "MIT"

__copyright__ = "Copyright 2023 Redpiar"

__version__ = '1.1.0'

__status__ = "(Beta)"

__newest__ = json.loads(requests.get("https://pypi.org/pypi/api-Rocket/json").text)["info"]["version"]

if __version__ != __newest__:
	print(f"""
{__title__} made by {__author__}\nPlease update the library. Your version: {__version__} a new version: {__newest__}
""")
else:
	print(f"""
{__title__} {__version__}{__status__} made by {__author__}\n
""")