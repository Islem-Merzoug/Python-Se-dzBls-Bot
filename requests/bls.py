import requests
from bs4 import BeautifulSoup
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

login_data = {
   'app_typ': 'Individual',
    'member': '2',
    'centre': '44#44',
    'category': 'Normal',
    'phone_code': '225',
    'phone': '283863588',
    'email': 'zaki.kaka99@gmail.com',
    'verification_code': 'Request verification code',
}
with requests.Session() as s:
    url = 'https://civ.blsspainvisa.com/book_appointment.php'
    r = s.get(url, headers = headers)
    # soup = BeautifulSoup(r.content, 'html.parser')
    r = s.post(url, data=login_data)
    print(r.content)


