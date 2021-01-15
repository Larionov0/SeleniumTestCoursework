from selenium import webdriver
from selenium.webdriver.common.by import By
from subprocess import Popen
import unittest


class AppTest(unittest.TestCase):
    BACKEND_FILE = 'backend.py'
    URL = 'http://localhost:8000'

    def setUp(self):
        self.server = Popen(['python', self.BACKEND_FILE])

    def tearDown(self):
        self.server.kill()

    def test_1(self):
        with webdriver.Chrome() as driver:
            driver.get(self.URL)
            self.assertTrue(driver.find_element(
                By.XPATH, '//h1[.="Is this a good way to process input?"]'), 'No header'
            )

            self.assertTrue(driver.find_element(By.XPATH, '//div[@id="question"]/pre[.!=""]'))

            elements = driver.find_elements(By.XPATH, '//div[@id="comments"]/ul/li')
            c1_author = elements[0].find_element(By.TAG_NAME, 'a').text
            c1_text = elements[0].find_element(By.TAG_NAME, 'span').text
            self.assertEqual(c1_author, 'Alice A.')
            self.assertEqual(c1_text, 'Test comment 1')

            c2_author = elements[1].find_element(By.TAG_NAME, 'a').text
            c2_text = elements[1].find_element(By.TAG_NAME, 'span').text
            self.assertEqual(c2_author, 'Bob B.')
            self.assertEqual(c2_text, 'Test comment 2')

            self.assertTrue(driver.find_element(
                By.XPATH, '//div[@id="signup-section"]/div/button[.="Sign Up"]'), 'sign up button is absent'
            )
            self.assertTrue(driver.find_element(
                By.XPATH, '//div[@id="signup-section"]/div/button[.="Log In"]'), 'log in button is absent'
            )
            self.assertTrue(
                driver.find_element(
                    By.XPATH,
                    '//div[label[1][.="Display Name"][following-sibling::input[1][@name="display_name"]]]'
                ),
                'display name field absent')
            self.assertTrue(
                driver.find_element(
                    By.XPATH,
                    '//div[label[2][.="Email"][following-sibling::input[1][@name="email"]]]'
                ),
                'email field absent')
            self.assertTrue(
                driver.find_element(
                    By.XPATH,
                    '//div[label[3][.="Password"][following-sibling::input[1][@name="password"]]]'
                ),
                'No password field')

    def test_2(self):
        with webdriver.Chrome() as driver:
            driver.get(self.URL)

            name_ = 'bob'
            name = driver.find_element(By.NAME, 'display_name')
            name.send_keys(name_)

            email = driver.find_element(By.NAME, 'email')
            email.send_keys("bob@gmail.com")

            password = driver.find_element(By.NAME, 'password')
            password.send_keys("bob12345")

            sign_up = driver.find_element(By.XPATH, '//button[.="Sign Up"]')
            sign_up.click()

            self.assertTrue(driver.find_element(By.XPATH, f'//div[text()="{name_}"]'), "sign up test failed")

            log_out = driver.find_element(By.XPATH, '//button[.="Log Out"]')
            log_out.click()

            self.assertTrue(driver.find_element(By.XPATH, '//button[.="Log In"]'), "can not log out")

            sign_up = driver.find_element(By.XPATH, '//button[.="Sign Up"]')  # пробуємо реєструватися з тими ж даними
            sign_up.click()

            self.assertTrue(
                driver.find_element(By.XPATH, '//button[.="Log In"]'),
                "Not unique users"
            )

    def test_3(self):
        with webdriver.Chrome() as driver:
            driver.get(self.URL)

            email = driver.find_element(By.NAME, 'email')
            wrong_mail = "NOT_ALICE@gmail.com"
            email.send_keys(wrong_mail)

            password = driver.find_element(By.NAME, 'password')
            password.send_keys("aaa")

            driver.find_element(By.XPATH, '//button[.="Log In"]').click()
            self.assertTrue(
                not bool(driver.find_elements(By.XPATH, '//button[.="Log Out"]')),
                "unregistered user authorised"
            )

            email = driver.find_element(By.NAME, 'email')
            email.clear()
            email.send_keys("alice_2002@gmail.com")
            password = driver.find_element(By.NAME, 'password')
            password.clear()
            password.send_keys("aaa")
            b = driver.find_element(By.XPATH, '//button[.="Log In"]')
            b.click()
            self.assertTrue(driver.find_element(By.XPATH, '//button[.="Log Out"]'), "registered user can not authorise")

    def test_4(self):
        with webdriver.Chrome() as driver:
            driver.get(self.URL)

            email = driver.find_element(By.NAME, 'email')
            email.send_keys("alice_2002@gmail.com")
            password = driver.find_element(By.NAME, 'password')
            password.send_keys("aaa")

            driver.find_element(By.XPATH, '//button[.="Log In"]').click()

            self.assertTrue(driver.find_element(By.ID, 'editor-section'), 'editor section absent')

            new_comment = driver.find_element(By.XPATH, '//button[.="New comment"]')
            self.assertTrue(new_comment, 'comment button absent')

            self.assertTrue(driver.find_elements(
                By.XPATH,
                '//p[.="(enter new comment)"]'),
                'comment field absent'
            )

            js_code = 'var elem = document.getElementById("editor-section"); ' \
                      'elem.style.borderColor = "red"; ' \
                      'elem.style.borderStyle = "solid";'
            driver.execute_script(js_code)
            driver.save_screenshot('screen.png')

    def test_5(self):
        with webdriver.Chrome() as driver:
            driver.get(self.URL)

            name_ = 'bob'
            name = driver.find_element(By.NAME, 'display_name')
            name.send_keys(name_)

            email = driver.find_element(By.NAME, 'email')
            email.send_keys("bob@gmail.com")

            password = driver.find_element(By.NAME, 'password')
            password.send_keys("bob12345")

            sign_up = driver.find_element(By.XPATH, '//button[.="Sign Up"]')
            sign_up.click()

            editor = driver.find_element(By.CLASS_NAME, 'ql-editor')

            editor.clear()
            my_comment = "my test comment"
            editor.send_keys(my_comment)
            new_comment_btn = driver.find_element(By.XPATH, '//button[.="New comment"]')
            new_comment_btn.click()

            self.assertEqual(
                driver.find_elements(
                    By.XPATH, '//div[@id="comments"]/ul/li/span[1]'
                )[-1].text, my_comment,
                'comment error'
            )

            editor.clear()
            for style, word in zip(['bold', 'italic', 'underline', 'strike'], ['first', 'second', 'third', 'fourth']):
                btn = driver.find_element(By.CLASS_NAME, f'ql-{style}')
                btn.click()
                editor.send_keys(word)
                btn.click()

            new_comment_btn.click()

            comment = driver.find_elements(
                By.XPATH, '//div[@id="comments"]/ul/li/span[1]'
            )[-1].get_attribute("innerHTML")

            self.assertEqual(
                '<strong>first</strong><em>second</em><u>third</u><s>fourth</s>',
                comment,
                "error with styles"
            )

            self.assertEqual(
                driver.find_elements(By.XPATH, '//div[@id="comments"]/ul/li/a')[-1].text, 'bob',
                'names does not match'
            )
            self.assertEqual(len(driver.find_elements(By.XPATH, '//button[.="Remove"]')), 2,
                             'buttons remove does not work')

    def test_6(self):
        with webdriver.Chrome() as driver:
            driver.get(self.URL)

            name_ = 'bob'
            name = driver.find_element(By.NAME, 'display_name')
            name.send_keys(name_)

            email = driver.find_element(By.NAME, 'email')
            email.send_keys("bob@gmail.com")

            password = driver.find_element(By.NAME, 'password')
            password.send_keys("bob12345")

            sign_up = driver.find_element(By.XPATH, '//button[.="Sign Up"]')
            sign_up.click()

            editor = driver.find_element(By.CLASS_NAME, 'ql-editor')

            editor.clear()
            my_comment1 = "my first comment"
            my_comment2 = 'my second comment'

            editor.send_keys(my_comment1)
            new_comment_btn = driver.find_element(By.XPATH, '//button[.="New comment"]')
            new_comment_btn.click()

            editor.clear()
            editor.send_keys(my_comment2)
            new_comment_btn.click()

            last_2_comments = driver.find_elements(By.XPATH, '//div[@id="comments"]/ul/li/span[1]')[-2:]
            self.assertEqual(my_comment1, last_2_comments[0].text, 'problem with comments')
            self.assertEqual(my_comment2, last_2_comments[1].text, 'problem with comments')

    def test_7(self):
        with webdriver.Chrome() as driver:
            driver.get(self.URL)

            name_ = 'bob'
            name = driver.find_element(By.NAME, 'display_name')
            name.send_keys(name_)

            email = driver.find_element(By.NAME, 'email')
            email.send_keys("bob@gmail.com")

            password = driver.find_element(By.NAME, 'password')
            password.send_keys("bob12345")

            sign_up = driver.find_element(By.XPATH, '//button[.="Sign Up"]')
            sign_up.click()

            my_comment1 = 'my first comment'
            my_comment2 = 'my second comment'

            editor = driver.find_element(By.CLASS_NAME, 'ql-editor')

            editor.clear()
            editor.send_keys(my_comment1)
            new_comment_btn = driver.find_element(By.XPATH, '//button[.="New comment"]')
            new_comment_btn.click()

            editor.clear()
            editor.send_keys(my_comment2)
            new_comment_btn.click()

            remove_btn = driver.find_elements(By.XPATH, '//div[@id="comments"]/ul/li/span[2][.="Remove"]')[-1]
            remove_btn.click()

            my_last_comment = driver.find_elements(By.XPATH, '//div[@id="comments"]/ul/li/span[1]')[-1]
            self.assertEqual(my_last_comment.text, my_comment1)

            other_comments = driver.find_elements(By.XPATH, '//div[@id="comments"]/ul/li/span[1]')
            self.assertEqual(len(other_comments), 3, 'some comments deleted')

    def test_8(self):
        with webdriver.Chrome() as driver1:
            driver1.get(self.URL)

            name_ = 'user1'
            name = driver1.find_element(By.NAME, 'display_name')
            name.send_keys(name_)

            email = driver1.find_element(By.NAME, 'email')
            email.send_keys("bob@gmail.com")

            password = driver1.find_element(By.NAME, 'password')
            password.send_keys("bob12345")

            sign_up = driver1.find_element(By.XPATH, '//button[.="Sign Up"]')
            sign_up.click()

            editor = driver1.find_element(By.CLASS_NAME, 'ql-editor')
            editor.clear()
            editor.send_keys('comment1')
            new_comment_btn = driver1.find_element(By.XPATH, '//button[.="New comment"]')
            new_comment_btn.click()

            with webdriver.Chrome() as driver2:
                driver2.get(self.URL)

                name_ = 'user2'
                name = driver2.find_element(By.NAME, 'display_name')
                name.send_keys(name_)

                email = driver2.find_element(By.NAME, 'email')
                email.send_keys("boba@gmail.com")

                password = driver2.find_element(By.NAME, 'password')
                password.send_keys("boba12345")

                sign_up = driver2.find_element(By.XPATH, '//button[.="Sign Up"]')
                sign_up.click()

                editor2 = driver2.find_element(By.CLASS_NAME, 'ql-editor')
                editor2.clear()
                editor2.send_keys('comment2')
                new_comment_btn2 = driver2.find_element(By.XPATH, '//button[.="New comment"]')
                new_comment_btn2.click()

                all_comments = driver2.find_elements(By.XPATH, '//div[@id="comments"]/ul/li/span[1]')
                self.assertEqual(len(all_comments), 4, 'Not all comments')

                editor.clear()
                editor.send_keys("comment3")
                new_comment_btn.click()

                all_comments = driver1.find_elements(By.XPATH, '//div[@id="comments"]/ul/li/span[1]')
                self.assertEqual(len(all_comments), 5, "Not 5 comments")

                last_remove = driver2.find_elements(By.XPATH, '//div[@id="comments"]/ul/li/span[2][.="Remove"]')[-1]
                last_remove.click()

                all_comments = driver2.find_elements(By.XPATH, '//div[@id="comments"]/ul/li/span[1]')
                self.assertEqual(len(all_comments), 4, "Not 4 comments")

        with webdriver.Chrome() as driver3:
            driver3.get(self.URL)

            my_comments = driver3.find_elements(By.XPATH, '//div[@id="comments"]/ul/li/span[1]')[2:]

            self.assertEqual(my_comments[0].text, 'comment1', 'wrong comments')
            self.assertEqual(my_comments[1].text, 'comment3', 'wrong comments')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
