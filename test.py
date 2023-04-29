# enconding=utf-8
import email as email_parse
import poplib
import re
import traceback


def get_code_from_mail(email, password):
    global server
    try:
        email = email
        password = password
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
            # content: str = str(message.get_payload(0))
            print(message)

            # if mes_from.__contains__('noreply@github.com'):
            #     content: str = str(message.get_payload(0))
            #     print(content)
            #     result = re.findall("[0-9]{8}", content)
            #     return result[0]
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        return ''
    server.quit()


if __name__ == '__main__':
    get_code_from_mail("bovellcurlem@hotmail.com", "yb48dA46")
