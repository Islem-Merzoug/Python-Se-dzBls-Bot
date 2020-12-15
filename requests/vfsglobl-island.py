# coding=utf-8
import json
import logging
import os
from datetime import date, datetime, timedelta
from time import sleep
from typing import Callable, Dict, Optional

import PIL
import requests
from PIL import Image
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests.sessions import Session

logging.basicConfig(
    format='%(levelname)s: %(asctime)s %(message)s',
    datefmt='%x %X',
    level=logging.INFO
)
logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ACCOUNT_POOL = (
    {'username': 'xxxx@xxxx',
     'password': 'xxxxxxxxx'},
)
BASE_URL = "https://row1.vfsglobal.com"


def send_mail(text, found=False):
    import smtplib
    from email.header import Header
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    TO = ['xxxx@xxxx']
    SUBJECT = 'Iceland Tourism/Visit to Family and Friends'
    if found:
        SUBJECT = "Available Slot found!"

    # Gmail Sign In
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    gmail_sender = 'xxxx@xxxx'
    gmail_passwd = 'xxxxxxxxx'

    server = None
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(gmail_sender, gmail_passwd)

        message = MIMEMultipart('alternative')
        message['From'] = '"%s" <%s>' % (Header('九条涼果', 'utf-8'),
                                         Header(gmail_sender, 'utf-8'))
        message['To'] = ','.join(
            ['"%s" <%s>' % (Header('Zwei Chan', 'utf-8'),
                            Header(to, 'utf-8')) for to in TO])
        message['Subject'] = "%s" % Header(SUBJECT, 'utf-8')
        message.attach(MIMEText(text, _charset="UTF-8"))

        logger.info("发送邮件: %s", text)
        server.sendmail(gmail_sender, TO, message.as_string())
        logger.info("邮件发送成功")
    except RuntimeError:
        logger.warning("邮件发送成功")
    finally:
        if server is not None:
            server.quit()


def load_loginpage(session: Session,
                   form_meta: Dict[str, str]) -> Dict[str, str]:
    """
    载入登录页面
    :return:
    * request_verification_token - 表单里的隐藏Token
    * captcha_image_url          - 验证码的URL，地址相对于根路径
    :raise RuntimeError 加载登录页面失败
    """
    url = "https://row1.vfsglobal.com/GlobalAppointment/"

    payload = {}
    headers = {
        'Connection'               : 'keep-alive',
        'Pragma'                   : 'no-cache',
        'Cache-Control'            : 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent'               : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User'           : '?1',
        'Accept'                   : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site'           : 'none',
        'Sec-Fetch-Mode'           : 'navigate',
        'Accept-Encoding'          : 'gzip, deflate, br',
        'Accept-Language'          : 'zh-CN,zh;q=0.9,en;q=0.8'
    }

    def parse_page(page_html):
        soup = BeautifulSoup(page_html, 'html.parser')

        form = soup.find('form', {'id': 'ApplicantListForm'})

        return {
            'request_verification_token': form.find(
                'input', {'name': '__RequestVerificationToken'})['value'],
            'captcha_image_url'         : form.find(
                'img', {'id': 'CaptchaImage'})['src'],
        }

    logger.info("尝试加载登录页面")
    response = session.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return {
            **form_meta,
            **parse_page(response.text),
        }

    raise RuntimeError('加载登录页面失败', response)


def solve_captcha(session: Session, form_meta: Dict[str, str],
                  howto: Callable[[PIL.Image.Image], str]) -> Dict[str, str]:
    """
    解决验证码
    :param session: Session
    :param form_meta: 登录页面的结果
    :param howto: 如何从验证码图片中解读出文字
    :return:
    * captcha_detext    - 验证码ID
    * captcha_inputtext - 验证码明文
    :raise RuntimeError 获取验证码失败
    """
    captcha_detext = form_meta['captcha_image_url'].split('=')[1]

    url = "https://row1.vfsglobal.com/GlobalAppointment/DefaultCaptcha/Generate"

    params = {
        't': captcha_detext
    }
    payload = {}
    headers = {
        'Connection'     : 'keep-alive',
        'User-Agent'     : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Accept'         : 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Sec-Fetch-Site' : 'same-origin',
        'Sec-Fetch-Mode' : 'no-cors',
        'Referer'        : 'https://row1.vfsglobal.com/GlobalAppointment/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    logger.info("尝试下载验证码图片")
    response = session.request("GET", url, params=params, headers=headers,
                               data=payload)

    if response.status_code == 200:
        from PIL import Image
        from io import BytesIO
        image = Image.open(BytesIO(response.content))
        captcha_inputtext = howto(image)
        logger.info("验证码: %s => %s", captcha_detext, captcha_inputtext)
        del form_meta['captcha_image_url']
        return {
            **form_meta,
            'captcha_detext'   : captcha_detext,
            'captcha_inputtext': captcha_inputtext
        }

    raise RuntimeError('获取验证码失败', response)


LAST_LOGIN_TIME: datetime = datetime.now()


def simulate_login(session: Session,
                   form_meta: Dict[str, str]) -> Dict[str, str]:
    """
    模拟登录
    :param:
    * request_verification_token
    * captcha_detext
    * captcha_inputtext
    * username
    * password
    :return:
    * vac_link - 访问/GlobalAppointment/Home/SelectVAC的链接
    :raise:
    * RuntimeError 登录失败
    """
    url = "https://row1.vfsglobal.com/GlobalAppointment/"

    payload = {
        '__RequestVerificationToken': form_meta['request_verification_token'],
        'Mission'                   : '',
        'Country'                   : '',
        'Center'                    : '',
        'IsGoogleCaptchaEnabled'    : 'False',
        'reCaptchaURL'              : 'https://www.google.com/recaptcha/api/siteverify?secret={0}&response={1}',
        'reCaptchaPublicKey'        : '6Ld-Kg8UAAAAAK6U2Ur94LX8-Agew_jk1pQ3meJ1',
        'EmailId'                   : form_meta['username'],
        'Password'                  : form_meta['password'],
        'CaptchaDeText'             : form_meta['captcha_detext'],
        'CaptchaInputText'          : form_meta['captcha_inputtext'],
    }
    headers = {
        'Connection'               : 'keep-alive',
        'Cache-Control'            : 'max-age=0',
        'Origin'                   : 'https://row1.vfsglobal.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type'             : 'application/x-www-form-urlencoded',
        'User-Agent'               : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User'           : '?1',
        'Accept'                   : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site'           : 'same-origin',
        'Sec-Fetch-Mode'           : 'navigate',
        'Referer'                  : 'https://row1.vfsglobal.com/GlobalAppointment/',
        'Accept-Encoding'          : 'gzip, deflate, br',
        'Accept-Language'          : 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    def parse_page(page_html: str) -> Dict[str, str]:
        """
        登录成功以后，获取预约页面的访问链接
        """
        soup = BeautifulSoup(page_html, 'html.parser')

        def check_account_banned():
            banner = soup.find('div', {'class': 'validation-summary-errors'})
            if banner is None:
                return

            raise RuntimeError('登录失败', banner.text.strip())

        check_account_banned()

        def is_vac_link(tag: Tag):
            return tag.has_attr('href') and \
                   tag['href'].startswith('/GlobalAppointment/Home/SelectVAC')

        return {
            'vac_link': soup.find(is_vac_link)['href']
        }

    logger.info("尝试用 %s 进行登录", form_meta['username'])
    response = session.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:  # follow redirection
        del form_meta['request_verification_token']
        del form_meta['captcha_detext']
        del form_meta['captcha_inputtext']
        global LAST_LOGIN_TIME
        LAST_LOGIN_TIME = datetime.now()
        return {
            **form_meta,
            **parse_page(response.text)
        }

    raise RuntimeError('登录失败', response)


def load_appointment_page(session: Session, form_meta: Dict[str, str]):
    """
    加载/GlobalAppointment/Home/SelectVAC，读取表单隐藏字段
    :param
    * vac_link
    :return:
    * request_verification_token
    """
    url = BASE_URL + form_meta['vac_link']

    payload = {}
    headers = {
        'Connection'               : 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent'               : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User'           : '?1',
        'Accept'                   : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site'           : 'same-origin',
        'Sec-Fetch-Mode'           : 'navigate',
        'Referer'                  : url,
        'Accept-Encoding'          : 'gzip, deflate, br',
        'Accept-Language'          : 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    logger.info("加载预约页面")
    response = session.request("GET", url, headers=headers, data=payload)

    def parse_page(page_html: str) -> Dict[str, str]:
        """
        加载成功以后，获取提交表单所需的信息
        Une fois le chargement réussi, obtenez les informations nécessaires pour envoyer le formulaire
        """

        soup = BeautifulSoup(page_html, 'html.parser')

        form = soup.find('form', {'id': 'VisaApplicationForm'})

        return {
            'request_verification_token': form.find(
                'input', {'name': '__RequestVerificationToken'})['value'],
        }

    if response.status_code == 200:
        return {
            **form_meta,
            **parse_page(response.text)
        }

    raise RuntimeError("预约页面加载失败", response)


def _check_appointment(session: Session,
                       form_meta: Dict[str, str],
                       location_code, location_name) -> Optional[dict]:
    """
    检查空席位
    :param
    * request_verification_token
    * vac_link
    """
    url = "https://row1.vfsglobal.com/GlobalAppointment/Account/GetEarliestVisaSlotDate"

    payload = f"countryId=6&missionId=7&LocationId={location_code}&VisaCategoryId=2815"
    headers = {
        'Connection'                : 'keep-alive',
        'Accept'                    : 'application/json, text/javascript, */*; q=0.01',
        'Origin'                    : 'https://row1.vfsglobal.com',
        'X-Requested-With'          : 'XMLHttpRequest',
        '__RequestVerificationToken': form_meta['request_verification_token'],
        'User-Agent'                : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Content-Type'              : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Sec-Fetch-Site'            : 'same-origin',
        'Sec-Fetch-Mode'            : 'cors',
        'Referer'                   : BASE_URL + form_meta['vac_link'],
        'Accept-Encoding'           : 'gzip, deflate, br',
        'Accept-Language'           : 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    estimate_login_time = \
        LAST_LOGIN_TIME + timedelta(minutes=20) - datetime.now()

    logger.info("获取 %s 预约空位，预计离下次要求登录还有 %s",
                location_name, estimate_login_time)
    response = session.request("POST", url, headers=headers, data=payload)

    if response.text == '""':
        return None
    if response.text.startswith("{"):
        return json.loads(response.text)
    if response.text.startswith("<"):
        raise RuntimeError("获取失败，账号失效")
    logger.info("预约空位: %s", response.text)
    raise RuntimeError("获取失败", response.text)


def check_appointment_london(session: Session,
                             form_meta: Dict[str, str]) -> Optional[dict]:
    return _check_appointment(session, form_meta,
                              5497, 'London')


def check_appointment_edinburgh(session: Session,
                                form_meta: Dict[str, str]) -> Optional[dict]:
    return _check_appointment(session, form_meta,
                              5498, 'Edinburgh')


def check_appointment_manchester(session: Session,
                                 form_meta: Dict[str, str]) -> Optional[dict]:
    return _check_appointment(session, form_meta,
                              5499, 'Manchester')


def main(account):
    def _retry(func: Callable, times=1):
        try:
            return func()
        except requests.ConnectionError as e:
            if times >= 5:
                logger.error("网络错误超过%d次: %s", times, e.args, exc_info=1)
                exit(0)
                raise e
            logger.warning("网络错误，重试第%d次: %s", times, e.args)
            return _retry(func, times=times + 1)

    def solve(image):
        image.show()
        return input("输入图中验证码: ").upper()

    session = requests.sessions.Session()

    meta = _retry(lambda: load_loginpage(session, account))
    meta = _retry(lambda: solve_captcha(session, meta, solve))
    meta = _retry(lambda: simulate_login(session, meta))
    meta = _retry(lambda: load_appointment_page(session, meta))

    while True:
        result = _retry(lambda: check_appointment_london(session, meta))
        if result is not None:
            dt = datetime.strptime(result['StandardDate'], '%d/%m/%Y').date()
            logger.info(
                "Available slot found on London! "
                "Earliest available date %s", dt)
            if dt < date(2019, 12, 7):
                os.system('say "Available slot found on London!"')
                send_mail(
                    "Available slot found on London! "
                    "Earliest available date %s" % dt, found=True)

        result = _retry(lambda: check_appointment_edinburgh(session, meta))
        if result is not None:
            dt = datetime.strptime(result['StandardDate'], '%d/%m/%Y').date()
            logger.info(
                "Available slot found on Edinburgh! "
                "Earliest available date %s", dt)
            os.system('say "Available slot found on Edinburgh!"')
            send_mail(
                "Available slot found on Edinburgh! "
                "Earliest available date %s" % dt, found=True)

        result = _retry(lambda: check_appointment_manchester(session, meta))
        if result is not None:
            dt = datetime.strptime(result['StandardDate'], '%d/%m/%Y').date()
            logger.info("Available slot found on Manchester! "
                        "Earliest available date %s", dt)
            if dt < date(2019, 12, 7):
                os.system('say "Available slot found on Manchester!"')
                send_mail(
                    "Available slot found on Manchester! "
                    "Earliest available date %s" % dt, found=True)

        sleep(1)


if __name__ == '__main__':
    account_idx = 0
    while True:
        account = ACCOUNT_POOL[account_idx % len(ACCOUNT_POOL)]
        try:
            main(account)
        except KeyboardInterrupt:
            exit(1)
        except BaseException as e:
            if '登录失败' in e.args or '账号失效' in e.args:
                account_idx += 1
                os.system('say "Login failed, switch account."')
                logger.warning("当前账号发生异常，尝试切换账号")
            else:
                os.system('say "Script finished with error."')
                logger.warning("异常 %s", e.args)
            # exit(1)
