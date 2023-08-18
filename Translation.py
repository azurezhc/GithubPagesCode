# -*- coding: utf-8 -*-
# Author: zhanghongchi
# 本Python 主要用来替换文档中的html img 路径
# 因为hugo会把本地图片资源包装在上一层 故直接采用ptyhon 预处理的方式来处理文档
# 为了不重复修改相对路径 对于img src存在../的文档不做处理

import os
import re

rootdir = 'content'


pattern = re.compile(r'<img src\s*=(.*?)>')


def ReplaceImgPath(content):
    print(content)
    image_path = content.group(1)
    if image_path.startswith('"../'):
        return content
    else:
        return '<img src="../' + image_path[1:-1] + '">'


for dirpath, dirname, filenames in os.walk(rootdir):
    for filepath in filenames:
        # 检测md结尾文档
        if filepath.endswith('.md'):
            # 拼接文件路径
            file = os.path.join(dirpath, filepath)
            print(file)
            # 打开文件
            f = open(file, 'r+', encoding='utf-8')
            # 读取文件内容
            content = f.read()
            # 替换文档中的图片路径
            after_content = re.sub(pattern, ReplaceImgPath, content)
            # content 写入文件
            f.seek(0)
            f.write(after_content)
            f.close()
