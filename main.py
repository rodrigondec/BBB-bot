from time import sleep

from nerodia.browser import Browser


browser = Browser('firefox')
browser.goto('https://gshow.globo.com/realities/bbb/bbb20/votacao/paredao-bbb20-quem-voce-quer-eliminar-babu-gizelly-ou-mari-6b0c783d-65cd-4a4e-940c-ad086cf73fee.ghtml')
browser.wait()


def votar_novamente():
    button = browser.button(text='Votar Novamente')
    if button.present:
        print('vou votar novamente!')
        button.click()
        sleep(2)


def votar_gizelly():
    gizelly_div = browser.div(text='Gizelly')
    if gizelly_div.present:
        print('existe gizelly!')
        gizelly_div.click()
        sleep(2)
        while gizelly_div.present:
            captcha_div = browser.div(
                class_name=['_3xDixtS9TduMA-tXdgvxyM', '_2DsRxsoPgkhrq5exq-TSVO', '_2cZtCsRea_lK2Xi3dqwru'])
            captcha_div.wait_for_exists()
            img = captcha_div.img()
            print('achei a imagem!!')
            print('Vou clickar!')
            img.click()
            sleep(5)


while True:
    try:
        votar_gizelly()
        votar_novamente()
    except Exception as e:
        print(e)
