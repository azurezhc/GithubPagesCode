---
title: "IMGUI扩展Inspector基础"
date: 2023-10-21
draft: false
---


# IMGUI扩展Inspector基础

前面了解了一些简单的UnityEditor扩展结构。但是这些都很定制化。我的最终目标是可以根据想要的数据编辑结构，提供一个舒适的管线。这里就记录我了解到的，如果扩展Inspector的基础结构。

Unity经历过长时间的发展，到目前位置已经有了三套UI系统。

* IMGUI，最早的UI系统，后来被逐渐替换成了UGUI。但是在编辑器侧依然维护者IMGUI的框架结构。
* UGUI，后来重构的新GUI框架。现在主要是在游戏运行时提供UI框架结构服务。
* UIToolkit，因为前面UGUI与大众的UI编辑器不一样，借鉴通用UI编辑器而制作的以

现在普遍来说游戏运行时都是以UGUI为主。而编辑器侧都是以IMGUI方式开发。但是后面可以看到IMGUI的构造方式不够只管。而且都是

这里主要记录IMGUI扩展Editor的方式，以及接口函数。记录以供入门理解扩展编辑器方式。

# Inspector扩展

如前面所述，在Unity我们写一个类继承MonoBehaviour或者ScriptableObject时候会，Inspector上会显示出相关的一些编辑UI。此即Unity Editor提供的编辑窗口。

现在我们要扩展对某个类的Inspector窗口。我们要以某种方式跟这个类关联。而Unity则提供了一个简单的方式来关联要扩展Inspector的类。

* 写一个继承Editor的类，此及用来提供编辑窗口相关功能的类。
* 用CustomEditor属性(Attribute)来关联目标类。

具体代码如下：

```csharp
// 要扩展Inspector显示的目标类
public class MonoAvatar : MonoBehaviour
{
    public int hp;
    public float speed;
    public string avatar_name;
}

//描述Inspector中UI相关结构细节的类
[CustomEditor(typeof(MonoAvatar))]
public class MonoAvatarEditor : Editor
{
    private void OnEnable()
    {
        //当关联的Inspector打开时调用
    }

    private void OnDisable()
    {
        //当关联的Inspector关闭时会先调用OnDisable然后调OnDestroy
    }

    private void OnDestroy()
    {
        //当关联的Inspector关闭时会调用OnDestroy
    }

    public override void OnInspectorGUI()
    {
        //IMGUI框架中绘制InspectorGUI的接口
        //会按照Inspector的绘制帧率来调用该接口
    }
}
```

其中OnInspectorGUI接口则是我们用来绘制Inspector窗口的主要战场。如果空置此函数，你会发现Inspector上不再显示原来相关的可编辑接口。这是因为默认的属性编辑Field是由Editor基类里面来提供的。如果想要保持原来的调用base.OnInspectorGUI即可。

现在我们要对Inspector界面上做一些新的绘制。这里用到的类即：

* EditorGUILayout : 提供了Editor下已经布局好的一些成品组件。
* GUILayout：GUI下已经布局好的一些成品组件。与EditorGUILayout的区别在于GUILayout也包含了运行时的UI结构。

通过这些以及足以绘制出足够的编辑器结构。

## 基础绘制

这里先示例，扩展一个Button，该Button可以使得编辑的对象，可以按照x,y,z填的数值，在编辑器中移动对应距离。代码如下：

```csharp
public override void OnInspectorGUI()
{
    base.OnInspectorGUI();
    // EditorGUI显示一个帮助提示框
    EditorGUILayout.HelpBox("这都是Editor内的编辑属性", MessageType.Info);
    // EditorGUI用来生成属性编辑框函数 这里即生成3个Int类型的编辑框，并且跟x,y,z三个属性值关联，其编辑获取值为右侧参数，返回值为输出赋值
    x = EditorGUILayout.IntField("x", x);
    y = EditorGUILayout.IntField("y", y);
    z = EditorGUILayout.IntField("z", z);
    //添加一个Button，当Buttong点击的时候触发回调函数，返回true进而触发点击逻辑。
    if (GUILayout.Button("StartMove"))
    {
        // 每个Editor都有一个target对象，绑定目前正在编辑的类型的对象。这里即场景中GameObject上的MonoAvatar类型。
        var avatar = (MonoAvatar)target;
        avatar.transform.position += new Vector3(x, y, z);
    }
}
```
最终显示效果如下：


<center><img src="../02.assets/p1.png"></center>

而EditorLayout中还有更多一系列接口函数，可以设置更多的空间类型。这些可以参考前面相关文档，研究并绘制出想要的组件结构。

对于Layout提供的接口中，大部分最后还是提供一个类型GUILayoutOption可变长参数列表。通过这些GUILaytoutOption对象则可以相应的调整显示的效果。

例如对于IntField来说有：

```csharp
public static int IntField(string label, int value, params GUILayoutOption[] options)
{
    return IntField(label, value, EditorStyles.numberField, options);
}
```
最后的GUILayoutOption则可以通过诸如GUILayout.Height(40)等参数来调节。

## 布局函数

现在我们考虑在Inspector进行布局的简单控制。这里就可以通过IMGUI的布局函数来实现。我们用Button来做一个示例：

```csharp
public override void OnInspectorGUI()
{
    base.OnInspectorGUI();
    EditorGUILayout.HelpBox("这都是Editor内的编辑属性", MessageType.Info);
    vec3 = EditorGUILayout.Vector3IntField("Vector3Field", vec3);

    //构造一个水平布局作用域，在域内的对象会被是为要水平布局的对象。
    using (new EditorGUILayout.HorizontalScope())
    {
        GUILayout.Button("LayoutField Left");
        GUILayout.Button("LayoutField Middle");
        GUILayout.Button("LayoutField Right");
    }
    //以前的代码中也提供了如下的作用域函数对
    //EditorGUILayout.BeginHorizontal
    //EditorGUILayout.EndHorizontal

    if (GUILayout.Button("StartMove"))
    {
        var avatar = (MonoAvatar)target;
        avatar.transform.position += new Vector3(x, y, z);
    }
}


```

最终效果如下：

<center><img src="../02.assets/p2.png"></center>


## 自动布局与位置计算

这里你会发现，前面并没有并没有直接用布局函数修改IntField来实现图中类似于Vector3的效果。这是因为其实对于Layout中接口来说，其都是带有自动布局效果的。如果直接使用HorizontalScope会发现其自动布局效果并不如意，如下。

<center><img src="../02.assets/p3.png"></center>

可以发现这是因为这个IntField的Label是根据所在区域的宽度算出的一个固定值。这导致整个Field长度远远长于了Inspector的宽度。同时的是，不论对布局参数如何修改，都无法修改这一部分。其布局修改针对的主要是后面填写区域部分。

这时候我们非要去制作这样一个显示，可想而知，就要自己去操作布局结构了。而这可以通过Layout对应的两个布局计算类来实现，即：

* EditorGUI : 编辑器下GUI元素的绘制接口。
* GUI : GUI元素的绘制接口。

但是在IMGUI中直接根据布局函数来绘制UI元素非常麻烦，而且自己计算GUI位置本质就是把布局功能完全接管到自己手里，这样可能导致原来自动布局的各种问题。

以下是一个自己计算Rect来绘制field的示例：

```csharp
public override void OnInspectorGUI()
{
    base.OnInspectorGUI();
    EditorGUILayout.HelpBox("这都是Editor内的编辑属性", MessageType.Info);
    vec3 = EditorGUILayout.Vector3IntField("Vector3Field", vec3);
    //获取当前已绘制好的所有属性占据的
    var now_rect = GUILayoutUtility.GetLastRect();
    //用Space空出要绘制的布局用空间 实际使用GUILayoutUtility的GetRect来获取布局用空间。
    var item_width = now_rect.width / 6;
    EditorGUILayout.Space(20);

    //根据已经占用的Rect参数来平均布局控件位置
    var start_x = now_rect.x;
    EditorGUI.LabelField(new Rect(now_rect.x, now_rect.yMax, item_width, 20), "x");
    x = EditorGUI.IntField(new Rect(start_x += item_width, now_rect.yMax, item_width, 20), x);
    EditorGUI.LabelField(new Rect(start_x += item_width, now_rect.yMax, item_width, 20), "y");
    y = EditorGUI.IntField(new Rect(start_x += item_width, now_rect.yMax, item_width, 20), y);
    EditorGUI.LabelField(new Rect(start_x += item_width, now_rect.yMax, item_width, 20), "y");
    z = EditorGUI.IntField(new Rect(start_x += item_width, now_rect.yMax, item_width, 20), z);
}
```

最终效果如下：
<center><img src="../02.assets/p4.png"></center>


# PropertyDrawer

通过上面的方法已经可以对目标类型进行Inspector扩展绘制了。但是这个粒度可能仍然不够使用，例如如下一些情况：

* 例如上面的MonoAvatar作为成员变量的时候，会变成一个ObjectField而不是展开其扩展的Inspector面板。
* 对于一些基础类型，我们想定制一些自己的Inspector展示方式。

虽然原有的结构也可以进行一定程度的功能复用。例如我们将一些绘制步骤封装成一个静态函数，复用函数即可复用绘制功能。但是其针对已究

好在Unity还提供了一种基于属性(Attribue)的绘制方式。通过继承PropertyDrawer并标记目标属性，我们可以对被属性修饰的字段进行定制绘制。

这里仍以上面的MonoAvatar示例，新增一个Vector3变量。修饰该变量，使得Inspector中多出一个InfoBox和一个Label表示该向量的距离。


```csharp
// 标记绘制属性 需要继承自PropertyAttribute
public class AvatarAttribute : PropertyAttribute
{
}

//通过CustomPropertyDrawer跟目标属性关联
[CustomPropertyDrawer(typeof(AvatarAttribute))]
public class AvatarPropertyAttributeDrawer : PropertyDrawer
{
    // 重载获取属性的绘制高度接口 基于足够的空间来绘制
    public override float GetPropertyHeight(SerializedProperty property, GUIContent label)
    {
        var property_height = EditorGUI.GetPropertyHeight(property);

        return property_height * 2 + 40;
    }

    //绘制属性接口 传入的Rect即整个属性所占用的绘制空间。property则是被标记的属性的抽象封装。
    public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
    {
        var start_y = position.y;
        var help_box_rect = new Rect(position.x, start_y, position.width, 40);
        EditorGUI.HelpBox(help_box_rect, "这是用Property绘制出来的对话框", MessageType.Info);
        //直接用Vector3IntField将原来的字段绘制出来
        var height = EditorGUI.GetPropertyHeight(property);
        var property_rect = new Rect(position.x, start_y += 40, position.width, height);
        var target_vector3 = property.vector3IntValue;
        property.vector3IntValue = EditorGUI.Vector3IntField(property_rect, "Vector3", target_vector3);
        //绘制一个LabelField 显示出向量的距离值
        var laebl_rect = new Rect(position.x, start_y + height, position.width, height);
        EditorGUI.LabelField(laebl_rect, new GUIContent(string.Format("{0:N2}", target_vector3.magnitude)));
    }
}

```

最终效果如下：
<center><img src="../02.assets/p5.png"></center>

需要注意的是，PropertyAttribute只能标记字段类型，所以只能拿到可序列化字段相关的数据，以及相关类型的反射数据。并不能拿到相关对象。所以其虽然可以添加Button这样的GUI但是其功能受限的。

另一方面是对于像是Button这样的功能结构，一般带有操作对象语义，实际上则可以通过Editor来实现，具体来说是走OnInspectorGUI来绘制。例如如下方式：

* 定义一个继承自MonoBehaviour或者ScriptableObject的类。
* 定义这个类对应的Drawer类型。通过CustomEditor关联起来。
* 在OnInspectorGUI中对target对象进行反射遍历，取出对应的属性。

\
对于OdinInspector来说，实际上大部分都是通过Editor方式来进行绘制的。例如Button这个属性。因为PropertyAttribute只能标记字段。但是Button一般标记一个方法，快捷的让方法可以显示出一个Button来调用。所以只能自己实现ButtonAttribute，在OnInspector中进行反射遍历，筛选绘制来实现。正是通过这样的方式，Odin实现了大量的属性，可以方便的通过属性(Attribute)方式快速定制整个Editor界面。

# Window扩展

除了对Inspector进行扩展。我们有些时候还需要一些编辑管线窗口。例如提供一个窗口来方便的编辑道具功能等等。这个时候就需要定制化的一个窗口来。

这里示例创建一个窗口筛选场景中所有带有MonoAvatar的Gameobject并且显示出来，当点击时可以快速定位场景。

Unity创建一个Window非常简单。可以通过如下方式即可：

```csharp
//继承自EditorWindow即可
public class MonoAvatarEditorWindow : EditorWindow
{
    //添加一个菜单项 创建该Window
    [MenuItem("Tools/AvatarEditorWindow")]
    private static void ShowWindow()
    {
        var window = GetWindow<MonoAvatarEditorWindow>();
        window.titleContent = new GUIContent("AvatarEditoWindow");
        window.Show();
    }

    //跟Inspector一样的一组生命周期接口
    public void OnEnable()
    {
    }

    public void OnDisable()
    {
    }

    public void OnDestroy()
    {
    }

    //约定的一个绘制接口，这个不是继承而来，而是由外部系统
    private void OnGUI()
    {
    }
}
```

可以发现对于EditorWindow来说直接使用OnGUI接口，并没有传入任何参数。此时整个窗口的绘制要素都存放在EditorWindow的字段之中。例如position字段为一个Rect类型，表示了此时整个EditorWindow窗口的大小。

下面筛选场景物体，把MonoAvatar的物体筛选出来。并且显示：

```csharp

public float button_width = 100;
public float button_height = 100;
public Vector2 scrollview_pos;
public int select_index = -1;

//找到所有对象 然后声明一个ScrollView区域并使用一个SelectionGrid来显示整个内容。
var objects = Object.FindObjectsOfType<MonoAvatar>();
var row_capacity = Mathf.FloorToInt(position.width / button_width);
using (new GUILayout.ScrollViewScope(scrollview_pos))
{
    select_index = GUILayout.SelectionGrid(select_index, GetObjectContents(objects), row_capacity, GetGUIStyle());
    if (select_index != -1)
    {
        //用selection标记当前激活的对象
        Selection.activeObject = objects[select_index];
    }
}

// 根据传入的Mono脚本生成对应的GUIContent列表返回，以供SelectionGrid显示。
public GUIContent[] GetObjectContents(MonoAvatar[] mono_avatars)
{
    var guicontents = new GUIContent[mono_avatars.Length];
    for (int i = 0; i < mono_avatars.Length; i++)
    {
        var guicontent = new GUIContent();
        guicontents[i] = guicontent;
        guicontent.text = mono_avatars[i].name;
        guicontent.image = AssetPreview.GetAssetPreview(mono_avatars[i].gameObject);
    }
    return guicontents;
}

//获取一个GUIStyle定制以下显示格式
public GUIStyle GetGUIStyle()
{
    var style = new GUIStyle(GUI.skin.button);
    style.alignment = TextAnchor.LowerCenter;
    style.imagePosition = ImagePosition.ImageAbove;
    style.normal.textColor = Color.white;
    style.fixedHeight = button_height;
    style.fixedWidth = button_width;
    return style;
}

```

最后呈现出如下效果：

<center><img src="../02.assets/p6.png"></center>

# 最后

这里只是如何扩展Unity Editor的基础介绍。但是很多结构实际上都是建立在基础结构之上一步步搭建起来的。