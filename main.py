import concurrent
import email as email_parse
import json
import poplib
import re
import time
import traceback
from collections import namedtuple

import psycopg2 as psycopg2
import requests
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

pkey = "20782B4C-05D0-45D7-97A0-41641055B6F6"
# Establish a connection to the database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="changeme"
)

# Open a cursor to perform database operations
cur = conn.cursor()


def wait_util(driver: uc.Chrome, by: By, element: str, time: int) -> any:
    return WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((by, element)))


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
        traceback.print_exc()
        return ''


# shared_var = 0


def get_proxy(index: int) -> str:
    print('index proxy --- ' + str(index))
    # if proxy == '':
    #     proxy = '2e9d7d4493fdc3da5636026c33896e9f'
    # else:
    #     proxy = 'dc55203f61addd15947dbf60b0825504'
    proxy_arr = ['586eca151ee91d30b102e3ff0a5ff566', '56d167f9dcb51fe2535802f6624d7252',
                 '13d6f94be47848c8986f36c85440e2a8']
    url = "https://tmproxy.com/api/proxy/get-new-proxy"
    payload = json.dumps({
        "api_key": proxy_arr[index],
        "id_location": 0
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    print(json_data)
    code = int(json_data['code'])
    print('code ' + str(code))

    if code.__eq__(0):
        result2: str = str(json_data['data']['https'])
        print('IP: ' + result2)
        return result2
    elif code.__eq__(5):
        message = json_data['message']
        print(message)
        result_find = re.findall("[0-9]{1,3}", message)
        print(result_find)
        wait_time = int(result_find[0])
        time.sleep(wait_time + 1)
        return get_proxy(index)


# @timeout(100)
def run(email):
    try:

        # global shared_var
        str_exec = "insert into github_student_pack ( username, passw, email_id) "
        options = uc.ChromeOptions()
        options.add_argument(
            "--load-extension=C:\\Users\\daoma\\PycharmProjects\\github_student_pack\\dknlfmjaanfblgfdfebhijalfmhmjjjo\\0.3.4_0")
        options.add_argument("--window-size=270,425")
        print('shared_var' + str(email.id))
        proxy: str = get_proxy(int(email.id) % 3)
        print('shared_var' + proxy)
        options.add_argument("--proxy-server=" + proxy)
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--disable-application-cache")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-application-cache")
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # captcha_key = '0d3baac93ed3fbbbddb7dfac3f529f88'
        # options.add_argument(r'--load-extension=D:\ifibfemgeogfhoebkmokieepdoobkbpo\3.3.1_0')
        # options.add_argument("--disable-application-cache")


        mail_username = email.username
        mail_pass = email.passw
        password = 'Anhmanhbu8'

        profile_dir = f'D:\\profile\\{mail_username}'
        options.add_argument(f'--user-data-dir={profile_dir}')
        driver = uc.Chrome(options=options)
        username = mail_username.replace("@hotmail.com", "").replace("@outlook.com", "")
        driver.get(
            "https://nopecha.com/setup#sub_1MizllCRwBwvt6pteITkRiia|enabled=true|disabled_hosts=%5B%5D|hcaptcha_auto_open=true|hcaptcha_auto_solve=true|hcaptcha_solve_delay=true|hcaptcha_solve_delay_time=3000|recaptcha_auto_open=true|recaptcha_auto_solve=true|recaptcha_solve_delay=true|recaptcha_solve_delay_time=1000|recaptcha_solve_method=Image|funcaptcha_auto_open=true|funcaptcha_auto_solve=true|funcaptcha_solve_delay=true|funcaptcha_solve_delay_time=1000|awscaptcha_auto_open=true|awscaptcha_auto_solve=true|awscaptcha_solve_delay=true|awscaptcha_solve_delay_time=1000|textcaptcha_auto_solve=true|textcaptcha_solve_delay=true|textcaptcha_solve_delay_time=100|textcaptcha_image_selector=|textcaptcha_input_selector=")
        time.sleep(2)
        driver.get("https://github.com/signup")
        wait_util(driver, By.ID, "email", 20).send_keys(mail_username)
        time.sleep(2)
        driver.find_element(By.ID, "email").send_keys(Keys.ENTER)
        isPresent: bool = len(driver.find_elements(By.XPATH,
                                                   "/html/body/div[1]/div[4]/main/div[2]/text-suggester/div[2]/p[1]/p")) > 0
        if isPresent:
            insert_data = str_exec + " VALUES ( %s, %s, %s )"
            object = (username, password, email.id)
            cur.execute(insert_data, object)
            conn.commit()
            return
        driver.find_element(By.ID, "password").send_keys("Anhmanhbu8")
        time.sleep(2)
        driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
        driver.find_element(By.ID, "login").send_keys(username)
        time.sleep(2)
        driver.find_element(By.ID, "login").send_keys(Keys.ENTER)

        driver.find_element(By.ID, "opt_in").send_keys("n" + Keys.ENTER)
        # id_request = call_resolve_funcaptcha()
        # captcha = get_captcha_res(id_request)

        # octocaptcha = driver.find_element(By.NAME, "octocaptcha-token")
        # driver.execute_script(f"arguments[0].value='{captcha}';", octocaptcha)
        time.sleep(10)
        wait_util(driver, By.XPATH, "/html/body/div[1]/div[4]/main/div[2]/text-suggester/div[1]/form/div[5]/button",
                  30).submit()

        time.sleep(5)
        code = get_code_from_mail(mail_username, mail_pass)
        if len(code) == 0:
            return
        wait_util(driver, By.NAME, "launch_code[]", 10).send_keys(code)
        time.sleep(2)
        driver.find_element(By.XPATH,
                            "/html/body/div[1]/div[6]/main/div[2]/div/form/div/div[2]/div/div[1]/div[1]/label").click()
        time.sleep(1)
        driver.find_element(By.XPATH,
                            "/html/body/div[1]/div[6]/main/div[2]/div/form/div/div[2]/div/div[2]/div[1]/label").click()
        time.sleep(1)
        driver.find_element(By.XPATH,
                            "/html/body/div[1]/div[6]/main/div[2]/div/form/div/div[2]/div/button").click()
        time.sleep(2)
        driver.find_element(By.XPATH,
                            "/html/body/div[1]/div[6]/main/div[2]/div/form/div/div[2]/div/button").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/main/div[2]/div/div/div[1]/div/a").click()
        time.sleep(8)
        insert_data = str_exec + " VALUES ( %s, %s, %s )"
        object = (username, password, email.id)
        cur.execute(insert_data, object)
        if driver.page_source.__contains__("Following"):
            print('Success')
        else:
            print('Failed')

    except Exception as ex:
        traceback.print_exc()
        str_exec = "insert into github_student_pack ( username, passw, email_id, STATUS) "
        insert_data = str_exec + " VALUES ( %s, %s, %s ,'FAILED' )"
        object = (username, password, email.id)
        cur.execute(insert_data, object)
    finally:
        # shared_var += 1
        conn.commit()
        driver.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        # thread = threading.Thread(target=get_proxy)
        # thread.start()

        str_SELECT = "SELECT e.id, e.username, e.passw from EMAIL e where e.id not in (SELECT email_id from github_student_pack)"
        cur.execute(str_SELECT)
        # data = cur.fetchall()
        # Create a named tuple to represent the data
        Row = namedtuple('Row', [desc[0] for desc in cur.description])
        # Fetch the data and convert it to named tuples
        rows = [Row(*row) for row in cur.fetchall()]
        # for email in rows:
        #     run(email)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            # Submit tasks to the pool
            futures = [executor.submit(run, email) for email in rows]

            # Wait for tasks to complete
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                print("result" + result)

    # try:
    #     with multiprocessing.Pool(processes=4) as pool:
    #         [pool.apply_async(run(), (email,)) for email in rows]

    except Exception as ex:
        print(ex)
    finally:
        cur.close()
        conn.close()
