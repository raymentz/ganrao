#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########## prepare ##########

# install mysql-connector-python:
# pip3 install mysql-connector-python --allow-external mysql-connector-python

import mysql.connector

# change root password to yours:
conn = mysql.connector.connect(user='root', password='password', database='test')
# ENGINE=InnoDB DEFAULT CHARSET=utf8
cursor = conn.cursor()
# a = "江门"
# a = a.decode("gbk").encode("utf-8")
# 创建user表:
#cursor.execute('create table ganrao (id varchar(20) primary key, zhenqu varchar(20), ganraoquyu varchar(20), date varchar(20),ganraodizhi varchar(20),lianxi varchar(20),jingdu varchar(20),weidu varchar(20),chuliqingkuang varchar(20),wanchengchuli varchar(20))')
#cursor.execute('insert into user (id, name) values (%s, %s)', ('61', '风华绝都爱剪辑'))
# 提交事务:
conn.commit()
cursor.close()

