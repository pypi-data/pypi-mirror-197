import qrunner
from qrunner import AdrElem


class HomePage(qrunner.Page):
    """首页"""
    my_entry = AdrElem(res_id='com.qizhidao.clientapp:id/bottom_view', index=2, desc='我的入口')
