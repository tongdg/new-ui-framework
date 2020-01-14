


if __name__ == '__main__':
    import sys
    import os
    BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    sys.path.append(BASE_PATH)
    from common import page

    EVOR_KEY = '虚拟化环境'
    VM_IP = sys.argv[1]
    driver = page.Page()
    driver.get('http://192.168.32.195:8000/')
    driver.send_keys('#form-username', 'tongdg')
    driver.send_keys('#form-password', '123456')
    driver.click('Sign in')
    driver.click('配置管理')
    driver.click('#sidebar-menu > div > ul > li.current-page > a')
    num = len(driver.find_elements('#EditVars > table > tbody > tr'))
    print(num)
    for i in range(1, num+1):
        print('#EditVars > table > tbody > tr:nth-child(%s) > td:nth-child(%s) > textarea' % (i, 2))
        evor_key = driver.get_attribute(
            selector='#EditVars > table > tbody > tr:nth-child(%s) > td:nth-child(%s) > textarea' % (i, 2),
            attr='text'
        )
        operation = driver.find_elements(
            selector='#EditVars > table > tbody > tr:nth-child(%s) > td:nth-child(%s) > div > button:nth-child(%s)  ' % (i, 8, 1),
        )
        url = driver.find_elements(
            selector='#EditVars > table > tbody > tr:nth-child(%s) > td:nth-child(%s) > textarea' % (i, 5)
        )
        if evor_key == EVOR_KEY:
            driver.click(operation)
            driver.send_keys(url, VM_IP)
            operation = driver.find_elements(
                selector='#EditVars > table > tbody > tr:nth-child(%s) > '
                         'td:nth-child(%s) > div > button:nth-child(%s)  '
                         % (i, 8, 1),
            )
            driver.click(operation)
            break













