# 07几何范围查找(Geometric Range Search)

[计算几何-笔记目录](./计算几何-笔记大纲.md)

在第六章中主要讨论的是点定位问题，及给定平面的刨分和一个点，确定点所在位置。本章则相当于其反向问题版本，给定一个矩形，确定哪些点被包含在这个矩形当中。本章业主要以在线算法为主，即给定点是预处理好的，而输入查询则是随机不可预期的。

* Range Query
  * 介绍范围查询在线算法概念，并以一维范围查询来初探该类问题。在一维情况下很简单，但是不容易直接推广到二维情况下。
* BBST
  * 介绍后面要用到的一种特殊BBST，并对其进行分析。使用该BBST也可以快速定位一维范围查询，虽然该结构复杂但可以推广到二维。
* kd-tree
  * 介绍引入kd-Tree概念。主要讲解了kd-Tree的构造方式。
* kd-Tree: Algorithm
  * 介绍kd-Tree的查询计算方式，并举出例子来说明。
* kd-Tree: Performance
  * 对二维kd-Tree进行性能分析。主要为构造耗时，存储消耗，查询时间等分析。也说明kd-Tree可以推广到任意维度都可行。
* Range Tree: Structure
  * 介绍Range Tree，讲解其结构，说明RangeTree的由来和原因。
* Range Tree: Query
  * 介绍在Range Tree上来进行查询的算法过程。
* Range Tree: Performance
  * 本节主要对Range Tree进行性能分析。分析其存储，预处理以及查询效率。存储空间大小在$O(nlogn)$范围，预处理时间花费在$O(nlogn)$，而查询需要$O(r+log^2n)$的时间。
* Range Tree: Optimization
  * 本届主要对Range Tree进行优化。目标是为了使得2维查询变成$O(logn)$时间量级。思路是最后Y查询的时候，可以发现不同条带之间，上下两个横街轴是共同的。

***

