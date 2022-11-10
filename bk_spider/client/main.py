import os
import datetime
import time
from threading import Thread

# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import wx


# project_path = os.getcwd()
# executable_path=f"{project_path}chromedriver.exe"
# 通过浏览器驱动管理器创建chrome浏览器对象
# driver = webdriver.Chrome(ChromeDriverManager().install())


def start_chrome(url: str) -> bool:
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {url}')  # Press ⌘F8 to toggle the breakpoint.
    driver.get(url)
    # 在60秒内加载网站
    for i in range(60):
        time.sleep(1)
        if driver.title:
            return True
    else:
        return False


def login(account: str, password: str) -> bool:
    click_input = 'document.getElementsByClassName("btn-login bounceIn actLoginBtn")[0].click();'
    driver.execute_script(click_input)
    time.sleep(2)
    click_password = 'document.getElementsByClassName("change_login_type _color")[0].click();'
    driver.execute_script(click_password)
    time.sleep(2)
    # 输入账号
    input_account = f'document.getElementsByClassName("phonenum_input")[0].value = "{account}"'
    driver.execute_script(input_account)
    # 输入密码
    input_password = f'document.getElementsByClassName("password_type password_input")[0].value = "{password}"'
    driver.execute_script(input_password)
    # 点击登录
    click_login = 'document.getElementsByClassName("btn confirm_btn login_panel_op login_submit _bgcolor")[0].click();'
    driver.execute_script(click_login)
    return True


def post(msg: str) -> bool:
    return True


def exit_web() -> bool:
    driver.quit()
    return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 创建一个gui实例
    app = wx.App()

    # 创建一个窗口
    frm = wx.Frame(None, -1, title="贝壳自动引流神器", pos=(100, 100), size=(800, 500), style=wx.DEFAULT_FRAME_STYLE)
    panel = wx.Panel(frm)
    wx.StaticText(panel, label="选择账号", pos=(10, 10), size=(60, 30))
    wx.StaticText(panel, label="设置话术", pos=(70, 10), size=(60, 30))
    wx.StaticText(panel, label="登录数量", pos=(130, 10), size=(60, 30))
    # 显示
    frm.Show()

    # Start the event loop.
    app.MainLoop()
    # if start_chrome("https://bj.ke.com/"):
    #     if login("15556748454", "nkss6666"):
    #         print("登录成功")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
