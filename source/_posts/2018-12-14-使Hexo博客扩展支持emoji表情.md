---
title: 使Hexo博客扩展支持emoji表情
date: 2018-12-14 14:25:45
tags: Hexo
categories:
top:
---

你的博客支持emoji吗？:smirk:快开看看我是怎么做的吧:secret:

<!--more-->

如何让 markdown 可以解析 emoji 呢？实际上我们发现，在编辑器中输入 `:blush:` 并没有表情出现，是为什么呢？

这是 markdown 渲染引擎的问题 ，将 markdown 变成 html 的转换器叫做markdown渲染器 。 Hexo默认是采用**hexo-renderer-marked**,这个渲染器不支持插件扩展，当然就不行了，还有一个支持插件扩展的是 **hexo-renderer-markdown-it**，这个支持插件配置，可以使用**markwon-it-emoji** 插件来支持emoji。需要将原来的 **marked** 渲染器换成 **markdown-it**渲染器。所以我们可以使用这个渲染引擎来支持emoji表情。

##### 卸载hexo默认的marked渲染器

首先进入博客根目录

> npm un hexo-renderer-marked --save

我这里卸载遇到了如下的错误：
```
npm ERR! path C:\Users\Hailin\Documents\Projects\fuhailin.github.io\node_modules\.bin\marked
npm ERR! code EEXIST
npm ERR! Refusing to delete C:\Users\Hailin\Documents\Projects\fuhailin.github.io\node_modules\.bin\marked: is outside C:\Users\Hailin\Documents\Projects\fuhailin.github.io\node_modules\marked and not a link
npm ERR! File exists: C:\Users\Hailin\Documents\Projects\fuhailin.github.io\node_modules\.bin\marked
npm ERR! Move it away, and try again.

npm ERR! A complete log of this run can be found in:
npm ERR!     C:\Users\Hailin\AppData\Roaming\npm-cache\_logs\2018-12-14T07_45_51_463Z-debug.log
```

看提示应该是npm编译的binary文件链接问题，错误指向`node_modules\.bin\marked`这个文件，而**node_modules**这个文件夹下面的内容都是可以通过`npm`再download下来的，所以我们可以直接先删除**node_modules**文件夹，然后再：

```bash
npm install
npm un hexo-renderer-marked --save
```

##### 安装新的渲染器和emoji插件
```bash
npm i hexo-renderer-markdown-it --save
npm install markdown-it-emoji --save
```
据说 [hexo-renderer-markdown-it](https://github.com/hexojs/hexo-renderer-markdown-it) 的速度要比 Hexo 原装插件要快，而且功能更多


##### 编辑站点配置文件

在站点配置文件后面追加如下内容：

```
# Markdown-it config
## Docs: https://github.com/celsomiranda/hexo-renderer-markdown-it/wiki
markdown:
  render:
    html: true
    xhtmlOut: false
    breaks: true
    linkify: true
    typographer: true
    quotes: '“”‘’'
  plugins:
    - markdown-it-abbr
    - markdown-it-footnote
    - markdown-it-ins
    - markdown-it-sub
    - markdown-it-sup
    - markdown-it-emoji  ## add emoji
  anchors:
    level: 2
    collisionSuffix: 'v'
    # If `true`, creates an anchor tag with a permalink besides the heading.
    permalink: false
    permalinkClass: header-anchor
    # The symbol used to make the permalink
    permalinkSymbol: ¶
```

##### emoji使用方法

这里有一份emoji与markdown编码的对照表:[Complete list of github markdown emoji markup · GitHub](https://gist.github.com/rxaviers/7360908)

Emoji test：:blush::cupid::star::hankey::+1::pig::cn::underage::mortar_board::heart_eyes:

**References**:
1. [Hexo中添加emoji表情](https://chaxiaoniu.oschina.io/2017/07/10/HexoAddEmoji/)
2. [Complete list of github markdown emoji markup · GitHub](https://gist.github.com/rxaviers/7360908)
3. [Hexo置顶及排序问题|叶落阁](https://yelog.org/2017/02/24/hexo-top-sort/)
