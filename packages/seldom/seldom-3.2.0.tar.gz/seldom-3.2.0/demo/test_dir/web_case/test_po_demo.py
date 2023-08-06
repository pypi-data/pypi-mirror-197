"""
page object model
Using the poium Library
https://github.com/SeldomQA/poium
```
> pip install poium=1.2.0
```
"""
import seldom
from poium import Page, Element, Elements


class BaiduPage(Page):
    """baidu page"""
    input = Element("#kw", describe="搜索输入框")
    button = Element("id=su", describe="搜索按钮")
    result = Elements("//div/h3/a", describe="结果")


class BaiduTest(seldom.TestCase):
    """Baidu search test case"""

    def test_case(self):
        """
        A simple test
        """
        page = BaiduPage(print_log=True)
        page.open("https://www.baidu.com")
        self.sleep(3)
        # assert element
        self.assertTrue(page.input.is_exist())
        page.input.send_keys("seldom")
        page.button.click()
        self.sleep(3)
        # assert title
        self.assertTitle("seldom_百度搜索")

        for r in page.result:
            # assert text in
            self.assertIn("seldom", r.text)


if __name__ == '__main__':
    seldom.main(browser='chrome', debug=True)
