---
title: 常用Git操作清单
date: 2019-01-15 19:07:09
tags: Git
categories: Tools
top:
---
 **欢迎使用Git工具进行项目管理, 下面是我整理的常用 Git 操作清单。**

<!-- more -->

几个专用名词的译名如下。

>Workspace：工作区
>Index / Stage：暂存区
>Repository：仓库区（或本地仓库）
>Remote：远程仓库

# 一、新建代码库

> `git init`: 在当前目录新建一个Git代码库
> `git init [project-name]`: 新建一个目录，将其初始化为Git代码库
> `git clone [url]`: 下载一个项目和它的整个代码历史

# 二、配置

Git的设置文件为 .gitconfig ，它可以在用户主目录下（全局配置），也可以在项目目录下（项目配置）。
> `git config --list` : 显示当前的Git配置
> `git config -e [--global]` : 编辑Git配置文件

**git命令行下面显示中文字符**:

> `git config --global core.quotepath false`: 由于Git默认引用非ASCII 字符，disable它的引用行为可以用这个命令
 设置提交代码时的用户信息
> `git config [--global] user.name "Your Name"`
> `git config [--global] user.email you@example.com`

# 三、增加/删除文件

**git add**: 把文件加入暂存区

 > `git add -A` : stages All
 > `git add .` : stages new and modified, without deleted
 > `git add -u` ： stages modified and deleted, without new
所以`git add -A` 等于  `git add .; git add -u`
 > `git add [file1] [file2] ...`: 添加指定文件到暂存区staging area
 > `git add [dir]`: 添加指定目录到暂存区，包括子目录
 > `git add -p`: 添加每个变化前，都会要求确认; 对于同一个文件的多处变化，可以实现分次提交

 删除工作区文件：
 > `git rm [file1] [file2] ...`: 删除工作区文件，并且将这次删除放入暂存区
 > `git rm --cached [file]`: 停止追踪指定文件，但该文件会保留在工作区
 > `git mv [file-original] [file-renamed]`: 改名文件，并且将这个改名放入暂存区

# 四、代码提交

 **git commit**: To save t	he changes in the staging area.

 >`git commit -m "write your log message here."` : to save the changes in the staging area with your log message.
 >`git commit [file1] [file2] ... -m [message]`: 提交暂存区的指定文件到仓库区

 If you use a command `git commit` without message ,you will open a log editors.
 **【Tip】**:To save what you have written, type <kbd>Ctrl</kbd>+<kbd>O </kbd>to write the file out, then<kbd> Enter </kbd>to confirm the filename, then <kbd>Ctrl</kbd>+<kbd>X</kbd> and <kbd>Enter</kbd> to exit the editor.

 >`git commit -a`：--all       提交工作区自上次commit之后的变化，直接到仓库区
  Tell the command to automatically stage files that have been modified and deleted, but new files you have not told Git about are not affected.
 >`git commit -v`：提交时显示所有diff信息
 >`git commit --amend -m [message]`: 使用一次新的commit，替代上一次提交;如果代码没有任何新变化，则用来改写上一次commit的提交信息
 >`git commit --amend [file1] [file2] ...`: 重做上一次commit，并包括指定文件的新变化


# 五、分支

 > `git branch`: 列出所有本地分支
 > `git branch -r`: 列出所有远程分支
 > `git branch -a`: 列出所有本地分支和远程分支
 > `git branch [branch-name]`: 新建一个分支，但依然停留在当前分支
 > `git checkout -b [branch]`: 新建一个分支，并切换到该分支
 > `git branch [branch] [commit]`: 新建一个分支，指向指定commit
 > `git branch --track [branch] [remote-branch]`: 新建一个分支，与指定的远程分支建立追踪关系
 > `git checkout [branch-name]`: 切换到指定分支，并更新工作区
 > `git checkout -`: 切换到上一个分支
 > `git branch --set-upstream [branch] [remote-branch]`: 建立追踪关系，在现有分支与指定的远程分支之间
 > `git checkout -b Hailin/leetcode：` : 新建一个在“Hailin”目录下的“leetcode”分支，并切换到其上
  ![这里写图片描述](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/20180312111635714.png)

 > `git merge [branch]`: 合并指定分支到当前分支
 > `git cherry-pick [commit]`: 选择一个commit，合并进当前分支
 > `git branch -d [branch-name]`: 删除分支
 删除远程分支:
 > `git push origin --delete [branch-name]`
 > `git branch -dr [remote/branch]`

 ![这里写图片描述](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/20180312111754710.png)

# 六、标签

 > `git tag`: 列出所有tag
 > `git tag [tag]` # 新建一个tag在当前commit
 > `git tag [tag] [commit]` # 新建一个tag在指定commit
 > `git tag -d [tag]` # 删除本地tag
 > `git push origin :refs/tags/[tagName]`  # 删除远程tag
 > `git show [tag]` # 查看tag信息
 > `git push [remote] [tag]` # 提交指定tag
 > `git push [remote] --tags` # 提交所有tag
 > `git checkout -b [branch] [tag]`  # 新建一个分支，指向某个tag


# 七、查看信息

 > `git status` # 显示有变更的文件 Which displays a list of the files that have been modified since the last time changes were saved.

**git log**: 显示当前分支的版本历史 To view the log of the project's history. When you run `git log`, Git automatically uses a pager to show one screen of output at a time. Press the <kbd>space </kbd>bar to go down a page or the<kbd> q </kbd>key to quit.
 > `git log path"` : to inspect only the changes to particular files or directories.where `path` is the path to a specific file or directory. The log for a file shows changes made to that file; the log for a directory shows when files were added or deleted in that directory, rather than when the contents of the directory's files were changed.
 > `git log --stat` # 显示commit历史，以及每次commit发生变更的文件
 > `git log -S [keyword]` # 搜索提交历史，根据关键词
 > `git log [tag] HEAD --pretty=format:%s` # 显示某个commit之后的所有变动，每个commit占据一行
 > `git log [tag] HEAD --grep feature` # 显示某个commit之后的所有变动，其"提交说明"必须符合搜索条件

 显示某个文件的版本历史，包括文件改名:
 > git log --follow [file]
 > `git whatchanged [file]`

 > `git log -p [file]` # 显示指定文件相关的每一次diff
 > `git log -5 --pretty --oneline` # 显示过去5次提交
 > `git shortlog -sn` # 显示所有提交过的用户，按提交次数排序
 > `git blame [file]` # 显示指定文件是什么人在什么时间修改过

 **git diff**: 显示暂存区和工作区的差异 Without any filenames will show you all the changes in your repository
 > `git diff --cached [file]` # 显示暂存区和上一个commit的差异
 > `git diff HEAD` # 显示工作区与当前分支最新commit之间的差异
 > `git diff [first-branch]...[second-branch]` # 显示两次提交之间的差异
 > `git diff --shortstat "@{0 day ago}"` # 显示今天你写了多少行代码
  >`git diff filename` : to compare the file as it currently is to what you last saved
  > `git diff directory`: will show you the changes to the files in some directory.
  > `git diff -r HEAD path/to/file`: To compare a file's current state to the changes in the staging area.  The` -r     `flag means "compare to a particular revision", `HEAD` is a shortcut meaning "the most recent commit"
  > `git diff -r HEAD~1`: The label `HEAD~1` then refers to the commit before it, while `HEAD~2` refers to the commit before that, and so on.

  **git show**: To view the details of a specific commit.
  >`git show 77d3` : you can use the command `git show` with the first few characters of the commit's hash.
 > `git show [commit]` # 显示某次提交的元数据和内容变化
 > `git show --name-only [commit]` # 显示某次提交发生变化的文件
 > `git show [commit]:[filename]` # 显示某次提交时，某个文件的内容
 > `git reflog` # 显示当前分支的最近几次提交

# 八、远程同步

 > `git fetch [remote]` # 下载远程仓库的所有变动
 > `git remote -v` # 显示所有远程仓库
 > `git remote show [remote]` # 显示某个远程仓库的信息
 > `git remote add [shortname] [url]` # 增加一个新的远程仓库，并命名
 > `git pull [remote] [branch]` # 取回远程仓库的变化，并与本地分支合并
 > `git push [remote] [branch]` # 上传本地指定分支到远程仓库
 > `git push [remote] --force` # 强行推送当前分支到远程仓库，即使有冲突
 > `git push [remote] --all` # 推送所有分支到远程仓库

# 九、撤销
 > `git checkout [file]` # 恢复暂存区的指定文件到工作区
 > `git checkout [commit] [file]` # 恢复某个commit的指定文件到暂存区和工作区
 > `git checkout .` # 恢复暂存区的所有文件到工作区
 > `git reset [file]` # 重置暂存区的指定文件，与上一次commit保持一致，但工作区不变
 > `git reset --hard` # 重置暂存区与工作区，与上一次commit保持一致
 > `git reset [commit]` # 重置当前分支的指针为指定commit，同时重置暂存区，但工作区不变
 > `git reset --hard [commit]` # 重置当前分支的HEAD为指定commit，同时重置暂存区和工作区，与指定commit一致
 >` git reset --keep [commit]` # 重置当前HEAD为指定commit，但保持暂存区和工作区不变
  新建一个commit，用来撤销指定commit
 后者的所有变化都将被前者抵消，并且应用到当前分支:
 > `git revert [commit]`


**git stash**: 暂时将未提交的变化移除,保存当前工作进度，会把暂存区和工作区的改动保存起来
 > `git stash save 'message...'` : 可以添加一些注释
 > `git stash list` : 显示保存进度的列表。也就意味着，git stash命令可以多次执行。
 > `git stash pop`  :恢复最新的进度到工作区。git默认会把工作区和暂存区的改动都恢复到工作区。
 > `git stash pop --index` : 恢复最新的进度到工作区和暂存区。（尝试将原来暂存区的改动还恢复到暂存区）
 > `git stash pop stash@{1}` : 恢复指定的进度到工作区。stash_id是通过git stash list命令得到的
 通过 `git stash pop` 命令恢复进度后，会删除当前进度。
 > `git stash drop [stash_id]` : 删除一个存储的进度。如果不指定stash_id，则默认删除最新的存储进度
 > `git stash clear`: 删除所有存储的进度。
 > `git stash apply [–index] [stash_id]` :  除了不删除恢复的进度之外，其余和git stash pop 命令一样。

# 十、其他

 > `git archive` # 生成一个可供发布的压缩包

# 十一、中国大陆地区下载Github源代码速度慢的解决办法

这里记录在Windows系统下clone github代码速度太慢的解决办法，亲测有效！

由于网络环境的限制，clone github代码速度只有4kb/s，实在是太慢了挂了VPN也一样。通过添加DNS可以解除一些网络限制：
 1. 查询网站的IP地址，进入( http://tool.chinaz.com/dns )，输入 github.com，结果如下所示：![](http://www.pianshen.com/images/926/09c9ece225c2cde531d00373dfc6a72e.JPEG) 得到github.com对应两个IP地址，使用`ping`命令测试两个地址，选择一个TTL值较小的IP地址。
 2. 接着，我们打开电脑的 `C:\Windows\System32\drivers\etc` 目录，找到hosts文件; Linux系统下在`/etc/hosts`
 3. 在文件末追加
```
151.101.197.194 github.global.ssl.fastly.net
192.30.253.112 github.com
```
保存后刷新DNS缓存。重新clone github， 速度得到明显提升，从4kb/s到300kb/s.

# 十二、Sync Git Fork to the Original Repo
```bash
$ git remote add upstream https://github.com/[Original Owner Username]/[Original Repository].git
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
$ git push
```
[Sync your Git Fork to the Original Repo](https://digitaldrummerj.me/git-syncing-fork-with-original-repo/)

# 十三、Git submodules
git submodules子模块功能允许你将其他的git 项目包含在你的项目当中，它能让你将另一个仓库克隆到自己的项目中，同时还保持提交的独立。
> `git submodule add [url]` ： 为当前项目添加子模块
> `cat .gitmodules` : submodules 存储在 `.gitmodules`项目配置文件中:
  ![](2019-02-17-123643.png)

> `git submodule add [url]` ： 为当前项目添加子模块

  ## Project workflow with submodules：
  ```bash
  git clone [parent_url]
  git submodule init
  git submodule update
  ```

  ## 如何删除submodules：
  1. Delete the relevant line from the .gitmodules file.
  2. Delete the relevant section from .git/config.
  3. Run git rm –cached path_to_submodule (no trailing slash).
  4. Commit and delete the now untracked submodule files.
  [(Stack Overflow reference)](http://stackoverflow.com/questions/1260748/how-do-i-remove-a-git-submodule)
