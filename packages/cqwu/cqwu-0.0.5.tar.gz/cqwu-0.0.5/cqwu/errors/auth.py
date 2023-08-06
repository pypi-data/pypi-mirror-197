from .base import CQWUEhallError


class AuthError(CQWUEhallError):
    pass


class UsernameOrPasswordError(AuthError):
    pass


class CookieError(AuthError):
    pass


class NeedCaptchaError(AuthError):
    """ 需要验证码才能登录 """
    def __init__(self, captcha: bytes):
        self.captcha = captcha
