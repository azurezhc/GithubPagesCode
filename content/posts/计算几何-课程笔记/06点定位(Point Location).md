---
title: "计算几何课程"
draft: false
date: 2023-08-25
---

# 06点定位(Point Location)

[计算几何-笔记目录](./计算几何-笔记大纲.md)


从本章之后的部分主要关注于在线算法部分。在线算法即指，输入没有一次性给出所有输入，而是随着时间逐步给出。其中点定位PointLocation是其中比较基础的部分。


* Online/Offline Algorithms
  * 解释在线算法和离线算法的区别。
* Introduction
  * 主要概述Point Location的背景，关联在线算法部分，提出在线算法的要求，给出一个宏观纵览。
* Slab Method
  * SlabMethod即通过先将图按顶点划分为多个竖条Slab后，再在每个Slab中按照从高到低的顺序来划分。进而使得每一个点坐标都可以通过位置来判断所属区块，进而判断位置。其预处理可以达到$O(nlogn)$时间，但复杂度有$\Theta(n^2)$
* Persistence
  * 本章主要介绍Ephemeral Structure和Persistent Structure之间的区别和用途。细分介绍Partial Persistent Structure和Fully Persistent Structure。
* Path Copying
  * 基于上面介绍的Persistence思路。在扫描线构造的时候不再是每个Slab生成树，而是引用老的一部分树结构。注意这里是平衡二叉树，每次都会插入一个节点，对插入操作的修改部分进行Copy，其余进行引用就可以了。
* Node Copying
  * 本章则是为了追求空间上达到$O(n)$复杂度而进一步优化数据结构，其演算更为复杂不想知道可以跳过。该结构是在Path Copying上进一步细化只Copy旋转改变的节点以达到复制的节点更少。这样的结构需要用到红黑树。同时会使查找时间变成$O(log^2n)$
* Limited Node Copying
  * 在Node Copying的基础上，为了重新降下来时间查找复杂度而而限制每个复制节点的大小。为此要类似B树一样向上分裂各个节点。
* Kirkpatrick Structure
  * 本章主要介绍Kirkpatrick结构以及该结构上的点定位操作。该几何结构，能做到跟Persistent Structure一样的存储结构和效率。该方法需要先预处理Subdivision成一个三角刨分结构。最后通过在细节三角刨分上面删除点来构建一个层级数据结构。该结构可以使得算法的时间复杂度在$O(logn)$而空间复杂度在$O(n)$量级。只是时间复杂度前面有一个巨大的常数。
* Trapezoidal Map
  * 本章主要介绍梯形图算法，这个算法是一个随机算法。本章先介绍了相关基础，给出了一个例子和对应的Search Structure来说明其运作的方式。
* Constructin Trapezoidal Map
  * 本章主要介绍构如何造梯形图的Search Structure。其方法是一种随机构造算法(RIC)。从空图开始，随机选择一条边加入到当前梯形图来处理生成Search Structure。
* Performance Of Trapezoidal Map
  * 本章主要分析梯形图的效率。在Trapezoidal Map算法中只有一个地方随机化，即线段的插入顺序。而在每一步骤中主要有两步时间消耗，生成梯形和点定位。统计求取期望即是，而分析过程中大量使用的主要是基于梯形四边形的后向分析技术。

***