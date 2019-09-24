---
title: 我的Hexo博客搭建过程与扩展功能记录
date: 2018-11-08 15:35:15
tags:
categories:
top:
description: 快速、简洁且高效的博客框架Hexo
---

Welcome to [Hexo](https://hexo.io/)! This is a guide post to use Hexo. Check [documentation](https://hexo.io/docs/) for
more info. If you get any problems when using Hexo, you can find the answer in
[troubleshooting](https://hexo.io/docs/troubleshooting.html) or you can ask me on
[GitHub](https://github.com/hexojs/hexo/issues).

<!--more-->

## Quick Start

### Create a new post

``` bash
$ hexo new "My New Post"
```

More info: [Writing](https://hexo.io/docs/writing.html)

### Run server

``` bash
$ hexo server
```

More info: [Server](https://hexo.io/docs/server.html)

### Generate static files

``` bash
$ hexo generate
```

More info: [Generating](https://hexo.io/docs/generating.html)

### Deploy to remote sites

``` bash
$ hexo deploy
```

More info: [Deployment](https://hexo.io/docs/deployment.html)


## How to use Hexo and deploy to GitHub Pages
* https://github.com/hexojs/hexo
* https://hexo.io/docs/

### 1. Install Hexo
```
$ sudo npm install -g hexo-cli

$ hexo -v
hexo-cli: 0.1.9
os: Darwin 14.3.0 darwin x64
http_parser: 2.3
node: 0.12.7
v8: 3.28.71.19
uv: 1.6.1
zlib: 1.2.8
modules: 14
openssl: 1.0.1p
```

### 2. Create a project for your GitHub Pages
```
$ hexo init fuhailin.github.io
INFO  Copying data to ~/***/fuhailin.github.io
INFO  You are almost done! Don't forget to run 'npm install' before you start blogging with Hexo!

$ cd fuhailin.github.io

$ npm install
```

### 3. Run a test server for your page on Mac
```
$ hexo server
INFO  Hexo is running at http://0.0.0.0:4000/. Press Ctrl+C to stop.

hexo s --draft  # 预览Draft
```

### 4. Set information for your new blog
https://hexo.io/docs/configuration.html
```
$ vi _config.yml

~~~~~~~~~~~~~~~~~ _config.yml ~~~~~~~~~~~~~~~~~~
# Site
title: fuhailin's note
subtitle:
description: fuhailin's personal blog
author: fuhailin
language:
timezone: Japan

# URL
## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
url: http://fuhailin.github.io/
root: /
permalink: :year/:month/:day/:title/
permalink_defaults:
```

### 5. Set information to use Git
https://github.com/hexojs/hexo-deployer-git
```
$ npm install hexo-deployer-git --save
$ vi _config.yml

~~~~~~~~~~~~~~~~~ _config.yml ~~~~~~~~~~~~~~~~~~
# Deployment
## Docs: http://hexo.io/docs/deployment.html
deploy:
  type: git
    repo: git@github.com:fuhailin/fuhailin.github.io.git
      branch: master
      ```

### 6. Set "watch" before starting your work
"watch" command can monitor your files.
https://hexo.io/docs/generating.html
```
$ hexo generate --watch
```

### 7. Create a new post file
```
$ hexo new first-post
INFO  Created: ~/***/fuhailin.github.io/source/_posts/first-post.md
```

### 8. Edit the above file with Markdown or Hexo's Helper
Hexo's Helper
https://hexo.io/docs/helpers.html
I use Atom with "shift + control + m" when I use Markdown :-)
https://atom.io/

### 9. Delete "source/_posts/hello-world.md"
It's not necessary to deploy.

### 10. Deploy your new blog!!
https://hexo.io/docs/deployment.html
```
$ hexo clean
$ hexo deploy
```
After writting the above command, you can see your new blog on GitHub Pages.
http://******.github.io/

### 11. Change your blog theme
https://github.com/hexojs/hexo/wiki/Themes
```
For instance, How to use the following theme.
https://hexo.io/hexo-theme-light/

## Install it
$ cd fuhailin.github.io
$ git clone https://github.com/theme-next/hexo-theme-next themes/next

## Update the above files
$ themes/light
$ git pull

## Set information to use the theme
$ cd fuhailin.github.io
$ vi _config.yml

~~~~~~~~~~~~~~~~~ _config.yml ~~~~~~~~~~~~~~~~~~
# Extensions
## Plugins: http://hexo.io/plugins/
## Themes: http://hexo.io/themes/
theme: light
```

### 12. Create a new page file
https://hexo.io/docs/writing.html
```
$ hexo new page aboutme
INFO  Created: ~/***/fuhailin.github.io/source/aboutme/index.md

$ cd source/aboutme/

$ vi index.md
```

### 13. Use "Read More"
Write `<!-- more -->` in your articles.

### 14. Use Plugins
https://github.com/hexojs/hexo/wiki/Plugins

## 为blog添加评论区
hexo添加gitment评论系统：
http://kuring.me/post/gitment/

## 给 Github 添加 README
默认情况下，Github中每一个项目，我们希望有一份 README.md 的文件来作为项目的说明，但是我们在项目根目录下的 blog\source
目录下创建一份 README.md 文件，写好说明介绍，部署的时候，这个 README.md 会被 hexo 解析掉，而不会被解析到 Github 中去的。
正确的解决方法其实很简单：
把 README.md 文件的后缀名改成 “MDOWN” 然后扔到`blog/source`文件夹下即可，这样 hexo 不会解析，Github 也会将其作为 MD
文件解析。
https://neveryu.github.io/2016/09/30/hexo-next-two/

## 添加Fork Me on github书签
https://www.jianshu.com/p/2002f4881353

****************************************

## NexT主题下修改文章底部#号tag标签
主题配置文件：set `tag_icon: true`
~~在`~hexo/themes/next/layout/_macro`中找到`post.swig`文件，在内搜索`el="tag">#`，将**#**换成**<i class="fa fa-tag"></i>**即可.~~

******************************
## 添加分享按钮
[theme-next/hexo-next-share](https://github.com/theme-next/hexo-next-share)

******************************
## 显示每篇文章的更新时间

最新版本的next主题已经加入了配置博文更新时间的代码。在主题配置文件中，`post_meta`中有一个`updated_at`属性，如果enable就是开启这个功能。所以我们在博文开头开头部分加入`updated`定义就行：

post Markdown code             |  效果
:-------------------------:|:-------------------------:
![](/uploads/hexo_updatetime2.png) | ![](/uploads/hexo_updatetime1.png)

## 在文章中插入图片

https://fuhailin.github.io/%E5%9C%A8Hexo%E5%8D%9A%E5%AE%A2%E4%B8%AD%E6%8F%92%E5%85%A5%E5%9B%BE%E7%89%87%E7%9A%84%E5%90%84%E7%A7%8D%E6%96%B9%E5%BC%8F/

*********************
## How to create and sync your hexo blog in one repo
https://xiaoyuliu.github.io/2018/03/28/how-to-sync-hexo-blog/
************************
## Hexo标签插件的使用
https://wuchenxu.com/2015/12/08/Static-Blog-hexo-github-6-tag-plugins/
******************
## 在文章中插入代码
自定义 Hexo 博客代码块: https://www.w3ctrain.com/2017/12/11/hexo-code-block/
http://octopress.org/docs/plugins/codeblock/

插入代码文件

把整个文件作为代码插入，这样做的好处是作为可运行的代码后续如果修正了bug，重新hexo g一下文章中的代码就会自动更新；不需要每次从文件中拷贝粘贴代码到文章中。

**配置code存放路径**
在hexo的配置文件`hexo/_config.yml`中看到`code_dir: downloads/code`,说明所有的code文件都放到`source/downloads/code`文件夹下。
**语法**
```
{% include_code [title] [lang:language] path/to/file %}
```
`[title]`:可选，标题名，默认是文件名
`[lang:language]`:可选设置语言后，根据不同的语言设置语法高亮

**举例**
代码文件存放在`source/uploads/code/hello_world.c`.

```
{% include_code lang:c hello world in c lang hello_world.c %}
```
{% include_code lang:c hello world in c lang hello_world.c %}


{% gist 55e8446e255abd3ee2900c3691cca09f trie.py %}

插入gist代码
```
{% gist d27c69e5852f3d0f4e7dc15bb90a2e24 trie.py %}
```

插入github代码
```
{% ghcode github_code_link start_line end_line %}
```

***********************
## 搜索引擎优化SEO
https://fuhailin.github.io/Hexo%E6%90%AD%E5%BB%BA%E5%8D%9A%E5%AE%A2%E8%BF%9B%E9%98%B6%E4%B9%8BSEO%E6%90%9C%E7%B4%A2%E5%BC%95%E6%93%8E%E4%BC%98%E5%8C%96/
****************
## Hexo博客文章添加置顶属性
使用插件[hexo-generator-index-pin-top](https://github.com/netcan/hexo-generator-index-pin-top)
安装：
> $ npm uninstall hexo-generator-index --save
> $ npm install hexo-generator-index-pin-top --save

使用：在需要置顶的**Front-matter**中加上`top: 数字`即可，数字越大，置顶越靠前。

********************
## 自定义Hexo博客的文章模板
博客模版存放在**scaffolds**文件夹
scaffolds文件夹：
```
├── scaffolds					//保存着默认模板，自定义模板就是修改该目录下的文件
│   ├── draft.md 				//默认的草稿模板
│   ├── page.md 				//默认的页面模板
│   └── post.md 				//默认的文章模板
```
在新建文章时，Hexo 会根据 scaffolds 文件夹内相对应的文件来建立文件，例如：
`hexo new draft "My Gallery"`
在执行这行指令时，Hexo 会尝试在 scaffolds 文件夹中寻找 draft.md

http://www.mashangxue123.com/Hexo/353523292.html

*********************

##  博文中嵌入PDF插件

https://github.com/superalsrk/hexo-pdf

********************

## 在博客中显示LaTeX数学公式

我这里使用的是`MathJax` LaTeX渲染引擎和~~`hexo-renderer-markdown-it`~~ [hexo-renderer-kramed](https://github.com/sun11/hexo-renderer-kramed) Markdown解析器
https://theme-next.org/docs/third-party-services/math-equations/

**********************

## 扩展支持emoji表情
https://github.com/crimx/hexo-filter-github-emojis
```
npm install hexo-filter-github-emojis --save
```
**emoji使用方法**

这里有一份emoji与markdown编码的对照表:
[Complete list of github markdown emoji markup · GitHub](https://gist.github.com/rxaviers/7360908)

Emoji test：:blush::cupid::star::hankey::+1::pig::cn::underage::mortar_board::heart_eyes:

但是发现在主页上的emoji表情没有显示出来
****************

## 文章置顶标签及排序
{% asset_img TIM20181212171732.png 'Hexo文章置顶及排序问题+置顶标签' %}
**添加置顶属性**
使用插件[hexo-generator-index-pin-top](https://github.com/netcan/hexo-generator-index-pin-top)
安装：
> $ npm uninstall hexo-generator-index --save
> $ npm install hexo-generator-index-pin-top --save

使用：在需要置顶的**Front-matter**中加上`top: 数字`即可，数字越大，置顶越靠前。

但是我使用的Next主题这样配置目前还不能实现自动给置顶的博文加上置顶标签，需要手动修改代码解决。

**设置置顶标志**

打开：`/blog/themes/next/layout/_macro/post.swig`文件，定位到`<span class="post-time">`标签下，插入如下代码：

```
{% if post.top %}
  <i class="fa fa-thumb-tack"></i>
  <font color=7D26CD>置顶</font>
  <span class="post-meta-divider">|</span>
{% endif %}
```
重新编译博客之后就可以显示了

希望有人能把这个功能提一个pull request到官方库里面，我现在能力还有限。

**References**:
1. [hexo博客优化之文章置顶+置顶标签](https://blog.csdn.net/qwerty200696/article/details/79010629)
2. https://github.com/netcan/hexo-generator-index-pin-top
3. [Hexo置顶及排序问题|叶落阁](https://yelog.org/2017/02/24/hexo-top-sort/)
****************

**Good References:**

Hexo+NexT 打造一个炫酷博客：https://juejin.im/post/5bcd2d395188255c3b7dc1db
Hexo官方中文文档：https://hexo.io/zh-cn/docs/
hexo进阶: http://stevenshi.me/2017/05/09/hexo-advance/
博客写作模板: https://blog.baoyukun.win/%E6%8A%80%E6%9C%AF/%E5%89%8D%E7%AB%AF/a-writing-model/
搭建 Hexo 博客的填坑经历和必要的优化：https://kris2d.info/posts/b706980b/
Hexo程序archive页面数量设置：http://www.yuzhewo.com/2015/11/21/Hexo%E7%A8%8B%E5%BA%8Farchive%E9%A1%B5%E9%9D%A2%E6%95%B0%E9%87%8F%E8%AE%BE%E7%BD%AE/
Hexo博客归档不分页显示设置方法：https://sobaigu.com/hexo-archives-show-all-in-one-page.html
搭建Hexo博客进阶篇---主题自定义（三）：https://www.jianshu.com/p/4b9ee8fec3a3
[Git Pages 使用指南](http://saili.science/2017/04/02/github-for-win/#)
[NexT官方文档](https://theme-next.org/docs/third-party-services/search-services)
