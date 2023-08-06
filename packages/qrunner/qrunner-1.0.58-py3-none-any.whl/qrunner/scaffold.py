import os.path
import sys

page_content_android = """import qrunner
from qrunner import AdrElem


class HomePage(qrunner.Page):
    my_entry = AdrElem(res_id='com.qizhidao.clientapp:id/bottom_view', index=2, desc='我的入口')

"""

case_content_android = """import qrunner
from tests.page.adr_page import HomePage


class TestSearch(qrunner.TestCase):

    def start(self):
        self.page = HomePage(self.driver)

    def test_pom(self):
        self.page.my_entry.click()
        self.sleep(10)


if __name__ == '__main__':
    qrunner.main(
        platform='android',
        device_id='UJK0220521066836',
        pkg_name='com.qizhidao.clientapp'
    )

"""

case_content_ios = """import qrunner


class TestSearch(qrunner.TestCase):

    def test_normal(self):
        self.elem(text='我的', desc='我的入口').click()
        self.sleep(10)


if __name__ == '__main__':
    qrunner.main(
        platform='ios',
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )

"""

func_content_web = """from tests.page.web_page import PatentPage


class PatentFunc:

    def __init__(self, driver):
        self.page = PatentPage(driver)

    def search(self, keyword):
        self.page.search_input.set_text(keyword)
        self.page.search_submit.click()
"""

page_content_web = """import qrunner
from qrunner import WebElem


class PatentPage(qrunner.Page):
    search_input = WebElem(id_='driver-home-step1', desc='查专利首页输入框')
    search_submit = WebElem(id_='driver-home-step2', desc='查专利首页搜索确认按钮')

"""

case_content_web = """import qrunner
from tests.func.web_func import PatentFunc


class TestPatentSearch(qrunner.TestCase):

    def start(self):
        self.func = PatentFunc(self.driver)

    def test_pom(self):
        self.driver.open_url()
        self.func.search('无人机')
        self.assert_in_page('王刚毅')


if __name__ == '__main__':
    qrunner.main(
        platform='web',
        base_url='https://patents.qizhidao.com/'
    )

"""

case_content_api = """import qrunner


class TestGetToolCardListForPc(qrunner.TestCase):

    def test_getToolCardListForPc(self):
        path = '/api/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        payload = {"type": 1}
        self.post(path, json=payload)
        self.assert_eq('code', 0)


if __name__ == '__main__':
    qrunner.main(
        platform='api',
        base_url='https://www.qizhidao.com'
    )
"""

data_content = """{
  "card_type": [0, 1, 2]
}
"""


def create_scaffold(platform):
    """create scaffold with specified project name."""

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    # 新增测试数据目录
    create_folder(os.path.join("tests"))
    create_folder(os.path.join("tests", "case"))
    create_folder(os.path.join("tests", "page"))
    create_folder(os.path.join("tests", "func"))
    create_folder(os.path.join("screenshot"))
    create_folder(os.path.join("report"))
    create_folder(os.path.join("test_data"))
    create_file(
        os.path.join("test_data", "data.json"),
        data_content,
    )
    if platform == "android":
        # 新增安卓测试用例
        create_file(
            os.path.join("tests", "case", "test_android_pom.py"),
            case_content_android,
        )
        create_file(
            os.path.join("tests", "page", "adr_page.py"),
            page_content_android,
        )

    elif platform == "ios":
        # 新增ios测试用例
        create_file(
            os.path.join("tests", "case", "test_ios_normal.py"),
            case_content_ios,
        )
    elif platform == "web":
        # 新增web测试用例
        create_file(
            os.path.join("tests", "case", "test_web_func.py"),
            case_content_web,
        )
        create_file(
            os.path.join("tests", "page", "web_page.py"),
            page_content_web,
        )
        create_file(
            os.path.join("tests", "func", "web_func.py"),
            func_content_web,
        )
    elif platform == "api":
        # 新增接口测试用例
        create_file(
            os.path.join("tests", "case", "test_api.py"),
            case_content_api,
        )
    else:
        print("请输入正确的平台: android、ios、web、api")
        sys.exit()
