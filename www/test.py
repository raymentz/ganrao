#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import mysql.connector
import hashlib
import pymysql
import os
import xlrd
import xlwt
from datetime import date, timedelta
from xlwt import *
import time
import json
import re
from flask import jsonify
import string
from datetime import datetime


# from sqlalchemy import Column, String, create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# def set_style(name,height,bold=False):
#     style = xlwt.XFStyle() # 初始化样式
#     font = xlwt.Font() # 为样式创建字体
#     font.name = name # 'Times New Roman'
#     font.bold = bold  #是否加粗，默认不加粗
#     font.color_index = 4
#     font.height = height  #定义字体大小
#     style.font = font
#     alignment = xlwt.Alignment() #创建居中
#     alignment.horz = xlwt.Alignment.HORZ_CENTER #可取值: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
#     alignment.vert = xlwt.Alignment.VERT_CENTER # 可取值: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
#     style.alignment = alignment # 文字居中


# Base = declarative_base()
#
#
# class ganrao(Base):
#     __tablename__ = 'ganrao'
#     id = Column(String(20), primary_key=True)
#     zhenqu = Column(String(20))
#     ganraoquyu = Column(String(20))
#     date = Column(String(20))
#     ganraodizhi = Column(String(40))
#     lianxi = Column(String(20))
#     jingdu = Column(String(20))
#     weidu = Column(String(20))
#     chuliqingkuang = Column(String(40))
#     wanchengchuli = Column(String(20))
#
# engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# class MyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, numpy.integer):
#             return int(obj)
#         elif isinstance(obj, numpy.floating):
#             return float(obj)
#         elif isinstance(obj, numpy.ndarray):
#             return obj.tolist()
#         else:
#             return super(MyEncoder, self).default(obj)

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
    cursor = conn.cursor()
    cursor.execute('select * from ganrao where wanchengchuli=%s order by chulijinjichengdu desc , date asc limit 10',('否',))
    results = cursor.fetchall()
    xinxi = []
    for row in results:
        xinxi.append(row)
    print(xinxi)
    return render_template('home.html',xinxi=xinxi)

@app.route('/chaxun', methods=['GET'])
def chaxun1():
    return render_template('chaxun.html')

@app.route('/chaxun', methods=['POST'])
def chaxun():
    if request.form['submit2'] == 'submit2':
        id2 = request.form['id2']
        ganraoquyu2 = request.form['ganraoquyu2']
        weidu2 = request.form['weidu2']
        jingdu2 = request.form['jingdu2']

        conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
        cursor = conn.cursor()

        try:

            cursor.execute('select * from ganrao where id = %s or ganraoquyu = %s or jingdu= %s or weidu= %s ',
                               (id2, ganraoquyu2, jingdu2, weidu2))
            # cursor.execute('select * from ganrao where id = %s ',(id2,))
            results = cursor.fetchall()
            print(results)
            if results ==[]:
                with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n查询失败，没有该条信息\n')
                return render_template('chaxun.html', message2='查询失败')
            else:
                for row in results:
                    id = row[0]
                    zhenqu = row[1]
                    ganraoquyu = row[2]
                    date = row[3]
                    ganraodizhi = row[4]
                    lianxi = row[5]
                    jingdu = row[6]
                    weidu = row[7]
                    chuliqingkuang = row[8]
                    wanchengchuli = row[9]
                    chulijinjichengdu = row[10]
                with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\nID为：' + id + '的一条信息查询成功\n')
                return render_template('chaxun.html', message1='查询成功', id2=id, zhenqu2=zhenqu,ganraoquyu2=ganraoquyu, date2=date, ganraodizhi2=ganraodizhi, lianxi2=lianxi,jingdu2=jingdu, weidu2=weidu, chuliqingkuang2=chuliqingkuang,wanchengchuli2=wanchengchuli,chulijinjichengdu2=chulijinjichengdu)

        except Exception as e:
            print('执行过程中发生了异常', e)
            conn.rollback()
        finally:
            conn.commit()
            conn.close()


@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    username3 = request.form['username']
    password3 = request.form['password']
    md5 = hashlib.md5()
    md5.update(password3.encode('utf-8'))
    password3 = md5.hexdigest()
    conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
    cursor = conn.cursor()
    try:
        cursor.execute('select * from user where username= %s ',(username3, ))
        results = cursor.fetchall()
        for row in results:
            username2 = row[0]
            password2 = row[1]
            realname2 = row[4]
        if cursor.rowcount>=1:
            if username3 == username2 and password3==password2:
                with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n登陆成功，欢迎'+realname2+'的使用！\n' )
                return render_template('form.html', message='登陆成功，欢迎'+realname2+'的使用！')
                # f = open('rizhi.txt', 'w')
                # f.write('登陆成功，欢迎'+username3+'的使用！'+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                # f.close()

            else:
                with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n'+username3+'登陆失败，账号或密码不正确\n')
                return render_template('form.html', message='登陆失败，账号或密码不正确', message1='no')
        else:
            with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n' + username3 + '登陆失败，账号或密码不正确\n')
            return render_template('form.html', message='登陆失败，账号或密码不正确', message1='no')
    except Exception as e:
        print('执行过程中发生了异常', e)
        conn.rollback()
    finally:
        conn.commit()
        conn.close()


@app.route('/zhuce', methods=['GET'])
def zhuce1():
    return render_template('zhuce.html')

@app.route('/zhuce', methods=['POST'])
def zhuce():
    username = request.form['username']
    password = request.form['password']
    phone = request.form['phone']
    email = request.form['email']
    realname1 = request.form['realname']
    quanxian1 = request.form['quanxian']

    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    password1 = md5.hexdigest().encode('utf-8')
    print(username, password1,phone,email,realname1,quanxian1)
    conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
    cursor = conn.cursor()
    cursor.execute('insert into user (username, password, phone,email,realname,quanxian) values (%s, %s,%s, %s,%s,%s)', (username, password1,phone,email,realname1,quanxian1))
    conn.commit()
    cursor.close()
    with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n' + realname1 + '注册成功\n')
    return render_template('zhuce.html', message2='注册成功')





@app.route('/xinxiluru', methods=['GET'])
def informations_form():
    return render_template('xinxiluru.html')

@app.route('/xinxiluru', methods=['POST'])
def informations():
    #submit1 = request.form['submit1']
    #submit2 = request.form['submit2']
    if request.form['submit1'] == 'submit1':
        id1 = request.form['id1']
        zhenqu1 = request.form['zhenqu1']
        ganraoquyu1 = request.form['ganraoquyu1']
        date1 = request.form['date1']
        ganraodizhi1 = request.form['ganraodizhi1']
        lianxi1 = request.form['lianxi1']
        jingdu1 = request.form['jingdu1']
        weidu1 = request.form['weidu1']
        chuliqingkuang1 = request.form['chuliqingkuang1']
        wanchengchuli1 = request.form['wanchengchuli1']
        ganraochangjing1 = request.form['ganraochangjing']
        jinjichengdu1 = request.form['jinjichengdu']
        wenti1 = request.form['wenti1']
        wenti2 = request.form['wenti2']
        wenti3 = request.form['wenti3']
        wenti4 = request.form['wenti4']
        wenti5 = request.form['wenti5']
        wenti6 = request.form['wenti6']
        wenti7 = request.form['wenti7']
        print(ganraochangjing1)

        conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
        cursor = conn.cursor()


        try:
            if wenti1== 'yes':
                q1 = 30
            else:
                q1 = 0
            if wenti2== 'yes':
                q2 = 20
            else:
                q2 = 0
            if wenti3== 'yes':
                q3 = 60
            else:
                q3 = 0
            if wenti4== 'yes':
                q4 = 60
            else:
                q4 = 0
            if wenti5== 'yes':
                q5 = 30
            else:
                q5 = 0
            if wenti6== 'yes':
                q6= 20
            else:
                q6 = 0
            if wenti7== 'yes':
                q7 = 80
            else:
                q7 = 0
            if chuliqingkuang1== '100':
                w8 = '是'
            else:
                w8 = '否'
            chulijinjichengdu1 = int(jinjichengdu1)*0.5+(q1+q2+q3+q4+q5+q6+q7)*0.5+int(ganraochangjing1)*0.5
            if wenti1=='yes' or wenti5== 'yes' :
                answer1 = '△请中心协助入内排查，通知无线电委员会按非法行为进行现场取缔处理。'
            else:
                answer1 =''
            if wenti3== 'yes' or wenti4== 'yes' or wenti7== 'yes' :
                answer2 = '△请维护优化人员处理设备故障，优化天线角度，检查核对参数配置。'
            else:
                answer2 =''
            if wenti2== 'yes' or wenti6== 'yes'  :
                answer3 = '△请中心派人与政府或私人企业机构协调商量处理。'
            else:
                answer3 =''

            cursor.execute('insert into ganrao (id, zhenqu, ganraoquyu, date, ganraodizhi, lianxi, jingdu, weidu, chuliqingkuang, wanchengchuli,chulijinjichengdu) values (%s, %s,%s, %s, %s, %s,%s, %s,%s, %s,%s)',(id1, zhenqu1, ganraoquyu1, date1, ganraodizhi1, lianxi1, jingdu1, weidu1, chuliqingkuang1, wanchengchuli1,chulijinjichengdu1))
            with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\nID为：'+id1+'的一条信息录入成功\n')
            return render_template('xinxiluru.html', message='录入成功',message1=answer1,answer2=answer2,answer3=answer3)
        except Exception as e:
            print('执行过程中发生了异常', e)
            conn.rollback()
        finally:
            conn.commit()
            conn.close()

@app.route('/xiugai', methods=['GET'])
def xiugai1():
    return render_template('xiugai.html')

@app.route('/xiugai', methods=['POST'])
def xiugai():
    id1 = request.form['id1']
    ganraoquyu1 = request.form['ganraoquyu1']
    ganraodizhi1 = request.form['ganraodizhi1']
    jingdu1 = request.form['jingdu1']
    weidu1 = request.form['weidu1']
    chuliqingkuang1 = request.form['chuliqingkuang1']

    conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
    cursor = conn.cursor()
    try:
        cursor.execute('select * from ganrao where id= %s ', (id1,))
        results = cursor.fetchall()
        for row in results:
            id1 = row[0]
            chuliqingkuang2 = row[8]
        if cursor.rowcount>=1:
            #cursor.execute('update ganrao set ganraoquyu = %s ganraodizhi = %s jingdu = %s weidu = %s chuliqingkuang = %s where id = %s', (ganraoquyu1,ganraodizhi1, jingdu1,weidu1,chuliqingkuang2+chuliqingkuang1,id1))
            if len(ganraoquyu1) != 0 :
                cursor.execute('update ganrao set ganraoquyu = %s where id = %s',(ganraoquyu1,id1 ))
            if len(ganraodizhi1) != 0 :
                cursor.execute('update ganrao set ganraodizhi = %s where id = %s', (ganraodizhi1,id1))
            if len(jingdu1) != 0:
                cursor.execute('update ganrao set jingdu = %s where id = %s', (jingdu1, id1))
            if len(weidu1) != 0:
                cursor.execute('update ganrao set weidu = %s where id = %s', (weidu1, id1))
            if len(chuliqingkuang1) != 0:
                cursor.execute('update ganrao set chuliqingkuang = %s where id = %s', (chuliqingkuang2+chuliqingkuang1, id1))
            with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\nID为：'+id1+'的一条信息修改成功\n')
            return render_template('xiugai.html', message='修改成功')
        else:
            with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n没有ID为：'+id1+'的一条信息，请重新录入信息\n')
            return render_template('xiugai.html', message='没有该条信息，请重新录入信息', message1='no')
    except Exception as e:
        print('执行过程中发生了异常', e)
        conn.rollback()
    finally:
        conn.commit()
        conn.close()


@app.route('/shangchuan', methods=['GET'])
def shangchuan1():
    return render_template('shangchuan.html')

@app.route('/shangchuan', methods=['POST'])
def shangchuan():
    if request.method == 'POST':
        # file = request.files.get('file_upload')
        # filename =file.filename
        # print(filename)
        # return render_template('shangchuan.html', message='上传成功')
        try:
            # form = UploadExcelForm(request.POST, request.FILES)
            # if form.is_valid():
            #     excel = xlrd.open_workbook( filename=None, file_contents=request.FILES['file_upload'].read())

            upload_file = request.files.get('file_upload')
            # filename = file.filename
            # print(filename)
            # str = file[0]
            # d= eval(str)
            # f = open(os.path.join('static', file.name), 'wb')
            # for chunk in file.chunks(chunk_size=1024):
            #     f.write(chunk)
            # f.close()
            # upload_file = request.files['image01']
            if upload_file :#and allowed_file(upload_file.filename):
                filename = upload_file.filename  #secure_filename(upload_file.filename)
                print(filename)
                #upload_file.save(os.path.join('/Users/Rayment/PycharmProjects/Interferencesources-app/www/static', filename))

                file1 = os.path.join('/Users/Rayment/PycharmProjects/Interferencesources-app/www/static', filename)
                upload_file.save(file1)
            #     return 'hello, ' + request.form.get('name', 'little apple') + '. success'
            # else:
            #     return 'hello, ' + request.form.get('name', 'little apple') + '. failed'
            excel = xlrd.open_workbook(file1)  # 打开xlsx文件,返回一个对象
            sheet = excel.sheet_by_index(0)  # 获取第一个sheet表格
            nrows = sheet.nrows
            newcols = sheet.ncols
            conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
            cursor = conn.cursor()
            newrows = 0
            for i in range(1,nrows):
                item = sheet.row_values(i)
                id1 = item[0]
                zhenqu1 = item[1]
                ganraoquyu1 = item[2]
                date1 = date(1900, 1, 1) + timedelta(days=int(item[3])-1)
                ganraodizhi1 = item[4]
                lianxi1 = int(item[5])
                jingdu1 = item[6]
                weidu1 = item[7]
                chuliqingkuang1 = item[8]
                wanchengchuli1 = item[9]
                chulijinjichengdu1 = item[10]
                cursor.execute('select * from ganrao where id= %s ', (id1,))
                results = cursor.fetchall()
                if results:
                    continue
                else:
                    cursor.execute('insert into ganrao (id, zhenqu, ganraoquyu, date, ganraodizhi, lianxi, jingdu, weidu, chuliqingkuang, wanchengchuli,chulijinjichengdu) values (%s, %s,%s, %s, %s, %s,%s, %s,%s, %s,%s)',(id1, zhenqu1, ganraoquyu1, date1, ganraodizhi1, lianxi1, jingdu1, weidu1, chuliqingkuang1,wanchengchuli1,chulijinjichengdu1))
                    newrows = newrows+1
            if newrows==0:
                newcols=0
            with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n成功上传了'+str(newrows)+'行'+str(newcols)+'列信息\n')
            return render_template('shangchuan.html', message='上传成功')
            # for row in range(sheet.nrows):
            #     print(row)
            #     args = sheet.row_values(row)
            #     print(args)
            #     print(type(args))
            #     if row == 0:
            #         continue
            #     if args[1] is None or args[1] == '':
            #         continue
            #     cursor.execute(cursor.execute('insert into ganrao (id, zhenqu, ganraoquyu, date, ganraodizhi, lianxi, jingdu, weidu, chuliqingkuang, wanchengchuli) values (%s, %s,%s, %s, %s, %s,%s, %s,%s, %s)',args=args))

        except Exception as e:
            print('执行过程中发生了异常', e)
            with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n上传失败\n')
            return render_template('shangchuan.html', message='上传失败')
            conn.rollback()
        finally:
            conn.commit()
            conn.close()
    #filename = request.form('file_upload').name
    # form = UploadExcelForm(request.POST, request.FILES)
    # if form.is_valid():
    #     wb = xlrd.open_workbook(
    #         filename=None, file_contents=request.FILES['excel'].read())

    # filename = request.form['filename']


@app.route('/daochu', methods=['GET'])
def daochu1():
    return render_template('daochushuju.html')


@app.route('/daochu', methods=['POST'])
def daochu():
    try:
        name = request.form['file_name']
        zhenqu1 = request.form['zhenqu1']
        date1 = request.form['date1']
        date2 = request.form['date2']
        filename = name + '.xls'  # 定义Excel名字
        filename1 = os.path.join('/Users/Rayment/Desktop', filename)
        wbk = xlwt.Workbook()  # 实例化一个Excel
        sheet1 = wbk.add_sheet('sheet1', cell_overwrite_ok=True)  # 添加该Excel的第一个sheet，如有需要可依次添加sheet2等
        fileds = [u'ID编号', u'镇区',u'干扰区域', u'日期',u'干扰地址', u'联系',u'经度', u'纬度',u'处理情况', u'是否完成处理',u'处理紧急程度']  # 直接定义结果集的各字段名
        conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
        cursor = conn.cursor()
        cursor.execute('select id,zhenqu,ganraoquyu,date,ganraodizhi,lianxi,jingdu,weidu,chuliqingkuang,wanchengchuli,chulijinjichengdu  from ganrao where  zhenqu =%s and date>=%s and date<=%s', (zhenqu1,date1,date2 ))
        #execude_sql(1024)  # 调用函数执行SQL，获取结果集
        results = cursor.fetchall()
        newrows = 0
        for i in range(0, len(fileds)):  # 写入字段信息
            sheet1.write(0, i, fileds[i])
        for row in range(1, len(results) + 1):   # 写入SQL查询数据
            for col in range(0, len(fileds)):
                sheet1.write(row, col, results[row - 1][col]) # ,set_style('宋体','200',True)
            newrows = newrows+1
        wbk.save(filename1)  # 保存Excel
        with open('/Users/Rayment/Desktop/rizhi.txt', 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '\n成功导出了' + str(newrows) + '行' + str(len(fileds)) + '列信息\n')
        return render_template('daochushuju.html', message='导出成功')
    except Exception as e:
        print('执行过程中发生了异常', e)
        return render_template('daochushuju.html', message='导出失败')
        conn.rollback()
    finally:
        conn.commit()
        conn.close()

@app.route('/rizhi', methods=['GET'])
def rizhi1():
    return render_template('rizhi.html')


@app.route('/rizhi', methods=['POST'])
def rizhi():
    with open('/Users/Rayment/Desktop/rizhi.txt', 'r') as f:  # 打开文件
        lines = f.readlines()  # 读取所有行
        lines1 = lines[-1]  # 取最后一行
        lines2 = lines[-2]
        lines3 = lines[-3]
        lines4 = lines[-4]
        lines5 = lines[-5]
        lines6 = lines[-6]
        lines7 = lines[-7]
        lines8 = lines[-8]
        lines9 = lines[-9]
        lines10 = lines[-10]
    return render_template('rizhi.html', message='查询最近日志成功',lines1=lines1,lines2=lines2,lines3=lines3,lines4=lines4,lines5=lines5,lines6=lines6,lines7=lines7,lines8=lines8,lines9=lines9,lines10=lines10)


# # print(zhenqu1,ganraoquyu1,date1,ganraodizhi1,lianxi1,jingdu1,weidu1,chuliqingkuang1,wanchengchuli1)
   # #  # 创建新User对象:
   #  new_ganrao = ganrao(id=id1, zhenqu=zhenqu1, ganraoquyu=ganraoquyu1, date=date1, ganraodizhi=ganraodizhi1, galianxi=lianxi1, jingdu=jingdu1, weidu=weidu1, chuliqingkuang=chuliqingkuang1, wanchengchuli=wanchengchuli1)
   #  # 添加到session:
   #  session.add(new_ganrao)
   #  # 提交即保存到数据库:
   #  session.commit()
   #  #关闭session:
   #  session.close()

# @app.route('/ditu', methods=['GET','POST'])
# def ditu():
#     return render_template('gaodeapi.html')

@app.route('/ditu', methods=['GET'])
def ditu1():
    return render_template('gaodeapi.html')


@app.route('/ditu', methods=['POST'])
def ditu():
    id2 = request.form['id2']
    conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
    cursor = conn.cursor()

    try:
        cursor.execute('select * from ganrao where id = %s ',(id2, ))
        results = cursor.fetchall()
        print(results)
        for row in results:
            id1 = row[0]
            zhenqu1 = row[1]
            ganraoquyu1 = row[2]
            date1 = row[3]
            ganraodizhi1 = row[4]
            lianxi1 = row[5]
            jingdu1 = row[6]
            weidu1 = row[7]
            chuliqingkuang1 = row[8]
            wanchengchuli1 = row[9]
            chulijinjichengdu1 = row[10]
        data = dict(id=id1,zhenqu=zhenqu1,ganraoquyu=ganraoquyu1,date=date1,ganraodizhi=ganraodizhi1,lianxi=lianxi1,jingdu=jingdu1,weidu=weidu1,chuliqingkuang=chuliqingkuang1,wanchengchuli=wanchengchuli1,chulijinjichengdu=chulijinjichengdu1 )
        data1 = json.dumps(data)
    except Exception as e:
        print('执行过程中发生了异常', e)
        conn.rollback()
    finally:
        conn.commit()
        conn.close()
        return render_template('gaodeapi.html',data = data1,id2 = id1, zhenqu2 = zhenqu1, ganraoquyu2 = ganraoquyu1, date2 = date1,ganraodizhi2 = ganraodizhi1, lianxi2 = lianxi1, jingdu2 = jingdu1, weidu2 = weidu1,chuliqingkuang2 = chuliqingkuang1, wanchengchuli2 = wanchengchuli1,chulijinjichengdu2 = chulijinjichengdu1)
    # data = data1, id = json.dumps(id1),
    # id2 = id, zhenqu2 = zhenqu, ganraoquyu2 = ganraoquyu, date2 = date,
    # ganraodizhi2 = ganraodizhi, lianxi2 = lianxi, jingdu2 = jingdu, weidu2 = weidu,
    # chuliqingkuang2 = chuliqingkuang, wanchengchuli2 = wanchengchuli,
    # chulijinjichengdu2 = chulijinjichengdu

# @app.route('/tubiao', methods=['GET','POST'])
# def zhuzhuangtu():
#     return render_template('tubiao.html')




@app.route('/biao', methods=['GET','POST'])
def zhuzhuangtu1():
    conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
    cursor = conn.cursor()
    cursor.execute('select * from ganrao where zhenqu = %s and wanchengchuli = %s ',('禅城','是', ))
    values1 = cursor.fetchall()
    y1 = len(values1)
    cursor.execute('select * from ganrao where zhenqu = %s and wanchengchuli = %s  ',('南海', '是',))
    values2 = cursor.fetchall()
    y2 = len(values2)
    cursor.execute('select * from ganrao where zhenqu = %s and wanchengchuli = %s  ',('顺德', '是',))
    values3 = cursor.fetchall()
    y3 = len(values3)
    cursor.execute('select * from ganrao where zhenqu = %s and wanchengchuli = %s  ',('三水', '是',))
    values4 = cursor.fetchall()
    y4 = len(values4)
    cursor.execute('select * from ganrao where zhenqu = %s and wanchengchuli = %s  ',('高明', '是',))
    values5 = cursor.fetchall()
    y5 = len(values5)
    cursor.execute('select * from ganrao where zhenqu = %s and wanchengchuli = %s  ',('禅城', '否',))
    values6 = cursor.fetchall()
    n1 = len(values6)
    cursor.execute('select * from ganrao where zhenqu = %s and wanchengchuli = %s  ',('南海', '否',))
    values7= cursor.fetchall()
    n2 = len(values7)
    cursor.execute('select * from ganrao where zhenqu = %s and wanchengchuli = %s  ',('顺德', '否',))
    values8 = cursor.fetchall()
    n3 = len(values8)
    cursor.execute('select * from ganrao where zhenqu = %s and wanchengchuli = %s  ',('三水', '否',))
    values9 = cursor.fetchall()
    n4 = len(values9)
    cursor.execute('select * from ganrao where zhenqu = %s and wanchengchuli = %s  ',('高明', '否',))
    values10 = cursor.fetchall()
    n5 = len(values10)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s  ', ('2018-04-01','2018-04-30' ,'否',))
    values11 = cursor.fetchall()
    x1 = len(values11)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s  ',
                   ('2018-03-01', '2018-03-31', '否',))
    values12 = cursor.fetchall()
    x2 = len(values12)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s  ',
                   ('2018-02-01', '2018-02-28', '否',))
    values13 = cursor.fetchall()
    x3 = len(values13)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s  ',
                   ('2018-01-01', '2018-01-31', '否',))
    values14 = cursor.fetchall()
    x4 = len(values14)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s  ',
                   ('2017-12-01', '2017-12-31', '否',))
    values15 = cursor.fetchall()
    x5 = len(values15)
    y6=y1+y2+y3+y4+y5
    n6=n1+n2+n3+n4+n5
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-04-01','2018-04-30', '否','禅城',))
    resukt1 = cursor.fetchall()
    a1 = len(resukt1)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-04-01','2018-04-30', '否','南海',))
    resukt2 = cursor.fetchall()
    a2 = len(resukt2)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-04-01','2018-04-30', '否','顺德',))
    resukt3 = cursor.fetchall()
    a3 = len(resukt3)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s  ',
                   ('2018-04-01','2018-04-30', '否','三水',))
    resukt4 = cursor.fetchall()
    a4 = len(resukt4)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-04-01','2018-04-30', '否','高明',))
    resukt5 = cursor.fetchall()
    a5 = len(resukt5)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-03-01', '2018-03-31', '否','禅城',))
    resukt6 = cursor.fetchall()
    a6 = len(resukt6)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-03-01', '2018-03-31', '否','南海',))
    resukt7 = cursor.fetchall()
    a7 = len(resukt7)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-03-01', '2018-03-31', '否','顺德',))
    resukt8 = cursor.fetchall()
    a8 = len(resukt8)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-03-01', '2018-03-31', '否','三水',))
    resukt9 = cursor.fetchall()
    a9 = len(resukt9)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-03-01', '2018-03-31', '否','高明',))
    resukt10 = cursor.fetchall()
    a10 = len(resukt10)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-02-01', '2018-02-28', '否','禅城',))
    resukt11 = cursor.fetchall()
    a11 = len(resukt11)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-02-01', '2018-02-28', '否','南海',))
    resukt12 = cursor.fetchall()
    a12 = len(resukt12)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-02-01', '2018-02-28', '否','顺德',))
    resukt13 = cursor.fetchall()
    a13 = len(resukt13)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-02-01', '2018-02-28', '否','三水',))
    resukt14 = cursor.fetchall()
    a14 = len(resukt14)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-02-01', '2018-02-28', '否','高明',))
    resukt15 = cursor.fetchall()
    a15 = len(resukt15)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-01-01', '2018-01-31', '否','禅城',))
    resukt16 = cursor.fetchall()
    a16 = len(resukt16)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-01-01', '2018-01-31', '否','南海',))
    resukt17 = cursor.fetchall()
    a17 = len(resukt17)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-01-01', '2018-01-31', '否','顺德',))
    resukt18 = cursor.fetchall()
    a18= len(resukt18)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-01-01', '2018-01-31', '否','三水',))
    resukt19 = cursor.fetchall()
    a19 = len(resukt19)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2018-01-01', '2018-01-31', '否','高明',))
    resukt20 = cursor.fetchall()
    a20 = len(resukt20)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2017-12-01', '2017-12-31', '否','禅城',))
    resukt21 = cursor.fetchall()
    a21 = len(resukt21)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2017-12-01', '2017-12-31', '否','南海',))
    resukt22 = cursor.fetchall()
    a22 = len(resukt22)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2017-12-01', '2017-12-31', '否','顺德',))
    resukt23 = cursor.fetchall()
    a23 = len(resukt23)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2017-12-01', '2017-12-31', '否','三水',))
    resukt24 = cursor.fetchall()
    a24= len(resukt24)
    cursor.execute('select * from ganrao where date>=%s and date<=%s and wanchengchuli = %s and zhenqu = %s ',
                   ('2017-12-01', '2017-12-31', '否','高明',))
    resukt25 = cursor.fetchall()
    a25 = len(resukt25)
    print(a1, a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24,a25)
    print(y1, y2, y3, y4, y5, y6, n1, n2, n3, n4, n5, n6, x1, x2, x3, x4, x5)

    conn.commit()
    conn.close()
    return render_template('tubiao.html', y1=y1, y2 = y2, y3 = y3, y4 = y4, y5 = y5, y6 = y6, n1 = n1, n2 = n2, n3 = n3, n4 = n4, n5 = n5, n6 = n6,x1=x1, x2 = x2, x3 = x3,x4 = x4,x5 = x5, a1 = a1, a2 = a2, a3 = a3, a4 = a4, a5 = a5, a6 = a6, a7 = a7,a8=a8, a9 = a9, a10 = a10, a11 = a11, a12 = a12, a13 = a13, a14 = a14, a15 = a15, a16 = a16, a17 = a17, a18 = a18, a19 = a19,a20=a20, a21 = a21, a22 = a22, a23 = a23, a24 = a24, a25 = a25)

@app.route('/gongdan', methods=['GET','POST'])
def tuxing():
    conn = mysql.connector.connect(user='root', password='password', database='test', charset='utf8')
    cursor = conn.cursor()
    cursor.execute('select * from ganrao where wanchengchuli=%s order by chulijinjichengdu desc , date asc limit 3',
                   ('否',))
    results = cursor.fetchall()
    xinxi = []
    for row in results:
        xinxi.append(row)
    print(xinxi)
    gongdanid = []
    cd = []
    cd2 = []
    now = []
    L = []
    for i in range(3):
        now1 = datetime.now()
        now2 = now1.strftime('%Y-%m-%d %H:%M:%S')
        id = 'GD' + xinxi[i][0]
        L3 = '自动报障'
        if (250.0 < float(xinxi[i][10]) <= 350.0):
            L1 = '重大故障'
            B1 = 7*24*60
        elif (150.0 < float(xinxi[i][10]) <= 250.0):
            L1 = '一般故障'
            B1 = 9*24*60
        else:
            L1 = '轻微故障'
            B1 = 12*24*60
        cd.append(L1)
        cd2.append(B1)
        gongdanid.append(id)
        now.append(now2)
        L.append(L3)
    print(cd,cd2,gongdanid,now,L)
    for i in range(3):
        cursor.execute('select * from gongdan where gongdanid= %s ', (gongdanid[i],))
        result2 = cursor.fetchall()
        print(gongdanid[i], xinxi[i][1], xinxi[i][2],xinxi[i][4], xinxi[i][5], xinxi[i][6], xinxi[i][7], xinxi[i][8], cd[i], xinxi[i][3],now[i] ,cd2[i],L[i],xinxi[i][9])
        if result2:
            continue
        else:
            cursor.execute('insert into gongdan (gongdanid, zhenqu, ganraoquyu, ganraodizhi, lianxi, jingdu, weidu, chuliqingkuang, chulijinjichengdu,lurushijian,paidanshijian,chulishixian,ganraolaiyuan,wangchengchuli) values (%s, %s,%s, %s, %s, %s,%s, %s,%s, %s,%s, %s,%s,%s)',(gongdanid[i], xinxi[i][1], xinxi[i][2],xinxi[i][4], xinxi[i][5], xinxi[i][6], xinxi[i][7], xinxi[i][8], cd[i], xinxi[i][3],now[i] ,cd2[i],L[i],xinxi[i][9]))
            # cursor.execute(
            #     'insert into ganrao (id, zhenqu, ganraoquyu, date, ganraodizhi, lianxi, jingdu, weidu, chuliqingkuang, wanchengchuli,chulijinjichengdu) values (%s, %s,%s, %s, %s, %s,%s, %s,%s, %s,%s)',
            #     (id1, zhenqu1, ganraoquyu1, date1, ganraodizhi1, lianxi1, jingdu1, weidu1, chuliqingkuang1,
            #      wanchengchuli1, chulijinjichengdu1))
    cursor.execute('select * from gongdan where wangchengchuli=%s order by  paidanshijian asc, chulijinjichengdu desc limit 3',('否',))
    result1 = cursor.fetchall()
    gongdan=[]
    for row in result1:
        gongdan.append(row)
    print(gongdan)
    now4= datetime.now()
    lishi= []
    shengyu = []
    for i in range(3):
        cday = datetime.strptime(gongdan[i][10], '%Y-%m-%d %H:%M:%S')
        cmin=(now4.timestamp()- cday.timestamp())/60
        print(cday,now4,cday.timestamp(),now4.timestamp())
        # cmin=(now4-cday).min
        print(cmin)
        # cmin1 = int(cmin.strftime('%M'))
        smin=int(gongdan[i][11])-int(cmin)
        lishi.append(int(cmin))
        shengyu.append(smin)
    print(lishi,shengyu)
    conn.commit()
    conn.close()
    return render_template('gongdan.html',lishi=lishi,shengyu=shengyu,gongdan=gongdan)



if __name__ == '__main__':
    app.run()
