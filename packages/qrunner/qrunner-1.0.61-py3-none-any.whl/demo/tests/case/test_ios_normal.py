import qrunner


class TestSearch(qrunner.TestCase):

    def test_normal(self):
        self.elem(text='我的', desc='我的入口').click()
        self.elem(text='settings navi', desc='设置入口').click()


if __name__ == '__main__':
    qrunner.main(
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company',
        errors=[{"text": "close white big"}]
    )
