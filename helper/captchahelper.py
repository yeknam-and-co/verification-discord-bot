from captcha.image import ImageCaptcha
import secrets
import string
def generate_captcha():
    image = ImageCaptcha(width=280, height=90)
    letters = string.digits
    captcha_text = ''.join(secrets.choice(letters) for i in range(6))
    data = image.generate(captcha_text)
    image.write(captcha_text, 'CAPTCHA.png')
    return captcha_text, 'CAPTCHA.png'