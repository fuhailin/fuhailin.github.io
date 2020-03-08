---
title: 在Hexo博客中插入图片的各种方式
date: 2019-01-04 17:59:38
tags: Hexo
categories: Tools
top:
description: 在Hexo博客中插入图片的各种方式
---

## 在文章中插入图片
[Hexo博客搭建之在文章中插入图片](https://yanyinhong.github.io/2017/05/02/How-to-insert-image-in-hexo-post/)

<!-- more -->

### 绝对路径本地引用
当Hexo项目中只用到少量图片时，可以将图片统一放在source/images文件夹中，通过markdown语法访问它们。
```
![](/images/image.jpg)
```
图片既可以在首页内容中访问到，也可以在文章正文中访问到。

### 相对路径本地引用
图片除了可以放在统一的images文件夹中，还可以放在文章自己的目录中。文章的目录可以通过站点配置文件_config.yml来生成。
`post_asset_folder: true`
将_config.yml文件中的配置项post_asset_folder设为true后，执行命令$ hexo new post_name，在source/_posts中会生成文章post_name.md和同名文件夹post_name。将图片资源放在post_name中，文章就可以使用相对路径引用图片资源了。

```
![](image.jpg)
```

### 标签插件语法引用

这种相对路径的图片显示方法在博文详情页面显示没有问题，但是在首页预览页面图片将显示不出来。如果希望**图片在文章和首页中同时显示**，可以使用标签插件语法。
```
# 本地图片资源，不限制图片尺寸
{% asset_img image.jpg This is an image %}
# 网络图片资源，限制图片显示尺寸
{% img http://www.viemu.com/vi-vim-cheat-sheet.gif 200 400 vi-vim-cheat-sheet %}

```
### HTML语法引用

```html
<img src="SpellCheck.png" width="50%" height="50%" title="拼写检查工具Grammarly." alt="拼写检查工具Grammarly."/>
```
直接将`![](image.jpg)`替换上面的语法即可。

### 启用fancybox：点击查看图片大图

我这里使用的是Hexo的NexT主题，NexT主题中提供了fancybox的方便接口。

Usage：https://github.com/theme-next/theme-next-fancybox3
markdown用法：

```
{% img http://www.viemu.com/vi-vim-cheat-sheet.gif 600 600 "点击查看大图:vi/vim-cheat-sheet" %}
```

**Hexo部分图片禁用fancybox**

hexo在使用fancybox插件时，图片的效果还是很可观的，但是我们往往是不需要所有的图片都用fancybox；
例如：hexo next主题下，添加某些图片的时候，有些事不需要可点击的
修改`theme\next\source\js\src\utils.js` 红色字体部分；

```diff
diff --git a/source/js/src/utils.js b/source/js/src/utils.js
index 0f3704e..8516665 100644
--- a/source/js/src/utils.js
+++ b/source/js/src/utils.js
@@ -11,6 +11,7 @@ NexT.utils = NexT.$u = {
       .not('.group-picture img, .post-gallery img')
       .each(function() {
         var $image = $(this);
+        if ($(this).hasClass('nofancybox')) return;
         var imageTitle = $image.attr('title');
         var $imageWrapLink = $image.parent('a');
```

在img标签使用的时候加上class="nofancybox"即可。

```html
<img src="http://www.viemu.com/vi-vim-cheat-sheet.gif" class="nofancybox" />
```
