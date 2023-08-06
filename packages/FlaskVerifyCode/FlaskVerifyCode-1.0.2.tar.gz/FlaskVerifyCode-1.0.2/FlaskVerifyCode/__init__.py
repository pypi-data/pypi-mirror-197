from flask import Flask,request
import sqlite3,json
import random,string
import time,datetime

import smtplib
from email.mime.text import MIMEText

# 登录邮箱服务器
mail_host = ''
mail_user = ''
mail_pass = ''
mail_header = ""
mail_title = ""

# 数据库文件
db = "database.db"

app = Flask(__name__)

# 增删改查简单封装
def RunSqlite(db,table,action,field,value):
    connect = sqlite3.connect(db)
    cursor = connect.cursor()

    # 执行插入动作
    if action == "insert":
        insert = f"insert into {table}({field}) values({value});"
        if insert == None or len(insert) == 0:
            return False
        try:
            cursor.execute(insert)
        except Exception:
            return False

    # 执行更新操作
    elif action == "update":
        update = f"update {table} set {value} where {field};"
        if update == None or len(update) == 0:
            return False
        try:
            cursor.execute(update)
        except Exception:
            return False

    # 执行查询操作
    elif action == "select":

        # 查询条件是否为空
        if value == "none":
            select = f"select {field} from {table};"
        else:
            select = f"select {field} from {table} where {value};"

        try:
            ref = cursor.execute(select)
            ref_data = ref.fetchall()
            connect.commit()
            connect.close()
            return ref_data
        except Exception:
            return False

    # 执行删除操作
    elif action == "delete":
        delete = f"delete from {table} where {field};"
        if delete == None or len(delete) == 0:
            return False
        try:
            cursor.execute(delete)
        except Exception:
            return False
    try:
        connect.commit()
        connect.close()
        return True
    except Exception:
        return False

# 生成指定长度的随机字符串
def generate_random_str(randomlength=32):
    str_list = [random.choice(string.digits) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str

# 调用发信函数
def SendMail(sender_user,recivers_user,title,subject,is_ssl = False):
    # 邮件发送方邮箱地址
    sender = sender_user
    receivers = [recivers_user]

    # 设置email信息
    # message = MIMEText(subject,'plain','utf-8')
    message = MIMEText(subject, 'html', 'utf-8')
    message['Subject'] = title
    message['From'] = sender
    message['To'] = receivers[0]

    # 登录并发送邮件
    try:
        if is_ssl != True:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host,25)
            smtpObj.login(mail_user,mail_pass)
        else:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)
            smtpObj = smtplib.SMTP_SSL(mail_host)
            smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(sender,receivers,message.as_string())
        smtpObj.quit()
        return True
    except smtplib.SMTPException as e:
        return False

# 创建验证码发送数据库
@app.route('/create',methods=['GET'])
def VerificationCodeDB():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    create = "create table VerificationCodeDB(" \
             "uid INTEGER primary key AUTOINCREMENT not null unique," \
             "email char(64) not null unique," \
             "code char(16) not null unique," \
             "time_stamp int not null," \
             "overdue_stamp int not null" \
             ")"
    cursor.execute(create)
    conn.commit()
    cursor.close()
    conn.close()

    return_dict = {'status': '1', 'message': '表结构已创建'}
    return json.dumps(return_dict, ensure_ascii=False)

# 配置默认数据
@app.route('/set_setting',methods=['POST'])
def SetSetting():
    return_dict = {'status': '0', 'message': ''}

    # 判断是不是POST请求
    if request.method == "POST":
        # 判断传入参数是否是5个
        if len(request.get_data()) != 0 and len(request.values) == 5:

            global mail_host
            global mail_user
            global mail_pass
            global mail_header
            global mail_title

            # 判断输入手机号是否合法
            mail_host = request.values.get("mail_host")
            mail_user = request.values.get("mail_user")
            mail_pass = request.values.get("mail_pass")
            mail_header = request.values.get("mail_header")
            mail_title = request.values.get("mail_title")

            print("配置主机: {} 配置用户: {} 密码: {} 数据头: {} 信息: {}".format(mail_host, mail_user,mail_pass,mail_header, mail_title))
            return_dict = {'status': '1', 'message': '已配置'}
            return json.dumps(return_dict, ensure_ascii=False)

        else:
            return_dict = {'status': '0', 'message': '传入参数长度不正确'}
            return json.dumps(return_dict, ensure_ascii=False)


    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)



# 全表扫描,删除无效的数据
@app.route('/delete_code',methods=['GET'])
def DeleteCode():
    time_stamp = int(time.time())

    # 查询表内所有数据
    select = RunSqlite("database.db","VerificationCodeDB","select","uid,overdue_stamp","none")
    if select != []:
        try:
            for id,val in select:
                if val <= time_stamp:
                    delete = RunSqlite("database.db","VerificationCodeDB","delete",f"uid='{id}'","none")
                    print("清理ID: {} --> 清理状态: {}".format(id,delete))
        except Exception:
            pass
        return_dict = {'status': '1', 'message': '已清理'}
        return json.dumps(return_dict, ensure_ascii=False)
    else:
        return_dict = {'status': '1', 'message': '表内记录为空无需清理'}
        return json.dumps(return_dict, ensure_ascii=False)

    return_dict = {'status': '1', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# 发送验证码
@app.route('/send',methods=['POST'])
def send_message():
    return_dict = {'status': '0', 'message': ''}

    # 判断是不是POST请求
    if request.method == "POST":
        # 判断传入参数是否是一个

        if len(request.get_data()) != 0 and len(request.values) == 1:
            # 判断输入邮箱是否合法
            email = request.values.get("email")
            if len(email) != 0:
                # 生成验证码
                msg_code = generate_random_str(5)

                # 设置五分钟时间戳
                timeStamp = int(time.time()) + 300
                dateArray = datetime.datetime.fromtimestamp(timeStamp)
                otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")

                # 判断是插入数据还是更新
                # if select_sql("select email from VerificationCodeDB where email='{}'".format(email)) == []:
                if RunSqlite("database.db","VerificationCodeDB","select","email",f"email='{email}'") == []:

                    # 插入验证码到数据库
                    insert = RunSqlite("database.db","VerificationCodeDB","insert","email,code,time_stamp,overdue_stamp",
                                       f"'{email}','{msg_code}',{int(time.time())},{timeStamp}")

                    # 如果插入失败则无需继续发送
                    if insert == False:
                        return_dict = {'status': '0', 'message': '插入数据失败,停止发送验证码'}
                        return json.dumps(return_dict, ensure_ascii=False)

                    message_code = "您本次登录的验证码是：{} 有效时间：5分钟 验证码有效期至：{}".format(str(msg_code), otherStyleTime)
                    ref = SendMail(mail_header, email, mail_title,
                                   f"<p>{message_code}</p><br>"
                                   "PowerBy: <a href='https://www.lyshark.com'>LyShark</a>", False)

                    if ref == True:
                        print("邮箱发送成功,请查收.")
                        return_dict = {'status': '1', 'message': message_code}
                        return json.dumps(return_dict, ensure_ascii=False)
                    else:
                        return_dict = {'status': '1', 'message': '邮件发送失败'}
                        return json.dumps(return_dict, ensure_ascii=False)

                # 否则说明有则需要更新
                else:
                    time_stamp = RunSqlite("database.db","VerificationCodeDB","select","time_stamp",f"email='{email}'")
                    if time_stamp == [] or time_stamp == False:
                        return_dict = {'status': '1', 'message': '查询时间戳失败'}
                        return json.dumps(return_dict, ensure_ascii=False)

                    # 验证必须要一分钟以后才可继续发送,避免恶意发送短信
                    if (int(time_stamp[0][0]) + 60) <= int(time.time()):
                        update = RunSqlite("database.db","VerificationCodeDB","update",f"email='{email}'",f"code='{msg_code}',time_stamp='{int(time.time())}',overdue_stamp='{timeStamp}'")
                        print("刷新验证码状态")
                        if update == [] or update == False:
                            return_dict = {'status': '1', 'message': '验证码刷新失败'}
                            return json.dumps(return_dict, ensure_ascii=False)

                        message_code = "您本次刷新的验证码是：{} 有效时间：5分钟 验证码有效期至：{} (请勿重复刷新)".format(str(msg_code), otherStyleTime)

                        ref = SendMail(mail_header, email, mail_title,
                                       f"<p>{message_code}</p><br>"
                                       "PowerBy: <a href='https://www.lyshark.com'>LyShark</a>", False)

                        if ref == True:
                            print("邮箱发送成功,请查收.")
                            return_dict = {'status': '1', 'message': message_code}
                            return json.dumps(return_dict, ensure_ascii=False)
                        else:
                            return_dict = {'status': '1', 'message': '邮件发送失败'}
                            return json.dumps(return_dict, ensure_ascii=False)

                        return_dict = {'status': '1', 'message': '未知错误'}
                        return json.dumps(return_dict, ensure_ascii=False)

                    # 如果一分钟以内重复请求,则返回一个错误
                    else:
                        return_dict = {'status': '0', 'message': '频率有点快,请一分钟之后再试!'}
                        return json.dumps(return_dict, ensure_ascii=False)

            else:
                return_dict = {'status': '0', 'message': '禁止传入空参数'}
                return json.dumps(return_dict, ensure_ascii=False)

        else:
            return_dict = {'status': '0', 'message': '传入参数个数不合法'}
            return json.dumps(return_dict, ensure_ascii=False)

    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

# 验证验证码是否正确
@app.route('/verification',methods=['POST'])
def verification_message():
    return_dict = {'status': '0', 'message': ''}

    # 判断是不是POST请求
    if request.method == "POST":
        # 判断传入参数是否是2个
        if len(request.get_data()) != 0 and len(request.values) == 2:
            # 判断输入手机号是否合法
            email = request.values.get("email")
            msg_code = request.values.get("code")
            if len(email) != 0 and len(msg_code) != 0:
                local_timestamp = int(time.time())

                try:
                    # 查询当前用户验证码与时间戳
                    ref_vfa = RunSqlite("database.db","VerificationCodeDB","select","email,overdue_stamp",f"email='{email}'")
                    if ref_vfa != False or ref_vfa != []:

                        # 验证时间戳是否有效
                        if local_timestamp <= ref_vfa[0][1]:

                            # 检查用户输入验证码是否有效.
                            ref_vf_code = RunSqlite("database.db","VerificationCodeDB","select","code",f"email='{email}'")
                            if ref_vf_code == [] or ref_vf_code == False:
                                return_dict = {'status': '1', 'message': '查询验证码出错'}
                                return json.dumps(return_dict, ensure_ascii=False)

                            # 验证码正确
                            if ref_vf_code[0][0] == msg_code:
                                delete = RunSqlite("database.db","VerificationCodeDB","delete",f"email='{email}'","none")
                                if delete != True:
                                    return_dict = {'status': '1', 'message': '删除验证码失败'}
                                    return json.dumps(return_dict, ensure_ascii=False)

                                return_dict = {'status': '1', 'message': '用户验证码正确,验证通过,验证码已被清理'}
                                return json.dumps(return_dict, ensure_ascii=False)

                            # 验证码错误
                            else:
                                return_dict = {'status': '0', 'message': '验证码错误'}
                                return json.dumps(return_dict, ensure_ascii=False)

                        # 验证码过期,无法验证
                        elif local_timestamp > ref_vfa[0][1]:

                            delete = RunSqlite("database.db","VerificationCodeDB","delete","email='{email}'","none")
                            if delete != True:
                                return_dict = {'status': '1', 'message': '删除验证码失败'}
                                return json.dumps(return_dict, ensure_ascii=False)

                            return_dict = {'status': '0', 'message': '验证码已过期,请重新获取验证码'}
                            return json.dumps(return_dict, ensure_ascii=False)
                    else:
                        return_dict = {'status': '0', 'message': '用户不存在'}
                        return json.dumps(return_dict, ensure_ascii=False)

                except Exception:
                    return_dict = {'status': '0', 'message': '请先发送验证码,然后在调用该接口'}
                    return json.dumps(return_dict, ensure_ascii=False)

            else:
                return_dict = {'status': '0', 'message': '禁止传入空参数'}
                return json.dumps(return_dict, ensure_ascii=False)
        else:
            return_dict = {'status': '0', 'message': '传入参数个数不合法'}
            return json.dumps(return_dict, ensure_ascii=False)
    return_dict = {'status': '0', 'message': '未知错误'}
    return json.dumps(return_dict, ensure_ascii=False)

@app.errorhandler(404)
def not_found(error):
    return_dict = {'status': '404', 'message': '页面没有找到'}
    return json.dumps(return_dict, ensure_ascii=False)

@app.errorhandler(405)
def not_found(error):
    return_dict = {'status': '405', 'message': '服务器不提供请求类型'}
    return json.dumps(return_dict, ensure_ascii=False)

@app.errorhandler(500)
def not_found(error):
    return_dict = {'status': '500', 'message': '传入参数有误,或存在不规范输入'}
    return json.dumps(return_dict, ensure_ascii=False)

@app.errorhandler(400)
def not_found(error):

    return_dict = {'status': '400', 'message': 'Bad Request'}
    return json.dumps(return_dict, ensure_ascii=False)

@app.errorhandler(409)
def not_found(error):
    return_dict = {'status': '409', 'message': 'Conflict'}
    return json.dumps(return_dict, ensure_ascii=False)

if __name__ == '__main__':
    app.run(port=5000,debug=False)