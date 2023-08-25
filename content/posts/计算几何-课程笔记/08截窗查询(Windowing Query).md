# 08截窗查询(Windowing Query)


在第七章中讨论的Range Query是给定一个矩形，查询有多少落在矩形中的点。而在本章，则相当于其一个扩展。对于点来说相当于对0维物体的查询，这里也可以对更高维度物体进行查询。例如对于1维来说，相当于给定一个矩形，查询与矩形相交的线段。

* Orthogonal Windowing Query
  * 主要介绍正交截窗查询(Orthogonal Windowing Query)的定义和分类。
* Stabbing Query
  * 主要介绍Stabbing Query。针对上述给出的Type B类型转化为1维查询问题。而该1维查询就相当于给定一个值，Stabbing出所有相交线段。
* Interval Tree: Construction
  * 本节主要介绍Interval Tree结构。介绍其构成方式，内部构成结构。最后给出一个简单的复杂度。
* Interval Tree: Query
  * 本节主要介绍如何在Interval Tree上左Stabbing Query。在该算法上给出查询的时间复杂度。
* Stabbing With A Segment
  * 介绍完1维直线的Stabbing Query之后，还需要回到2维的问题上。在2维中，这里实际是一个线段去做Stabbing Query。这里的主要改变就是修改Interval Tree中的两边List改为Range Tree。最后给出一个Windowing Query的算法，并分析出其算法性能。
* Grounded Range Query
  * 本节主要目标为了优化上面算法中的空间复杂度度。因为使用了Range Tree使得算法空间复杂度为$O(n)$，而思路想法在于Windowing Query中的Range Query实际上是一个无界的边界，所以构成了一个特殊的Range Query，即Grounded Range Query。
* 1D-GRQ Using Heap
  * 本节介绍在1维中使用最小堆(Minimum Heap)来实现上面的GRQ算法。这里用堆的一个重要原因是因为其可以拓展到2维情况下。
* Priority Search Tree
  * 主要介绍优先搜索树(Priority Search Tree)，PST=Heap+BBST。
* 2D-GRQ Using PST
  * 主要介绍基于PST怎么来做上面的2维Windowing Query。讲述了算法伪代码，举出了求解的例子，还分析了查询时间。注意到这个查询树的时间任然是O(r+logn)但是空间复杂依然变为O(n)
* Segment Tree
  * 本节主要目标其实是解决通用的Windowing Query。在通用的情况下线条并不再是正交的，于是对于上面Type B的那些线段，前述方法将失效。而解决方法就是使用Segment tree。
* Vertical Segment Stabbing Query