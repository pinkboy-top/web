import smtplib
from email.mime.text import MIMEText


def post_163_smtp(mail_user,mail_pass,sender,receivers,title,content):
    """
    mail_user:163用户名
    mail_pass:密码(部分邮箱为授权码)
    sender:邮件发送方邮箱地址
    receivers:邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    title:邮件发送主题
    content:邮件正文内容
    """
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.163.com'
    #163用户名
    mail_user = mail_user  
    #密码(部分邮箱为授权码) 
    mail_pass = mail_pass  
    #邮件发送方邮箱地址
    sender = sender
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = receivers  

    #设置email信息
    #邮件内容设置
    message = MIMEText(content,'plain','utf-8')
    #邮件主题       
    message['Subject'] = title
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
        return 'success'
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
        return ['errpr', e]


if __name__ == '__main__':
    post_163_smtp('xxxx@163.com', 'xxxxxxxx',
    'xxxxxxx@163.com', ['xxxxxxxxxxxxxxx@foxmail.com'], '测试发送主题', '测试发送正文内容')