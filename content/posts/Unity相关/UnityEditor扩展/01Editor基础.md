---
title: "Editor基础"
date: 2023-10-20
draft: false
---


# Editor基础

Unity对于编辑器扩展提供了非常大的空间，可以让开发者在编辑器中定制开发各种功能。

首先要理解Unity对于编辑器开发的一些框架。只有符合框架规范的代码才可以被Unity接受。首先最主要的便是Editor文件夹。Editor文件夹对于Unity来说是一个特殊的文件夹，其跟Plugin，Resources等一样是一个特殊的文件夹。具体内容可以参考官方文档：

https://docs.unity3d.com/2021.3/Documentation/Manual/SpecialFolders.html

简单来说，对于Editor文件夹内的脚本，Unity会默认编译成名为Assembly-CSharp-Editor的程序集，进而排除在运行时代码之外。这也是理所应当，因为编辑器主要针对的是开发用的Editor环境，其必然不能跟运行逻辑有所纠葛。

<center><img src="../01.assets/p1.png"></center>


除此之外对于Editor文件夹还有几点：

* 对于名为Editor文件夹放在任何位置都可以，只要是这个名字之下的都会被包含进目标程序集。
* 但是其放置的位置会受到Unity编译顺序的影响，这个可以见官方文档。例如Plugin中的Editor文件夹会被放进Assembly-CSharp-Editor-firstpass程序之中，在前一步编译。

对于使用了UnityEditor空间的脚本我们都需要放置在Editor文件夹下，不然会编译不通过。而UnityEditor空间内的函数则是我们扩展编辑器的主要接口。

# 常用属性结构

