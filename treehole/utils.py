#!/usr/bin/env python
# -*- coding=UTF-8 -*-
# Created at Mar 20 19:50 by BlahGeek@Gmail.com

import sys
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('UTF-8')

import logging
from datetime import datetime, timedelta
from treehole.renren import RenRen
import os
from treehole.models import ContentModel, BlockIpModel
from ipaddr import IPNetwork, IPAddress

def needRecaptchar(addr, content):
    if ContentModel.objects.filter(
            ip=addr, 
            time__range=(datetime.now()-timedelta(hours=24), \
                         datetime.now())
            ).count() > 2:
        return True
    return False
    

def checkIP(addr):
    IPS = (
            IPNetwork('59.66.0.0/16'), 
            IPNetwork('166.111.0.0/16'), 
            IPNetwork('101.5.0.0/16'), 
            IPNetwork('219.223.160.0/19'), 
            # private address
            IPNetwork('127.0.0.0/8'), 
            IPNetwork('10.0.0.0/8'), 
            IPNetwork('192.168.0.0/16'), 
            )
    if BlockIpModel.objects.filter(ip=addr).count() > 0:
        return False
    return any([IPAddress(addr) in x for x in IPS])

def postRawStatu(text):
    """ Post status without number, without saving to db"""
    r = RenRen()
    r.postStatus(text)

def postStatu(text, ipaddr='127.0.0.1'):
    """ Post status, start with '#xxx', saving to db"""
    new_content = ContentModel(ip=ipaddr, 
            time=datetime.now(), 
            content=text)
    new_content.save()
    number = ContentModel.objects.count()
    text = '#THU' + str(number) + '# ' + text
    postRawStatu(text)

MSG = {
        'IP_NOT_VALID': '不允许您的IP发布', 
        'CONTENT_TOO_LONG': '状态长度应该在6-100字之间', 
        'TOO_MANY_TIMES': '每个IP相邻发布时间不能小于30分钟', 
        'PUBLISH_ERROR': '服务器错误，发布失败', 
        'RECAPTCHA_INCORRECT': '验证码错误', 
        'RECAPTCHA_NEEDED': '请输入验证码', 
        'PUBLISH_OK': '发布成功！'}

COLORS = [
        ('#1abc9c', '#16a085'), 
        ('#2ecc71', '#27ae60'), 
        ('#3498DB', '#2980B9'), 
        ('#9B59B6', '#8E44AD'), 
        ('#34495E', '#2C3E50'), 
        ('#F1C40F', '#F39C12'), 
        ('#E67E22', '#D35400'), 
        ('#E74C3C', '#C0392B'), 
        ('#95A5A6', '#7F8C8D')
        ]
