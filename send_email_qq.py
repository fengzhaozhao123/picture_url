import smtplib
import mimetypes
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
import datetime
import zipfile
import os

#第三方SMTP服务
mail_host = "smtp.qq.com"     # 这里 使用的是qq邮箱的smtp服务器
mail_user = "767938404@qq.com"    # xxxxxx@qq.com
mail_pass = "dellahxvatlebdii"   # 邮箱的授权码

receiver = "756483412@qq.com"
sender = "767938404@qq.com"

"""
# yixia wei fasong wenben
message = MIMEText("你好，世界！")
message["From"] = sender
message["To"] = receiver
message["Subject"] = "邮件主题"

def send_email():
    try:
        server = smtplib.SMTP_SSL()   # 在阿里云上python2.7以上需要使用SSL协议 
        server.connect(mail_host, port=465) # 阿里云25 和80 端口均被使用 465端口使用 SSL协议
        server.login(mail_user,mail_pass)
        server.sendmail(sender,receiver,message.as_string())
        server.close()
        print("邮件发送成功!")
    except Exception as e:
        print("邮件发送失败!",e)
"""

file_path = "/home/nvidia/dolphin_data/images/"
zip_path = "/home/nvidia/dolphin_data/"
zip_path_name = zip_path + "images.zip"

def zip_dir(dir_path, outFullName):
    """
    压缩指定文件夹:
    param dir_path: 目标文件夹路径:
    param outFullName:  压缩文件保存路径+XXXX.zip
    :return:
    """
    testcase_zip = zipfile.ZipFile(outFullName, 'w', zipfile.ZIP_DEFLATED)
    #for path, dir_names, file_names in os.walk(dir_path):
    #    for filename in file_names:
    #        testcase_zip.write(os.path.join(path, filename))
    image_path_list = os.listdir(dir_path)
    for file_names in image_path_list:
        testcase_zip.write(os.path.join(dir_path, file_names))
    testcase_zip.close()
    print("打包成功")



def send_mail():
    time = datetime.datetime.today().strftime("%m-%d %H：%M")
    msgRoot = MIMEMultipart('related')
    # email_body
    msgRoot['From'] = Header("SYSU_DOLPHIN_IMAGES", 'utf-8')
    msgRoot['To'] =  Header("sysu402402@aliyun.com", 'utf-8')
    subject = "new images in {}".format(time)
    msgRoot['Subject'] = Header(subject, 'utf-8')
    
    
    data = open(zip_path_name, 'rb')
    ctype, encoding = mimetypes.guess_type(zip_path_name)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    attach_zip = MIMEBase(maintype, subtype)
    attach_zip.set_payload(data.read())
    data.close()
    encoders.encode_base64(attach_zip)  # 把附件编码
    # 修改附件名称
    filename = "{}-dolphin_images.zip".format(time)
    attach_zip.add_header('Content-Disposition', 'attachment', filename=filename)
    msgRoot.attach(attach_zip)
    
    try:
        # SMTP类初始化一个对象，含两个参数，一个是服务器类型（QQ邮箱、163邮箱等等），一个是端口号
        server = smtplib.SMTP_SSL(mail_host, 465)
        # login函数登录邮箱，含2个参数，一个是登录账号，一个是密码
        server.login(mail_user,mail_pass)
        server.sendmail(sender, receiver, msgRoot.as_string())
        server.close()
        print('邮件发送成功')
        #     return True
    except Exception as e:
        print('邮件发送失败', str(e))
        # return False



if __name__ == '__main__':
    zip_dir(file_path, zip_path_name)
    send_mail()

