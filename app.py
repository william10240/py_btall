#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request
import re,os,ssl,sys
import logging
logging.basicConfig(
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', level=logging.INFO)

APP_PATH = os.path.dirname(os.path.abspath(__file__))
PHOTO_PATH = os.path.join(APP_PATH, 'photos')
if not os.path.exists(PHOTO_PATH):
    os.mkdir(PHOTO_PATH)

# <img src="https://www.btbttpic.com/upload/attach/000/107/ab65d09a88ea1f662a4de07c03a32307.jpg" width="800" height="1170">
ptImg = re.compile(
    r'https://www.btbttpic.com/upload/attach.*?\.jpg', re.I | re.S | re.M)
ptTitle = re.compile(
    r'zip\.gif.*?>btbtt06.com(.*?)</a>', re.I | re.S | re.M)
ptAjax = re.compile(
    r'<a href="http://www.btbtt08.com/attach-dialog-(.*?)-ajax-1.htm" class="ajaxdialog" ajaxdialog', re.I)


def opener():
        return request.build_opener()

def json(code, msg='', data='', callback=None):
    json_data = {
        'code': code,
        'msg': msg,
        'data': data
    }
    return json_data


def _domatch(rec, htmls):
    mh = rec.findall(htmls)
    if mh :
        return mh
    else:
        return ''


def _request(url, tims=0):
    logging.info("request:"+url)
    try:
        res = opener().open(url, timeout=20)
        html = res.read()
    except Exception as e:
        return json(-1, '网络错误:' + str(e))
        # tims += 1
        # if tims == 3:
        #     return json(-1, '网络错误')
        # return _request(url, tims)

    html = html.decode('UTF-8')


    return html


def _saveFile(src, fname):
    
    fpath = os.path.join(PHOTO_PATH, fname)

    if os.path.exists(fpath):
        return json(0, '文件已存在')

    try:
        rs = opener().open(src)
        rs = rs.read()
    except Exception as e:
        return json(-1, '网络错误:' + str(e))


    try:
        with open(fpath, 'wb') as op:
            op.write(rs)
    except Exception as e:
        return json(-1, '保存文件失败:' + str(e))

    return json(0, '保存成功')


def main(src):
    html = _request(src)
    src = _domatch(ptImg, html)
    filename = _domatch(ptTitle, html)[0]
    # print(filename)
    ajax = _domatch(ptAjax, html)[0]
    # print(ajax)

    logging.info("开始保存:" + filename)
    ajaxstr = _saveFile(
        "http://www.btbtt08.com/attach-download-"+ajax+".htm", filename)
    logging.info(ajaxstr)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 2 :
        main(sys.argv[1])
    else:
        logging.error("参数不正确")
