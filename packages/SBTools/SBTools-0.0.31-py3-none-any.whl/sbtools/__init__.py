# -*- coding: utf-8 -*-
import re
import json
import time
import random
import string
import pymysql
import hashlib
import sqlite3
import requests
import http.cookies
from datetime import datetime

class mysqldb():
    def __init__(self,host='',port=3306,db='',user='',passwd='',charset='utf8'):
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd,charset=charset,read_timeout=10,write_timeout=10)
        self.cur = self.conn.cursor(cursor = pymysql.cursors.DictCursor)

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

class sqlite(object):
    def __init__(self,sqlcmd,db_name):
        self.sqlcmd = sqlcmd
        self.db_name = db_name

    def run(self):
        return self.sqlcommit()

    def sqlcommit(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            sqlex=cursor.execute(self.sqlcmd)
            sqlrc=cursor.rowcount
            sqlfa=cursor.fetchmany(200)
            cursor.close()
            conn.commit()
            conn.close()
            if self.sqlcmd.split(" ")[0]=='select':
                return sqlfa
            else:
                return sqlrc
        except Exception as error:
            return "sqlite数据库执行发生错误:"+str(error)

def  mysqlex(sqlcmd,host='',port=3306,db='',user='',passwd='',charset='utf8',args=[]):
    if host =='':
        with mysqldb() as db:
            try:
                if args!=[]:
                    db.executemany(sqlcmd,args)
                else:
                    db.execute(sqlcmd)
                if sqlcmd.split(" ")[0]=="select":
                    return db.fetchall()
                else:
                    return db.rowcount
            except Exception as error:
                return "mysql数据库执行发生错误:"+str(error)
    else:
        with mysqldb(host,port,db,user,passwd,charset) as db:
            try:
                if args!=[]:
                    db.executemany(sqlcmd,args)
                else:
                    db.execute(sqlcmd)
                if sqlcmd.split(" ")[0]=="select":
                    return db.fetchall()
                else:
                    return db.rowcount
            except Exception as error:
                return "mysql数据库执行发生错误:"+str(error)

class date_time:
    def __init__(self):
        now = datetime.now()
        self.year = now.year
        self.month = now.month
        self.day = now.day
        self.hour = now.hour
        self.minute = now.minute
        self.second = now.second
        self.now = now.strftime("%Y-%m-%d %H:%M:%S")
        self.time = now

def send_msg(title='',content='',msg_code=None,msg_url=None,touser="@all"):
    url='http://msg.msgbox.xyz/send_msg'
    data={"title":title,"content":content,'msg_code':msg_code,'url':msg_url,"touser":touser}
    r=requests.post(url,json=data,timeout=3)
    return r.text

def ding_msg(title='',content='',msg_code=None,msg_url=None):
    url='http://msg.msgbox.xyz/ding_msg'
    data={"title":title,"content":content,'msg_code':msg_code,'url':msg_url}
    r=requests.post(url,json=data,timeout=3)
    return r.text

def mprint(*args):
    if args:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), *args)

def format_cookie(cookie_str):
    cookie = http.cookies.SimpleCookie(cookie_str)
    cookie_dict = {}
    for key, morsel in cookie.items():
        cookie_dict[key] = morsel.value
    return json.dumps(cookie_dict)

def write_str(Str,File="./temp.log"):
    with open(File, 'a') as File:
        File.write(Str+"\n")
        print ("写入完成！")

def random_agent(UserAgentList):
    return UserAgentList[int(random.random()*len(UserAgentList))]

def timestamp(type=0):
    thistime = time.time()
    return int(thistime) if type==0 else int(thistime * 1000)

def md5_hex(text):
    return hashlib.md5(text.encode()).hexdigest()

def hex_to_rgb(hex_or_rgb):
    if isinstance(hex_or_rgb, str):
        hex_string = hex_or_rgb.lstrip('#')
        return tuple(int(hex_string[i:i+2], 16) for i in (0, 2, 4))
    elif isinstance(hex_or_rgb, tuple) and len(hex_or_rgb) == 3:
        return hex_or_rgb
    else:
        raise ValueError('Input must be a string in the format "#RRGGBB" or a tuple of 3 integers.')

def rgb_to_hex(rgb):
    if isinstance(rgb, str):
        rgb = tuple(map(int, (rgb.replace("(","").replace(")","")).split(',')))
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"

def gen_uid():
    return md5_hex(str(''.join(random.sample(string.ascii_letters + string.digits,18)))+str(timestamp(1)))

def link_str(str1, str2, lstr=''):
    if str(str1) == '':
        return str(str2)
    else:
        return f"{str1}{lstr}{str2}"

def find_string(string,pattern):
    return re.compile(pattern).findall(str(string))

def find_substring(string, pattern):
    """
    Find the first substring in the string that matches the pattern and return it.

    Args:
    string (str): The string to search in.
    pattern (str): The regular expression pattern to match.

    Returns:
    str or None: The first matched substring or None if no match is found.
    """
    match = re.search(pattern, string)
    if match:
        return match.group()
    else:
        return None

def get_url(string):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    url = re.findall(pattern,string)
    return url

def cut_string(string, length):
    str_len = len(string)
    list=[]
    for i in range(0, str_len, length):
        list.append(string[i:i+length])
    return list

def buityful_number(ens):
    ens=str(ens)
    ens_type='normal'
    is_digital=re.compile('^[0-9]{1,20}$').match(ens)
    if is_digital!=None:
        if len(ens)<=3:
            ens_type='999 Club'
        elif len(ens)<=4:
            ens_type='10K Club'
            if find_string(ens,'([0-9])\\1{3,}')!=[]:
                ens_type='AAAA'
            elif find_string(ens,'([0-9])\\1{2,}')!=[]:
                ens_type='AAAB'
            elif len(find_string(ens,'([0-9])\\1{1,}'))>=2:
                ens_type='AABB'
        elif len(ens)<=5:
            ens_type='100K Club'
            if find_string(ens,'([0-9])\\1{4,}')!=[]:
                ens_type='AAAAA'
            elif find_string(ens,'([0-9])\\1{3,}')!=[]:
                ens_type='AAAAB'
            elif find_string(ens,'([0-9])\\1{2,}')!=[]:
                ens_type='AAABC'
    else:
        len_ens=len(ens)
        if len_ens==3:
            ens_type='3L'
            if find_string(ens,'([0-9a-zA-Z])\\1{2,}')!=[]:
                ens_type='EEE'
        elif len_ens==4:
            ens_type='4L'
            if find_string(ens,'([0-9a-zA-Z])\\1{3,}')!=[]:
                ens_type='EEEE'
            elif find_string(ens,'([0-9a-zA-Z])\\1{2,}')!=[]:
                ens_type='EEEF'
            elif len(find_string(ens,'([0-9a-zA-Z])\\1{1,}'))>=2:
                ens_type='EEFF'
    return str(ens_type).lower()

def get_this_ip():
    try:
        my_ip = requests.get('http://ip.42.pl/raw').text
    except Exception as e1:
        try:
            my_ip = requests.get('http://jsonip.com').json()['ip']
            mprint(f'Error in get_this_ip: {e1}')
        except Exception as e2:
            my_ip = requests.get('https://api.ipify.org/?format=json').json()['ip']
            mprint(f'Error in get_this_ip: {e1}, {e2}')
    return my_ip

mprint(get_this_ip())