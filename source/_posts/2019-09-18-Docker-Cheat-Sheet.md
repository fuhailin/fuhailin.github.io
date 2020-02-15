---
title: Docker Cheat Sheet
tags: [Docker,Kubernets]
date: 2019-09-18 23:37:29
categories:
top:
---

为什么要使用Docker：“有了Docker，开发人员能够借助任何工具、使用语言来构建任何应用”。Docker化的应用是完全绿色便携的，能运行在任何平台。

<!-- more -->

## Docker的安装

Linux：
```bash
curl -sSL https://get.docker.com/ | sh

```

OR

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/Screenshot from 2019-09-20 22-12-42.png)

## Docker Hub

| Docker语法                | 描述                                                         |
| ------------------------- | ------------------------------------------------------------ |
| docker search  searchterm | Search Docker Hub for images.                                |
| docker pull user/image    | Downloads an image from Docker Hub.                          |
| docker login              | Authenticate to Docker Hub (or other Docker registry).       |
| docker push user/image    | Uploads an image to Docker Hub. You must be authenticated to run this command. |



## Image and Container Information

| Docker语法                         | 描述                                                    |
| ---------------------------------- | ------------------------------------------------------- |
| docker ps                          | List all running containers.                            |
| docker ps -a                       | List all container instances, with their ID and status. |
| docker history user/image          | Lists the history of an image.                          |
| docker logs [container name or ID] | Displays the logs from a running container.             |
| docker port [container name or ID] | Displays the exposed port of a running container.       |
| docker diff [container name or ID] | Lists the changes made to a container.                  |

## Work With Images and Containers

| Docker语法                                           | 描述                                                         |
| ---------------------------------------------------- | ------------------------------------------------------------ |
| docker run -it user/image                            | Runs an image, creating a container and changing the terminal to the terminal within the container. |
| docker run -p $HOSTPORT:$CONTAINERPORT -d user/image | Run an image in detached mode with port forwarding.          |
| ctrl+p then ctrl+q                                   | From within the container’s command prompt, detach and return to the host’s prompt. |
| docker attach [container name or ID]                 | Changes the command prompt from the host to a running container. |
| docker stop [container name or ID]                   | Stop a container.                                            |
| docker rm -f [container name or ID]                  | Delete a container.                                          |
| docker rmi                                           | Delete an image.                                             |
| docker tag user/image:tag user/image:newtag          | Add a new tag to an image.                                   |
| docker exec [container name or ID] shell command     | Executes a command within a running container.               |

## Image Creation

| Docker语法                          | 描述                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| docker commit user/image            | Save a container as an image.                                |
| docker save user/image              | Save an image to a tar archive.                              |
| docker build -t sampleuser/ubuntu . | Builds a Docker image from a Dockerfile in the current directory. |
| docker load                         | Loads an image from file.                                    |

## Docker net/http: TLS handshake timeout的解决办法

由于国内网络环境问题，Docker pull国外镜像出现无法使用的网络问题，因此更换国内镜像：
修改 `sudo vim /etc/docker/daemon.json`，添加如下地址：

```json
{
  "registry-mirrors": [
    "https://khec465u.mirror.aliyuncs.com"
  ]
}
```
重启Docker服务：`sudo service docker restart`

##　解决每次使用Docker命令都需要root权限的问题

将你使用的具有root权限的用户加入docker group： ``sudo usermod -aG docker $USER``


https://www.linode.com/docs/applications/containers/docker-commands-quick-reference-cheat-sheet/

*******

# Kubernets
**Deploying the Dashboard UI**：`kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml`
[使用 kubeconfig 或 token 进行用户身份认证](https://jimmysong.io/kubernetes-handbook/guide/auth-with-kubeconfig-or-token.html)
**生成 token**

需要创建一个admin用户并授予admin角色绑定，使用下面的yaml文件创建admin用户并赋予他管理员权限，然后可以通过token访问kubernetes，该文件见[admin-role.yaml](https://github.com/rootsongjc/kubernetes-handbook/tree/master/manifests/dashboard-1.7.1/admin-role.yaml)。

```bash
# 创建 serviceaccount 和角色绑定:
$ kubectl create -f admin-role.yaml
# 获取admin-token的secret名字:
$ kubectl -n kube-system get secret|grep admin-token
# 获取token的值
$ kubectl -n kube-system describe secret admin-token-528zm
# 使用 kubectl 提供的 Proxy 服务来访问Dashboard
# 如果8001端口号占用，加 --port 8002 参数
kubectl proxy
# 打开如下地址：
# http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/
```

![/ ](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/Screen Shot 2019-12-20 at 11.16.39 AM.png)
[Docker Volumes: Why, When, and Which Ones?](https://spin.atomicobject.com/2019/07/11/docker-volumes-explained/)

[Python项目容器化实践(四) - Kubernetes基础篇](https://www.dongwm.com/post/use-kubernetes-1/)
[Deploying Python ML Models with Flask, Docker and Kubernetes](https://alexioannides.com/2019/01/10/deploying-python-ml-models-with-flask-docker-and-kubernetes/)
