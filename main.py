import email as email_parse
import poplib
import re
import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

pkey = "20782B4C-05D0-45D7-97A0-41641055B6F6"
key_captcha = '0d3baac93ed3fbbbddb7dfac3f529f88'


def wait_util(driver: uc.Chrome, by: By, element: str, time: int) -> any:
    return WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((by, element)))


# def get_code_from_mail(email_username: str, email_password: str) -> str:
#     mb = MailBox("outlook.office365.com").login(email_username, email_password)
#
#     messages = mb.fetch(criteria=AND(seen=False, from_="noreply@github.com"),
#                         mark_seen=False,
#                         bulk=True)
#     for msg in messages:
#         # Print form and subject
#         print(msg.from_, ': ', msg.subject)
#         # Print the plain text (if there is one)
#         content = msg.text
#         p = re.compile("confirm_verification/(.*)\\?")
#         result = p.search(content)
#         return result.group(1)
#     raise Exception("Khong lai duoc ma code")

def get_code_from_mail(email_username: str, email_password: str) -> str:
    global server
    try:
        email = email_username
        password = email_password
        pop3_server = "outlook.office365.com"
        server = poplib.POP3_SSL(pop3_server, 995)

        # ssl加密后使用
        # server = poplib.POP3_SSL('pop.163.com', '995')
        print(server.set_debuglevel(1))  # 打印与服务器交互信息
        print(server.getwelcome())  # pop有欢迎信息
        server.user(email)
        server.pass_(password)
        print('Messages: %s. Size: %s' % server.stat())
        print(email + ": successful")
        num_messages = len(server.list()[1])
        for i in range(num_messages):
            # get the message at index i
            message_lines = server.retr(i + 1)[1]
            # join the message lines into a single string
            message_text = b'\n'.join(message_lines)
            # parse the message text into an email object
            message = email_parse.message_from_bytes(message_text)
            # print the subject and sender of the message
            print(f'Subject: {message["subject"]}')
            print(f'From: {message["from"]}')
            mes_from: str = message["from"]
            if mes_from.__contains__('noreply@github.com'):
                content: str = str(message.get_payload(0))
                print(content)
                result = re.findall("[0-9]{8}", content)
                return result[0]
    except Exception as ex:
        print(ex)
        raise ex


# def get_code_by_tag(tag: str):
#     url = f"https://api.testmail.app/api/json?apikey=b69eb6af-7b07-4d51-94c3-d571a4322b0f&namespace=7r668&pretty=true&tag={tag}"
#     response = requests.request("GET", url)
#     res = response.text
#     re.search("confirm_verification/(.*?)\\?via_launch_code_email=true", res)


# def call_resolve_funcaptcha() -> str:
#     url = f"http://2captcha.com/in.php?key={key_captcha}&method=funcaptcha&publickey={pkey}&surl=https%3A%2F%2Fapi.funcaptcha.com&pageurl=https%3A%2F%2Fgithub.com%2Fsignup"
#
#     response = requests.request("GET", url)
#     res = response.text
#     print(res)
#     return res.split("|")[1]


# def get_captcha_res(id: str) -> str:
#     i = 0
#     while i < 15:
#         time.sleep(10)
#         url = f"http://2captcha.com/res.php?key={key_captcha}&action=get&id={id}"
#         response = requests.request("GET", url)
#         res: str = response.text
#         print(res)
#         if res.__contains__('OK'):
#             return res[3:]
#         if res == 'ERROR_CAPTCHA_UNSOLVABLE':
#             break
#         elif res == 'CAPCHA_NOT_READY':
#             print("retry continue")
#             i = i + 1
#         else:
#             print("not jet handler")
#             break
#
#     return get_captcha_res(call_resolve_funcaptcha())


def main():
    try:
        options = uc.ChromeOptions()
        options.add_argument(
            "--load-extension=C:\\Users\\daoma\\PycharmProjects\\github_student_pack\\dknlfmjaanfblgfdfebhijalfmhmjjjo\\0.3.4_0")
        options.add_argument("--window-size=270,425")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--disable-application-cache")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-application-cache")
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # captcha_key = '0d3baac93ed3fbbbddb7dfac3f529f88'
        # options.add_argument(r'--load-extension=D:\ifibfemgeogfhoebkmokieepdoobkbpo\3.3.1_0')
        driver = uc.Chrome(options=options)
        mail_username = 'seyahmyway2@hotmail.com'
        mail_pass = 'tKM3bQ21'
        driver.get(
            "https://nopecha.com/setup#sub_1MizllCRwBwvt6pteITkRiia|enabled=true|disabled_hosts=%5B%5D|hcaptcha_auto_open=true|hcaptcha_auto_solve=true|hcaptcha_solve_delay=true|hcaptcha_solve_delay_time=3000|recaptcha_auto_open=true|recaptcha_auto_solve=true|recaptcha_solve_delay=true|recaptcha_solve_delay_time=1000|recaptcha_solve_method=Image|funcaptcha_auto_open=true|funcaptcha_auto_solve=true|funcaptcha_solve_delay=true|funcaptcha_solve_delay_time=1000|awscaptcha_auto_open=true|awscaptcha_auto_solve=true|awscaptcha_solve_delay=true|awscaptcha_solve_delay_time=1000|textcaptcha_auto_solve=true|textcaptcha_solve_delay=true|textcaptcha_solve_delay_time=100|textcaptcha_image_selector=|textcaptcha_input_selector=")
        time.sleep(2)
        driver.get("https://github.com/signup")
        wait_util(driver, By.ID, "email", 10).send_keys(mail_username)
        time.sleep(2)
        driver.find_element(By.ID, "email").send_keys(Keys.ENTER)

        driver.find_element(By.ID, "password").send_keys("Anhmanhbu8")
        time.sleep(2)
        driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
        driver.find_element(By.ID, "login").send_keys(mail_username.replace("@hotmail.com", ""))
        time.sleep(2)
        driver.find_element(By.ID, "login").send_keys(Keys.ENTER)

        driver.find_element(By.ID, "opt_in").send_keys("n" + Keys.ENTER)
        # id_request = call_resolve_funcaptcha()
        # captcha = get_captcha_res(id_request)

        # octocaptcha = driver.find_element(By.NAME, "octocaptcha-token")
        # driver.execute_script(f"arguments[0].value='{captcha}';", octocaptcha)
        time.sleep(4)
        driver.find_element(By.XPATH,
                            "/html/body/div[1]/div[4]/main/div[2]/text-suggester/div[1]/form/div[5]/button").submit()
        time.sleep(3)
        code = get_code_from_mail(mail_username, mail_pass)
        wait_util(driver, By.NAME, "launch_code[]", 10).send_keys(code)
        time.sleep(2)
        driver.find_element(By.XPATH,
                            "/html/body/div[1]/div[6]/main/div[2]/div/form/div/div[2]/div/div[1]/div[1]/label").click()
        time.sleep(1)
        driver.find_element(By.XPATH,
                            "/html/body/div[1]/div[6]/main/div[2]/div/form/div/div[2]/div/div[2]/div[1]/label").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div[2]/div/form/div/div[2]/div/button").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div[2]/div/form/div/div[2]/div/button").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div[2]/div/div/div[1]/div/a").click()
        time.sleep(8)
        if driver.page_source.__contains__("Following"):
            print('Success')
            driver.quit()
        else:
            print('Failed')
            driver.quit()

    except Exception as ex:
        print(ex)
        time.sleep(1000)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
