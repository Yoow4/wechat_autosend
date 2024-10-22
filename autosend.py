from pywinauto import Application
from pywinauto.keyboard import SendKeys
from pywinauto.timings import wait_until
import time


def start_wechat(path):
    """启动微信应用并返回主窗口句柄"""
    app = Application(backend="uia").start(path)
    return app.window(title="微信")

def click_button(button):
    """点击指定的按钮"""
    wait_until(10, 0.5, lambda: button.exists())
    print(f"点击按钮: {button.window_text()}")
    button.click_input()

def find_and_click_chat_box(dlg, chat_title):
    """查找并点击聊天框"""
    chat_box = None
    for _ in range(20):
        try:
            chat_box = dlg.child_window(title_re=f".*{chat_title}.*", control_type="ListItem")
            if chat_box.exists():
                print(f"聊天框 '{chat_title}' 已找到，点击")
                chat_box.click_input()
                return True
        except Exception as e:
            print(f"查找聊天框时发生错误: {e}")
        time.sleep(0.5)  # 等待0.5秒再尝试
    print(f"未能找到聊天框 '{chat_title}'")
    return False


def send_message(chat_input, message):
    """在聊天窗口输入消息并发送"""
    wait_until(20, 0.5, lambda: chat_input.exists())

    max_retries = 5  # 设置最大重试次数
    attempts = 0

    while attempts < max_retries:
        chat_input.click_input()
        time.sleep(1)  # 等待聊天输入框激活
        chat_input.set_focus()  # 确保聊天输入框为活动状态

        # 清空输入框
        SendKeys('^a')  # 选中所有文本
        SendKeys('{DELETE}')  # 删除选中的文本
        time.sleep(0.5)  # 等待删除操作完成

        # 逐字符输入消息
        for char in message:
            SendKeys(char)
            time.sleep(0.1)  # 每个字符之间的延迟

        time.sleep(1)  # 等待消息输入完成，给输入框时间更新

        # 获取输入框内容
        current_text = chat_input.get_value()  # 使用 get_value() 获取输入框内容
        print(f"当前输入框内容: '{current_text}'")  # 调试信息

        # 输出调试信息
        # print("调试信息：")
        # dlg.print_control_identifiers()  # 打印控件标识符

        if current_text == message:
            # 确保发送按钮可用并且已经聚焦
            sendButton = dlg.child_window(title="发送(S)", control_type="Button")
            if sendButton.exists() and sendButton.is_enabled():
                sendButton.click_input()  # 发送消息
                print("消息已发送")
                return  # 成功发送后返回
            else:
                print("发送按钮不可用，无法发送消息")
                break  # 退出循环，因为发送按钮不可用
        else:
            print(f"输入框内容不完整，当前内容: '{current_text}'，重试输入")
            attempts += 1  # 增加尝试次数

    print("达到最大重试次数，无法发送完整消息")






if __name__ == "__main__":
    wechat_path = r'D:\Tencent\WeChat\WeChat.exe'   #设置微信路径
    chat_title = "文件传输助手"  # 设置聊天框标题
    message = "测试自动发送代码 "  # 设置要发送的消息

    dlg = start_wechat(wechat_path)

    # 等待并点击“进入微信”按钮
    loginButton = dlg.child_window(title="进入微信", control_type="Button")
    click_button(loginButton)
    time.sleep(2)  # 等待主窗口加载

    # 打印控件标识符以调试
    # dlg.print_control_identifiers()

    # 查找并点击聊天框
    if find_and_click_chat_box(dlg, chat_title):
        # 获取聊天窗口并输入消息
        chat_input = dlg.child_window(title=chat_title, control_type="Edit")
        send_message(chat_input, message)
