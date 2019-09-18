---
title: Docker Cheat Sheet
tags: Docker
date: 2019-09-18 23:37:29
categories:
top:
---

为什么要使用Docker：“有了Docker，开发人员能够借助任何工具、使用语言来构建任何应用”。Docker化的应用是完全绿色便携的，能运行在任何平台。

<!-- more -->

## DOcker的安装

Linux：
```
curl -sSL https://get.docker.com/ | sh

```

## Docker Hub

| Docker语法                	| 描述                                                                           	|
|---------------------------	|--------------------------------------------------------------------------------	|
| docker search  searchterm 	| Search Docker Hub for images.                                                  	|
| docker pull user/image    	| Downloads an image from Docker Hub.                                            	|
| docker login              	| Authenticate to Docker Hub (or other Docker registry).                         	|
| docker push user/image    	| Uploads an image to Docker Hub. You must be authenticated to run this command. 	|

## Image and Container Information

| Docker语法                          	| 描述                                                    	|
|-------------------------------------	|---------------------------------------------------------	|
| docker ps                           	| List all running containers.                            	|
| docker ps -a                        	| List all container instances, with their ID and status. 	|
| docker history  user/image          	| Lists the history of an image.                          	|
| docker logs  [container name or ID] 	| Displays the logs from a running container.             	|
| docker port  [container name or ID] 	| Displays the exposed port of a running container.       	|
| docker diff  [container name or ID] 	| Lists the changes made to a container.                  	|


## Work With Images and Containers

| Docker语法                                            	| 描述                                                                                                	|
|-------------------------------------------------------	|-----------------------------------------------------------------------------------------------------	|
| docker run  -it user/image                            	| Runs an image, creating a container and changing the terminal to the terminal within the container. 	|
| docker run  -p $HOSTPORT:$CONTAINERPORT -d user/image 	| Run an image in detached mode with port forwarding.                                                 	|
| ctrl+p then ctrl+q                                    	| From within the container’s command prompt, detach and return to the host’s prompt.                 	|
| docker attach  [container name or ID]                 	| Changes the command prompt from the host to a running container.                                    	|
| docker stop  [container name or ID]                   	| Stop a container.                                                                                   	|
| docker rm -f  [container name or ID]                  	| Delete a container.                                                                                 	|
| docker rmi                                            	| Delete an image.                                                                                    	|
| docker tag  user/image:tag user/image:newtag          	| Add a new tag to an image.                                                                          	|
| docker exec  [container name or ID] shell command     	| Executes a command within a running container.                                                      	|


## Image Creation

| Docker语法                          	| 描述                                                              	|
|-------------------------------------	|-------------------------------------------------------------------	|
| docker commit  user/image           	| Save a container as an image.                                     	|
| docker save  user/image             	| Save an image to a tar archive.                                   	|
| docker build -t sampleuser/ubuntu . 	| Builds a Docker image from a Dockerfile in the current directory. 	|
| docker load                         	| Loads an image from file.                                         	|

## Docker net/http: TLS handshake timeout的解决办法

由于国内网络环境问题，Docker pull国外镜像出现无法使用的网络问题，因此更换国内镜像：
修改`/etc/docker/daemon.json`，添加如下地址：
```json
# 配置代理,此处为阿里云的镜像,可选其他的.
{
  "registry-mirrors": [
    "https://khec465u.mirror.aliyuncs.com"
  ]
}
```

##　解决每次使用Docker命令都需要root权限的问题

将你使用的具有root权限的用户加入docker group：`sudo usermod -aG docker $USER`


https://www.linode.com/docs/applications/containers/docker-commands-quick-reference-cheat-sheet/
