import qrunner
from tests.func.web_func import PatentFunc


class TestPatentSearch(qrunner.TestCase):

    def start(self):
        self.func = PatentFunc(self.driver)

    def test_pom(self):
        """pom模式代码"""
        self.driver.open_url()
        self.func.search('无人机')
        self.assert_in_page('王刚毅')


if __name__ == '__main__':
    qrunner.main(
        platform='web',
        base_url='https://patents.qizhidao.com/'
    )
