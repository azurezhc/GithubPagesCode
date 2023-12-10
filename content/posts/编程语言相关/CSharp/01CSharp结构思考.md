---
title: "C#结构思考"
date: 2023-12-10
draft: false
---


# Dispatch实现以及效率

Dispatch结构可以认为是设计模式的监听者模式结构。实际这里最主要的点便是映射结构，更确切的说，是将一个Key值跟一个函数调用（或者一个函数调用List）绑定在一起。通过这个Key值是可以调用目标注入的函数调用。这个结构在很多场合中非常适用，尤其是通过运行时某个字段的值来调用对应处理函数。这在C#中显然要通过Dictionary和delegate结构来实现。虽然delegate跟接口在功能类似化，但是delegate有个显著特性是，只关注函数签名，隐藏相关类型对象，而不是关注函数名称对象。如果用接口，则所有对象上都要实现该接口，这样才能绑定进来。这样在某些场合限制还是很多的。

我想到一共有三种方式来处理：

> * 方式1：直接使用原生的Action，每遇到一个新的事件类型添加一个对应变量参数的Action变量值字段。

即如下结构
```csharp
public class Dispatch
{
    public Action<int> action_event_1;
    // 当需要一个新的通知事件时 直接根据参数添加对应delegate即可
    public Action<int, string> action_event_2;
}
```

这样的好处是效率高，而且代码清晰，每遇到一个新的添加一个字段即可。在很多情况下需求都可以被该方式满足。在这里添加的每个Action的变量值字段就相当于脚本语言如Python语言中dict的键值。

而缺点就在于

* 并没有解决运行时根据某字段值分派问题。例如我传递过来的是一个基础类型，其中有个字段```dispatch_type```。根据该字段来选择合适的处理方法就需要大量```ifelse```来判断。因为不是一个动态容器结构，而是使用了类型的变量字段方式，所以一定要```ifelse```操作。而这个地方```ifelse```所作的工作就类似于python语言中，对dict进行查询键值的操作。非常多余且不利于扩展。
* 对于Action来说，C#并没有提供清空接口。也就是说当需要清空时，要针对每个事件自己去写清空操作。这又是一系列根据变量值字段的硬编码。

但是如果这个Dispatch是个持久化结构，即长时间驻留内存，而注入回调与移除回调的控制端是自我知晓的，即他有明确定义，什么时候应该注入回调，什么时候应该移除回调。那么这个结构也是合适的。

> * 方式2：使用delegate的基类System.Delegate来声明Dictionary中的泛型结构。

即如下结构

```csharp
public class Dispatch
{
    public Dictionary<int, System.Delegate> delegate_dict;

    public void Operation()
    {
        // 使用Action包装一下目标function 传入
        delegate_dict[1] = new Action<TargetParams>(TestTargetFunction);
        // 调用使用DynamicInvoke 传入目标参数
        delegate_dict[1].DynamicInvoke(new TargetParams())；
    }
}
```

> * 方式3：使用跟C#中event类似的结构。简单来说，就是共同基类，每个处理接口中，转换成对应应当处理的结构。

即使用如下结构

```csharp
public class Dispatch
{
    public Dictionary<int, Action<BaseDispatchEvent>> delegate_dict;

    public void Operation()
    {
        delegate_dict[1] = TestBaseFunction;
        delegate_dict[1](new BaseDispatchEvent())；
    }

    public void TestBaseFunction(BaseDispatchEvent base_event)
    {
        var child_event = base_event as IntDispatchEvent;
    }
}
```

其实可以看出来，使用System.Delegate可以方便注入各种函数，其函数包装签名在注入点而不是函数申明处，进而有一下方便之处：

* 注入的目标函数，其函数签名部分可以为任意类型。不需要额外添加一个数类型转换操作。
* 由于函数签名可以为任意类型。所以注入回调函数，不需要再额外声明一个子类的参数数据结构。

而使用基类方式，因为Action被申明写死，所以只能使用同一个参数，所以需要在内部进行转换。从功能上来讲，其都可以实现前面的主要要求，即：

* 根据一个运行时字段的值，来进行分配函数操作。

另一方面是可以感觉到对于System.Delegate的调用方式实际上时近似于反射的，对于```DynamicInvoke```接口，其为了可以接受任意长度任意类型参数所以其接受为一个object边长数组。所以其调用效率不会太高。



## 效率对比

下面是主要测试这三个方式的一个效率对比。根据前面所讲，我最关注的是，这几个方式当频繁调用时的时间损耗。如果损耗过大，那显然是不行的。另一方面是，有些实现结构，例如方式2和方式3其实现的功能结构是一致的,只是方便程度不太一样。

在我电脑上的一个简单效率对比：

运行次数：$10^6$
| 方式说明                   | 时间花费(ms) |
| -------------------------- | ------------ |
| 使用直接原生Action         | 6            |
| 声明基类Action然后强转类型 | 7            |
| 使用System.Delegate        | 2053         |

可见System.Delegate调用速率过慢，以至于有几百倍的效率差异。

补充方式1方式3对比
运行次数：$10^9$
| 方式说明                   | 时间花费(ms) |
| -------------------------- | ------------ |
| 使用直接原生Action         | 5688         |
| 声明基类Action然后强转类型 | 7142         |

额外的耗时部分实际上就来自于类型转换。

## 总结说明

可以看到不论什么方式最后都还是比原生Action调用慢。其中System.Delegate实在是慢的过头，以至于虽然提供了最方便的架构方式但是依然不能轻易采用。

而类型转换的方式损耗实际上还是在一个比较可控的范围，其中有很大一部分开销来自于类型转换，如果没有类型转换两者效率近乎相等。但是通常情况来说，我们可能不同接口中需要的数据结构往往是不同的，这就需要进一步的数据划分。我觉得这也是C#用这种方式来实现event这么一个关键字结构的原因。另一方面在这种结构里面，BaseDispatchEvent封装了所有事件数据结构拥有的结构，例如那个用来运行时判定分配的数据字段值。实际上可以认为其代表的就是运行时参数这么一个抽象。

实际上直接申明Action变量值字段的方式，结合其他一些数据结构，足以应付大部分情况。例如一般经常用在架构中的注册监听方式。对于每一个类型，实际上其关联的参数字段都是固定的，直接声明成固定类型即可。上述的结构，实际上只是因为架构中要在运行时，去处理一系列数据类型的处理。如果对于调用者，注册者来说，知道确切的语义环境，直接声明Action跟简单跟快捷。


# 实例类型判定

前面讲到这个结构需要一个运行时字段来判断处理方式。这类情况实际上经常发生在，一个功能结构，其输入为某个类型的子类，但是参数什么为父类的情况下。此时该功能的语义就是接受这一类对象或者数据结构，根据不同类型来进行处理操作。

这里考察的就是C#中，如果要方便定义一个子类某一个字段的值，使得其运行时对象可以方便获取字段值。我想到的大概也有三种方式：

> * 直接通过面向对象的概念，通过GetType来获取。
> * 通过虚函数结构，通过一个虚属性来方便定义。
> * 父类定义一个属性，子类构造是赋值，并且不可变。

我考虑的主要还是两个方面，1：使用便利程度，2：运行时效率。

* 通过虚属性结构来操作：

```csharp
public enum EventTypeField
{
    BASE_TYPE,
    INT_TYPE,
}

public class TestBaseType
{
    public virtual EventTypeField type_property => EventTypeField.BASE_TYPE;
}

public class TestIntChildType : TestBaseType
{
    public override EventTypeField type_property => EventTypeField.INT_TYPE;
}
```

声明枚举类型来做为分发字段值。通过一个虚属性来定义获取变量的属性字段，对于任何子类型实例，获取该字段，即可获得我们想绑定在这个类型上的类型标记值。进而进行分派。这里实际上是通过，虚函数结构来走。即申明一个虚函数```type_property```，然后通过属性的快捷方式，定义这个函数的返回值，来将这个运行时变量与类型部分绑定在一起。

* 通过父类公用变量字段来操作：

```csharp
public enum EventTypeField
{
    BASE_TYPE,
    INT_TYPE,
}

public class TestBaseType
{
    public readonly EventTypeField type_field;
    public TestBaseType(EventTypeField target_field)
    {
        type_field = target_field;
    }
}

public class TestIntChildType : TestBaseType
{
    public TestIntChildType() : base(EventTypeField.INT_TYPE)
    {
    }
}
```

即申明一个变量字段在父类中，这样子类都会拥有该字段。同时该字段就相当于这一系列类共有的封装结构，即都有一个变量字段，这个变量字段可以来分派这些数据结构。因为是个变量字段，所以只能通过实例构造来赋值该字段。相应的，对比前面一种方式，相关结构时绑定在类上。这里实际上是每个实例中都有这么一个字段，这个字段值都相同来操作的。

这个方式最大的问题在，会忘记去调用基类的构造操作而导致```type_field```值不对。代码书写上有所不便。

实际上还有一个中间结构，即定义一个抽象函数，在基类构造时固定调用该函数来完成共有数据部分初始化。不过本质还是一样的。没必要去绕这么一下。

另外在单字段判断的情况下这三种方式一致。但是如果父类不是定义一个类型字段，提供一个共有数据结构基础，我们通过这个共有的数据结构来进行判断操作。那么还是需要后两种方式。

## 效率对比

运行次数：$10^9$
| 方式说明       | 时间花费(ms) |
| -------------- | ------------ |
| GetType()方式  | 2631         |
| 虚属性方式     | 4979         |
| 变量值字段方式 | 2615         |

## 总结说明

可以发现虚属性申明方式意外的要耗一些。实际上因为虚属性要过虚表还要调用函数，自然会比变量值字段要多耗时一些。而获取类型跟变量值则相差无几。也就是说实际上对于面向对象来说，声明好结构，使用Type来判断即可。


# Action结构

根据CLR可以知道C#委托(delegate)结构底层实际上是一个数组结构。当删除一个委托实例时，会把之后的委托实例全部前移。所以可想而知在频繁增删的时候其效率是不高的。

另一方面是委托没有提供简单的清空接口。要清空一个委托需要使用如下方式来进行操作。

```csharp

public Action target_delegate;

public void ClearDelegate()
{
    //直接赋值为null来操作 通常操作 这代表一个空的invocationlist
    target_delegate = null;

    //获取列表然后清空
    System.Delegate[] dels = target_delegate.GetInvocationList();
    foreach (var inner_del in dels)
    {
        delegate_normal -= inner_del as Action;
    }
}
```

所以这里主要思考这个结构如何优化使用。

> * 使用LinkedList链表结构。每个节点就一个Action。遍历与增删都依据链表结构运行。
> * 使用略加修改的数组。每个位置一个Action。

主要考量的是，1：使用便利性。2：遍历效率。3：增删效率。

* 使用LinkedList结构如下：

```csharp
public class LinkedListAction
{
    // 直接使用C# 的LinkedList结构 其内部实现就是一个链表结构
    public LinkedList<Action> actions;

    public LinkedListAction()
    {
        actions = new LinkedList<Action>();
    }
    // 操作结构直接使用LinedList即可
    public void AddAction(Action new_action)
    {
        actions.AddLast(new_action);
    }

    public void RemoveAction(Action new_action)
    {
        actions.Remove(new_action);
    }

    public void ClearAction()
    {
        actions.Clear();
    }

    public void Call()
    {
        foreach (Action action in actions)
        {
            action();
        }
    }
}
```


* 略加修改的数组如下，其底层跟Action类似。不同的是，Action底层每次增删都会有个列表迁移。而这里的ArrayAction查找到后直接设置为null来进行快速操作。所以其数组会存在空洞，同时存在数组扩容问题。但这些都是比较好解决的问题。

```csharp
public class ArrayAction
{
    // 数组来存放整个列表 queue则来放置空缺位置 使用list stack也可以
    public Action[] actions;
    public int min_index;
    public Queue<int> queue;


    public ArrayAction()
    {
        actions = new Action[50];
        queue = new Queue<int>();
        min_index = 0;
    }
    // 操作则是，添加后移，移除直接设置为空 所以遍历的时候存在空节点
    public void AddAction(Action new_action)
    {
        if (queue.Count != 0)
        {
            var empty_index = queue.Dequeue();
            actions[empty_index] = new_action;
            return;
        }
        actions[min_index] = new_action;
        min_index++;
    }

    public void RemoveAction(Action new_action)
    {
        for (int i = 0; i < actions.Length; i++)
        {
            if (actions[i] == new_action)
            {
                actions[i] = null;
                queue.Enqueue(i);
                return;
            }
        }
    }

    public void ClearAction()
    {
        for (int i = 0; i < min_index; i++)
        {
            actions[i] = null;
        }
        queue.Clear();
        min_index = 0;
    }

    public void Call()
    {
        for (int i = 0; i < min_index; i++)
        {
            if (actions[i] != null)
            {
                actions[i]();
            }
        }
    }
}
```
## 效率对比


测试使用50个匿名生成的Action。注入列表中来进行测试。

* 遍历效率

运行次数：$10^7$
| 方式说明       | 时间花费(ms) |
| -------------- | ------------ |
| 原始Action     | 2820         |
| LinkedList实现 | 25050        |
| Array实现      | 3750         |

* 随机增删

这里的随机增删采用随机对称增删，即删除一个再添加回去，这样测试比较好些。

运行次数：$10^7$
| 方式说明       | 时间花费(ms) |
| -------------- | ------------ |
| 原始Action     | 22084        |
| LinkedList实现 | 5261         |
| Array实现      | 2707         |

可以看到LinkedList为了提高增删实际上对于遍历的损耗是比较大的。我觉得这一部分应该来自于底层实现是链表，内存离散寻址。相对应的，对于原始Action的实现来说，其随机增删，每次都会移动整个底层列表，所以其增删效率就低很多了。相对应的可以发现Array的实现在遍历时效率相差不大，而增删时则是最优的。

* 空洞遍历

这里空洞遍历即基于Array实现，因为其可以随机增删所以其数组会存在空洞，所以测试随机移除一半以后的遍历效率。

运行次数：$10^7$
| 方式说明       | 时间花费(ms) |
| -------------- | ------------ |
| 原始Action     | 1293         |
| LinkedList实现 | 11136        |
| Array实现      | 2642         |


* 注入函数个数较少时，随机增删

这里考虑少量函数注入使用情况，看看效率。

运行次数：$10^7$
| 方式说明       | 时间花费(ms) |
| -------------- | ------------ |
| 原始Action     | 15536        |
| LinkedList实现 | 5225         |
| Array实现      | 2607         |

## 总结说明

可以看到Array的实现非常高效。实际上这是因为CLR对于Action底层的实现，确实是不够高效的方式，可以看到，即便对于注册监听的函数个数很小的时候，对于原生Action随机增删来说依然有较大消耗。
所以这里可以用自己的结构替代。实际上Array实现的方式就来自于动态数组实现。可以看到即便存在一定数量的空洞，Array的遍历效率依然不会太差。另一方面是，如果对于成对出现的增删操作，可以想到，对于Array来说，其空洞数量并不是特别多。其遍历效率就是整个数组的遍历效率。绝大部分情况是很好的。

而对于这方面的优化结构，还可以进一步迭代优化。