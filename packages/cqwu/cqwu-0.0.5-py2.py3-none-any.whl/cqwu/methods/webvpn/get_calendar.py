import base64
import cqwu
from cqwu.errors import CookieError


class GetCalendar:
    async def get_calendar(
        self: "cqwu.Client",
        xue_nian: int = None,
        xue_qi: int = None,
    ) -> str:
        """ 获取课程表 """
        xue_nian = xue_nian or self.xue_nian
        xue_qi = xue_qi or self.xue_qi
        jw_html = await self.request.get(
            f"{self.web_ehall_path}/appShow?appId=5299144291521305", follow_redirects=True
        )
        if "教学管理服务平台" not in jw_html.text:
            raise CookieError
        jw_host = self.get_web_vpn_host(jw_html.url)
        jw_url = f"{jw_host}/cqwljw/student/wsxk.xskcb10319.jsp"
        params = {
            "params": base64.b64encode(f"xn={xue_nian}&xq={xue_qi}".encode()).decode(),
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Referer': f'{jw_host}/cqwljw/student/xkjg.wdkb.jsp?menucode=S20301',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        jw_html = await self.request.get(jw_url, params=params, headers=headers, timeout=60, follow_redirects=True)
        jw_html = jw_html.text.replace("""<script type="text/javascript" src="//clientvpn.cqwu.edu.cn/webvpn/bundle.debug.js" charset="utf-8"></script>""", "")
        return jw_html.replace("<title></title>", '<meta charset="UTF-8">')
