---
title: Hello-Hexo
date: 2018-11-08 15:35:15
updated: 2018-11-11 12:15:27  # 搜狗输入法：sj 快速输入当前时间
tags: Hexo
categories: 实用工具笔记
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
$ git clone git://github.com/tommy351/hexo-theme-light.git themes/light

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

## 显示每篇文章的更新时间

最新版本的next主题已经加入了配置博文更新时间的代码。在主题配置文件中，`post_meta`中有一个`updated_at`属性，如果enable就是开启这个功能。所以我们在博文开头开头部分加入`updated`定义就行：

post Markdown code             |  效果
:-------------------------:|:-------------------------:
![](/uploads/hexo_updatetime2.png) | ![](/uploads/hexo_updatetime1.png)

## 在文章中插入图片
[Hexo博客搭建之在文章中插入图片](https://yanyinhong.github.io/2017/05/02/How-to-insert-image-in-hexo-post/)

### 绝对路径本地引用
当Hexo项目中只用到少量图片时，可以将图片统一放在source/images文件夹中，通过markdown语法访问它们。
```
![](/images/image.jpg)
```

### 相对路径本地引用
图片除了可以放在统一的images文件夹中，还可以放在文章自己的目录中。文章的目录可以通过站点配置文件_config.yml来生成。
`post_asset_folder: true`
将_config.yml文件中的配置项post_asset_folder设为true后，执行命令$ hexo new post_name，在source/_posts中会生成文章post_name.md和同名文件夹post_name。将图片资源放在post_name中，文章就可以使用相对路径引用图片资源了。
```
![](image.jpg)
```

这种相对路径的图片显示方法在博文详情页面显示没有问题，但是在首页预览页面图片将显示不出来。如果希望图片在文章和首页中同时显示，可以使用标签插件语法。
```
{% asset_img image.jpg This is an image %}
```
直接将`![](image.jpg)`替换上面的语法即可。

## How to create and sync your hexo blog in one repo
https://xiaoyuliu.github.io/2018/03/28/how-to-sync-hexo-blog/

## Hexo标签插件的使用
https://wuchenxu.com/2015/12/08/Static-Blog-hexo-github-6-tag-plugins/


**Good References:**

Hexo+NexT 打造一个炫酷博客：https://juejin.im/post/5bcd2d395188255c3b7dc1db
