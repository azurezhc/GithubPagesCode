# 04Voronoi图(Voronoi Diagram)

本章主题介绍平面如何划分。通过对平面划分成距离点最近的区域，与Voronoi图相关联。Voronoi图是一个经典问题，同时介绍了计算几何中的一个经典数据结构DCEL。

* Introduction
  * 介绍Voronoi图的来源，应用场景。有一篇很不错的背景介绍文章。
* Terminologies
  * 介绍Voronoi图相关概念术语。
* Properties
  * 介绍Voronoi的特性。主要是等距性和非空性。
* Complexity
  * 简单介绍Voronoi的存储复杂性。
* Representation
  * 介绍对Voronoi的存储，表示。主要方式为主区域刨分(Subdivision)，同时也适用于其他一些表示。同时为了快速的查找，引入了DCEL。
* DCEL
  * 介绍了DECL数据结构来存储平面图结构。
* Hardness
  * 规约技术界定了Voronoi图的复杂度，使用的是排序方式来规约操作。
* Sorted Sets
  * 关注在某些情况下Voronoi图的求解问题是否会更容易。例如在某个方向排好顺序，类似凸包的Graham Scan方式，是否可以有效降低复杂度。
* $VD_{sorted}$
  * $VD_{sorted}$即排序的Voronoi图复杂度。在这里引入了$\epsilon{}-Closeness$问题并将其归约到$VD_{sorted}$来说明排序对于降低Voronoi图的复杂度并没有帮助。值得一说的是，即便知道Voronoi图的问题也不能帮助排序，看似两个问题结构毫无关联。
* Naive Construction
  * 简单说明一下最朴素的构造方式。
* Incremental Construction
  * 增量式构造。即每次增加一个点的方式来构造Voronoi图
* Divide-And-Conquer
  * 基于分而治之的思路，将平面划分，分成多个区域然后合并起来操作。
* Plane-Sweep
  * 基于扫描线的方式来生成Voronoi图结构。基本想法是，根据已经扫描过的点来确定一些潜在的生成Voronoi点的事件位置。高层想法是基于抛物线结构。


# Voronoi图介绍

Voronoi图第一次由G. F. Voronoi(1868 - 1908)第一次正式的提出并且界定，于是后来这种图结构，一般都称之为Voronoi图。直观来看Voronoi图由一系列点和边构成，这些边会把点隔开，各自围成一个区域，在该区域内的点距离该点的距离是最近的，如下图：

<center><img src="../04.assets/p1.png"></center>

* 这些中心点，我们称之为Voronoi Site，简称Site。
* 这些区域，我们称之为Voronoi Cell，简成为Cell。从几何上来看，该Site之所以拥有这个Cell，是因为这个Cell中的点距离这个Site是最近的。

用数学的方式定义来说如下：

Voronoi图由一些d维空间中点$S=\Set{p_1,\cdots,p_n}$构成，每个点$p_i$称之为Site。对于每一个Site来说，存在一个区域Cell，该Cell包围目标$p_i$，该区域可表示为$Cell(p_i)=\set{q\in{}\mathbb{R}^n|d(q,p_i)<d(q,p_j),\forall{}j\neq{}i}$。

根据这些定义我们可以得到一些特性：

> 每个Cell都是凸的。

因为对于每个Cell可以通过$p_i$跟其余$n-1$个点求所在半平面的交来来确定，因为半平面可以认为是一个凸多边形。而凸多边形在交运算下保持，所以Cell也是凸的。

{{< admonition info "思考问题">}} 

* Voronoi图会包含线段，射线，以及直线

只当所有点都在一条线上的时候会出现直线。因为存在直线，那么所有点间平分线都必须平行。有一个相交则都有交点。所以所有Site都在一跳直线上。

* $n$个点的Voronoi图最多会包含多少条线
  
根据无敌的平面图欧拉公式$V-E+R=2$，这里$R$即面数是所有Site个数。$E$为边数，而$V$为边交点个数。所以可以得到$E-V=n-2$。

{{< /admonition >}}


# DCEL结构


# Voronoi规约

# Voronoi图构造