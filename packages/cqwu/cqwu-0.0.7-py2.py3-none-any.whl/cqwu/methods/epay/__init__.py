from .gen_pay_qrcode import GenPayQrcode
from .get_balance import GetBalance


class EPay(
    GenPayQrcode,
    GetBalance,
):
    pass
