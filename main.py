from time import sleep
from threading import Thread

from nerodia.browser import Browser
from decouple import config


class Bot(Thread):
    def __init__(self, candidate, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = config('email')
        self.password = config('password')

        self.candidate = candidate

        self._running = False

        self.url = url
        self.browser = None

        self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        print('abrindo browser')
        self.browser = Browser('firefox')
        self.browser.goto(self.url)
        self.browser.wait()

    def close(self):
        print('fechando browser')
        self.browser.close()

    def auth(self):
        self.condidate_div.click()

        # IFRAME MALDITO!
        # with self.browser.windows[1]
        # self.browser.

        # login = self.browser.input(id='login')
        # login.wait_for_present()
        # login.send_keys(self.email)
        #
        # password = self.browser.input(id='password')
        # password.wait_for_present()
        # password.send_keys(self.password)
        #
        # entrar = self.browser.button(text='Entrar')
        # entrar.wait_for_present()
        # entrar.click()

    @property
    def condidate_div(self):
        return self.browser.div(text=self.candidate)

    @property
    def captcha_div(self):
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
        candidate = self.condidate_div
        if candidate.present:
            print('candidato presente!')
            candidate.click()
            sleep(2)
            while candidate.present:
                captcha_div = self.captcha_div
                captcha_div.wait_for_exists()
                print('Achei o captcha!')
                img = captcha_div.img()
                print('Vou clickar!')
                img.click()
                sleep(5)

    def run(self):
        # self.open_browser()

        # self.auth()

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

    input('Esperando vc logar no sistema!')

    bot.start()

    bot.join()
