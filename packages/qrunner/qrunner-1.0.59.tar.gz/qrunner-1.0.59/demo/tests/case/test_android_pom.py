import qrunner

from tests.page.adr_page import HomePage


class TestSearch(qrunner.TestCase):
    """进入我的页"""

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
