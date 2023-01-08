import requests

# https://api.telegram.org/bot5229724925:AAG8314SO8RJoWREmaIGE-dHaXRkBw5ssqc/sendMessage?chat_id=-608762318&text=salom
BOT_TOKEN = "5229724925:AAG8314SO8RJoWREmaIGE-dHaXRkBw5ssqc"
CHANNEL_ID = "-608762318"



class TelegramPusher:

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text=%s"

    def __init__(self, text: str):
        self.msg = text

    def exception(self):
        url = self.url % f"Exception: \n{self.msg}"
        requests.get(url=url)

    def messenger(self):
        requests.get(url=self.url % self.msg)

