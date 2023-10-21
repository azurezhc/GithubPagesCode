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

相对应的，对于使用了UnityEditor空间的脚本我们都需要放置在Editor文件夹下，不然会编译不通过。而UnityEditor空间内的函数则是我们扩展编辑器的主要接口。

# 常用属性结构

Unity提供一套原生的属性(Attribute，也称特性)结构。可以标记一些属性来方便修改对应的Inspector显示。

```csharp
[RequireComponent(typeof(Transform))]
//RequireComponent 添加该组件时，对应GameObject上要有对应类型组件
[AddComponentMenu("Game/EditorAttributeTest")]
//在AddComponent 指定该组件的显示方式，设置为""可以隐藏该项
public class BaseEditorAttributeTest : MonoBehaviour
{
    [Header("Header Info")]
    //HeaderAttribute可以添加一个文字抬头说明
    [Range(0, 100)]
    //RangeAttribute可以使对应显示变成一个滑动条，限定范围
    public int int_num;
    [Multiline(4)]
    //MultilineAttribute可以使文本编辑窗口显示多行
    public string short_description;
    [TextArea(4, 6)]
    //TextAreaAttribute可以显示一个文本编辑器区域
    public string long_description;
    [Tooltip("Show Tool Tip Contents")]
    //TooltipAttribute可以给概述添加一个提示文本
    public bool show_tool_tip;

    [ContextMenu("RandomValue")]
    //ContextMenuAttribute使得冒号菜单中添加该名称菜单项，点击后调用该方法
    public void RandomValue()
    {
        int_num = Random.Range(0, 10);
    }
}
```

最终显示出来的效果如下：

<center><img src="../01.assets/p2.png"></center>

可以看到这些属性只能略微改变原有的显示样式。还达不到扩展Editor的效果。

# OdinInspector

这里就要隆重介绍OdinInspector。其是一个第三方插件。主要提供了大量属性(Attribute)。通过这些属性可以直接标注目标属性，然后在Inspector上绘制出想要的结构，有了这个工具基本上可以定制出大量自己想要的显示效果。

<center><img src="../01.assets/p3.png"></center>

但是跟前面所述一样，对于结构属性之间的关联，其仍然是由使用人员来定义的。OdinInspector只是提供了一系列通用方便的工具结构。

# 事件通知接口

除了基础的属性(Attribute)之外。Unity实际上还约定了几个专门的函数，这些函数在Unity约定的情况下会被调用，通过这些接口，就可以对这些情况进行自定义事件处理。

常用的有：

```csharp
// 当通过Inspector修改属性的时候被调用。
public void OnValidate()
{

}
//绘制该物体的Gizmos，即一个编辑器中用来表示的对象 编辑器每次重回时都会调用该接口
public void OnDrawGizmos()
{
    Gizmos.DrawWireSphere(transform.position, 5);
}
//当该物体被选中的时候，绘制改物体的Gizmos
public void OnDrawGizmosSelected()
{
    Gizmos.DrawSphere(transform.position, 2);
}
```

通过OnValidate我们可以对Inpsector的输入输出都进行一个宏观的控制。而Gizmos相关接口，可以在SceneView中给出一个可视化标识。