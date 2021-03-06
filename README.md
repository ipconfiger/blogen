blogen
======

A local static blog site generator and previewer,that help you deploy blog on github pages

Can you read chinese？yes i cam

__注意：刚更新了一个版本到pypi，因为生成的markdown文件目录名的问题导致了push到库后build启动了jekyll编译失败导致无法build发布，所以修改了目录名，请已经按装了的童鞋尽快更新到最新版本0.0.0.3 pre__

项目的由来
-------
为了弄公司的开发博客，很装13的选了github来host。为了SEO的缘故，以前那个 [jsloger](https://github.com/ipconfiger/jsloger) 就不怎么适合了。本着DRY的原则去考察了一下Jekyll，但是估计和ruby8字不和，搜索一下在github搭建blog大堆人都推荐这货，难道那家用着都这么欢乐么？事实是这货得自己创建一堆文件夹，自己创建一堆模板。文档里提到的Rake啥的，根本跑着不欢乐，down源码一看写那么多，就生成个静态文件的blog至于么？所以评估了一下，如果折腾Jekyll估计花两天，这两天折腾出来能弄的东西估计我花一天时间就用Python写好了。于是我就用Python写了目前这货。Jekyll能见的80%的功能应该都有，而且安装简单使用简便。如果对ruby没有强烈的爱就试试本货吧。欢迎Pythoner一起来完善。

本货其实不怎么需要文档
--------
本货只关注发布博客的内容和内容的格式化。格式化的方式交给了markdown和jinja2的模板。然后提供了几个命令用于串联相关的操作而不用自己去完成，所以使用步骤异常的简单。

使用的步骤：

###1 安装 
    $sudo pip install blogen 
###2 创建站点
建个目录，进入后执行一条命令即可
    
    $mkdir myblog
    $cd myblog
    $blogen --init 站点名称
这个命令会创建配置文件config.yaml和一大堆目录

* _data是存放blog的markdown文件的地方
* html是生成的html文件存放的地方
* templates是模板文件。这里只是生成了一个最简单的，模板可以完全根据自己的需要来改
* static是存放站点的CSS，JS和图片文件的地方

__注意：templates目录下会默认生成 index.html 和 post.html，这两个文件一个是首页模板和内容页模板，可以自由修改，保持名字不变即可__

###3 发布第一篇blog
发布blog只需要一条命令即可

    $blogen --post "hello world"
    
这条指令会在posts目录创建一个.md的markdown文件。注意，本货只支持markdown，因为其他太多的格式我不会，欢迎有需要的同学帮我添加其他格式的支持。

生成文件的格式是  年-月-日-hello_word.md  标题参数中的空格会被替换成下划线。你也可以通过直接指定日期的方式来创建blog（比如在迁移老blog数据的时候）

    $blogen --post "2012-1-1-hello word"
    
创建后随便找个文本编辑器或者markdown的编辑器就可以去编辑blog的文件了。
新创建的.md 文件头部有一个固定的头部，定义在两行 /// 之间。格式为  变量名＝值
其中 title 和 post_time 是固定的变量，必须存在不能删除，但是可以修改值，比如用英文文件名创建的title值是英文的，在这里可以改成中文，这样文件名是英文的避免一些系统的中文路径不兼容问题。
在此之外可以自己定义额外的变量，这些变量会作为post对象的属性在渲染模板的时候被注入到对象中

Mac下推荐Mou。Windows下可以用 [markdownpad](http://markdownpad.com/)

###4 生成
写好blog后需要经过生成的过程，当然本货在预览的时候已经悄悄的帮你生成过了。当然如果通过markdown可视化编辑器写的几乎不需要预览。就可以通过一条命令直接生成html后上传服务器拉。

    $blogen --rebuild
    
现在暂时是打印了生成的过程列表。我想以后还是改成用显示百分比的方式比较好，如果遇到一个疯狂写手的话

###5 预览
预览部分其实用的bottle来创建的本地测试站点，我默认打开的debug，方便遇到问题大家好给我反馈

    $blogen --server
    
站点启动后通过访问  http://127.0.0.1:5000 即可看到内容了。

站点已经设置成自动reload，所以这个时候就可以开心的修改模板文件添加各种css，js，以及图片文件了。比如添加base.html到templates目录，然后修改index.html以及post.html继承base，blabla，剩下的就跟做一个静态站没啥区别了。

__注意：在static目录放内容的时候现在很蛋痛的只支持往子目录里放内容，而且只支持一级子目录。比如css需要在static下建一个子目录css，然后放到css目录里，js同理可得__

###6 配置
修改配置文件settings.yaml即可。要注意默认生成的两条不能去掉。
可以自己添加配置项到配置文件中。
配置文件会生成一个对象config被注入到模板环境，所以自定义了配置通过{{ config.xxx }} 就能访问了


###7 post对象的属性

* filename       文件名，不带后缀的
* title          标题
* post_date      发布时间（python的datetime对象）
* md_content     Markdown格式的内容
* html_content   HTML格式的内容 

动态属性：
通过markdown文件头部定义的site_name 和 post_time 之外用户自定义的变量

###8 其他需要自己做的或者知道的

1. 学会jinja2的模板，因为本货的模板是基于jinja2的
2. 会配置Python环境，如果是windows用户起码会装setuptools，pip什么的
3. 自己做个静态站点不成问题，不然你怎么改模板啊？当然自己下一套blog模板折腾一下改吧改吧也是能弄出来的
4. comment？自己折腾，第三方的用啥都可以
5. 站点计数？也是，前端代码都自己折腾了，这货也好说了
6. 学会用git，不然你怎么向github提交自己写的内容啊？

###9 已经发现的bug

__注意：刚更新了一个版本到pypi，因为生成的markdown文件目录名的问题导致了push到库后build启动了jekyll编译失败导致无法build发布，所以修改了目录名，请已经按装了的童鞋尽快更新到最新版本__

这个问题已经解决了

    很不幸，刚发到pip就发现了一个bug。我忘了在settings里面放配置首页列表分页的页大小的参数了。   
    今天中午前在pip装过的同学只有换新版才能正常。


###10 New Feature

####0.0.0.7 pre:
1. 将markdown文件头定义的变量动态注入到post对象里。这样就可以在模板里根据这些数据来动态生成点东西
2. 修改了生成的markdown文件头格式，为了不和Jekyll的头部混淆


###11 打算增加的Feature

1. 生成单页，类似Wiki的方式来组织页面 