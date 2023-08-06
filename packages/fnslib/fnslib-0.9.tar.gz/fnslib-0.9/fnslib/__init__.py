import openai
import random
import requests
from colorama import init, Fore, Style
import random
import string
init()

def getgpt(OpenAI_Token, Request):
	openai.api_key = OpenAI_Token
	try:
		resp = openai.Completion.create(
			engine="text-davinci-002",
			prompt=Request,
			max_tokens=1024,
			n=1,
			stop=None,
			temperature=0.5,
		).get("choices")[0].text
		print(f'[{Fore.GREEN}FNSLib{Style.RESET_ALL}] Successful get responce from openai.')
		return resp
	except Exception as e:
		print(f'[{Fore.RED}FNSLib{Style.RESET_ALL}] Error while get responce from openai.')
		return f'Error while connect to openai.\nError: {e}'

def send_webhook(message, webhook):
	try:
		data = {'content': message}
		requests.post(webhook, json=data)
		print(F'[{Fore.GREEN}FNSLib{Style.RESET_ALL}] Successful posted request.')
		return 'Success'
	except Exception as e:
		print(f'[{Fore.RED}FNSLib{Style.RESET_ALL}] Error while trying post request.')
		return f'{e}'

def generate_password(length):
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for i in range(length))
    return password