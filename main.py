from time import sleep
from threading import Thread

from nerodia.browser import Browser
from decouple import config


class Bot(Thread):
    def __init__(self, candidate, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = config('email')
        self.senha = config('senha')

        self.candidate = candidate

        self._running = False

        self.url = url
        self.browser = None

    def open_browser(self):
        self.browser = Browser('firefox')
        self.browser.goto(self.url)
        self.browser.wait()

    def auth(self):
        pass

    def get_condidate_div(self):
        return self.browser.div(text=self.candidate)

    def get_captcha_div(self):
        return self.browser.div(
            class_name=[
                '_3xDixtS9TduMA-tXdgvxyM',
                '_2DsRxsoPgkhrq5exq-TSVO',
                '_2cZtCsRea_lK2Xi3dqwru'
            ]
        )

    def votar_novamente(self):
        button = self.browser.button(text='Votar Novamente')
        if button.present:
            print('vou votar novamente!')
            button.click()
            sleep(2)

    def votar(self):
        candidate = self.get_condidate_div()
        if candidate.present:
            candidate.click()
            sleep(2)
            while candidate.present:
                captcha_div = self.get_captcha_div()
                captcha_div.wait_for_exists()
                img = captcha_div.img()
                img.click()
                sleep(5)

    def run(self):
        self._running = True
        while self._running:
            try:
                self.votar()
                self.votar_novamente()
            except Exception as e:
                pass

        self.browser.close()


if __name__ == '__main__':
    bot = Bot(
        'Gizelly',
        'https://gshow.globo.com/realities/bbb/bbb20/votacao/'
        'paredao-bbb20-quem-voce-quer-eliminar-babu-gizelly-'
        'ou-mari-6b0c783d-65cd-4a4e-940c-ad086cf73fee.ghtml'
    )

    bot.start()
    bot.join()
