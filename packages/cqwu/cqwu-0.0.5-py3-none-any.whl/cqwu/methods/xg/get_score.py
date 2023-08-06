import json
from typing import List

import cqwu
from cqwu import types
from cqwu.errors.auth import CookieError


class GetScore:
    async def get_score(
            self: "cqwu.Client",
            year: int = None,
            semester: int = None,
    ) -> List["types.Score"]:
        """
        获取期末成绩

        Returns:
            List[types.Score]: 成绩列表
        """
        year = year or self.xue_nian
        semester = semester or self.xue_qi
        url = "http://xg.cqwu.edu.cn/xsfw/sys/zhcptybbapp/*default/index.do#/cjcx"
        html = await self.oauth(url)
        if not html:
            raise CookieError()
        if html.url != url:
            raise CookieError()
        await self.request.get(
            "http://xg.cqwu.edu.cn/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=5275772372599202&appName=zhcptybbapp&v=046351851777942055")
        query_url = "http://xg.cqwu.edu.cn/xsfw/sys/zhcptybbapp/modules/cjcx/cjcxbgdz.do"
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://xg.cqwu.edu.cn',
            'Referer': 'http://xg.cqwu.edu.cn/xsfw/sys/zhcptybbapp/*default/index.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
            'X-Requested-With': 'XMLHttpRequest',
        }
        query_data = [
            {
                "name": "XN",
                "caption": "学年",
                "linkOpt": "AND",
                "builderList": "cbl_m_List",
                "builder": "m_value_equal",
                "value": str(year),
            },
            {
                "name": "XQ",
                "caption": "学期",
                "linkOpt": "AND",
                "builderList": "cbl_m_List",
                "builder": "m_value_equal",
                "value": str(semester),
            }
        ]
        data = {
            'querySetting': json.dumps(query_data),
            'pageSize': '100',
            'pageNumber': '1',
        }
        html = await self.request.post(query_url, headers=headers, data=data)
        data = [types.Score(**i) for i in html.json()["datas"]["cjcxbgdz"]["rows"]]
        return data
