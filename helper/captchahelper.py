from captcha.image import ImageCaptcha
import secrets
import string
def generate_captcha(user_id: int):
    image = ImageCaptcha(width=280, height=90)
    letters = string.ascii_uppercase + string.digits
    captcha_text = ''.join(secrets.choice(letters) for i in range(6))
    image.write(captcha_text, f'CAPTCHA_{user_id}.png')
    return captcha_text, f'CAPTCHA_{user_id}.png'