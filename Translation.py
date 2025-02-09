# -*- coding: utf-8 -*-
# Author: zhanghongchi
# 1 本Python 主要用来替换文档中的html img 路径
# 因为hugo会把本地图片资源包装在上一层 故直接采用ptyhon 预处理的方式来处理文档
# 为了不重复修改相对路径 对于img src存在../的文档不做处理
# 2 附加修复hugo的内置公式问题 需要添加 <raw>short code</raw>

import os
import re


# 1--替换img 路径操作
img_pattern = re.compile(r"<img src\s*=(.*?)>")


def ReplaceImgPath(content):
    return re.sub(img_pattern, ReplaceImgPathFunction, content)


def ReplaceImgPathFunction(content):
    # print(content)
    image_path = content.group(1)
    image_path = image_path.strip().strip('"')
    if image_path.startswith("../"):
        return content.group()

    return '<img src="../' + image_path + '">'


# 2--替换公式$$ 符号操作
equation_pattern = re.compile(
    r"(\{\{< raw >\}\})?(\$\$?[\s\S]+?\$\$?)(\{\{< /raw >\}\})?"
)


def ReplaceKatexRaw(content):
    return re.sub(equation_pattern, ReplaceKatexRawFunction, content)


def ReplaceKatexRawFunction(content):
    katex_content = content.group(2)
    return r"{{< raw >}}" + katex_content + r"{{< /raw >}}"


rootdir = "content"
rootdir_path = "."


# 文件相关操作
def DoTargetFile(filepath, replace_func_list):
    print(filepath)
    # 检测md结尾文档
    if filepath.endswith(".md"):
        # 打开文件
        f = open(filepath, "r+", encoding="utf-8")
        # 读取文件内容
        content = f.read()
        # 替换文档中的图片路径
        for func in replace_func_list:
            content = func(content)
        # content 写入文件
        f.seek(0)
        f.write(content)
        f.close()


def ScanContentFile(replace_func_list):
    for dirpath, dirname, filenames in os.walk(rootdir):
        for filepath in filenames:
            # 检测md结尾文档
            if filepath.endswith(".md"):
                # 拼接文件路径
                file = os.path.join(dirpath, filepath)
                print(file)
                # 打开文件
                f = open(file, "r+", encoding="utf-8")
                # 读取文件内容
                content = f.read()
                # 替换文档中的图片路径
                for func in replace_func_list:
                    content = func(content)
                # content 写入文件
                f.seek(0)
                f.write(content)
                f.close()


## 针对目标文件列表进行指定操作
def ScanTargetFileList():
    # 文件路径
    file_list = [
    ]

    # 文件夹路径
    directory_list = [
        "content/posts/Unity相关",
    ]

    # 操作方式
    func_list = [ReplaceImgPath, ReplaceKatexRaw]

    for file_path in file_list:
        DoTargetFile(os.path.join(rootdir_path, file_path), func_list)

    # 便利Director下md文件
    for dir_root_path in directory_list:
        dir_path = os.path.join(rootdir_path, dir_root_path)
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if not f.endswith(".md"):
                    continue

                file_path = os.path.join(root, f)
                DoTargetFile(file_path, func_list)


if __name__ == "__main__":
    print("Start Replace Tool")

    # ScanContentFile()
    # DoTargetFile(os.path.join(rootdir_path, "content/posts/程序动画/01插值研究.md"))
    ScanTargetFileList()
