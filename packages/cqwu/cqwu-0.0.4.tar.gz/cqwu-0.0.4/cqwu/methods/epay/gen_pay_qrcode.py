import qrcode
from bs4 import BeautifulSoup

import cqwu
from cqwu.errors.auth import CookieError


class GenPayQrcode:
    async def gen_pay_qrcode(
        self: "cqwu.Client",
    ) -> None:
        """
        生成支付二维码
        """
        url = "http://218.194.176.214:8382/epay/thirdconsume/qrcode"
        html = await self.oauth(url)
        if not html:
            raise CookieError()
        if html.url != url:
            raise CookieError()
        soup = BeautifulSoup(html.text, "lxml")
        try:
            data = soup.find("input", attrs={"id": "myText"})["value"]
        except (ValueError, TypeError, KeyError, IndexError):
            return
        qr = qrcode.QRCode()
        qr.add_data(data)
        qr.print_ascii(invert=True)
        img = qrcode.make(data)
        img.save("qrcode.png")
        print("生成支付码到 qrcode.png 成功，请打开该文件查看")
