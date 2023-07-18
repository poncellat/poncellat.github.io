Title: Docker Container Lifecycle
Date: 2022-07-11 18:25
Modified: 2022-07-11 18:25
Tags: docker
Keywords: docker
Authors: Hephzibah Pon Cellat Arulprakash

## Docker Container Lifecycle

Running instance of a image is container. It can have below various status.

### **Created**

```
$ docker create -it  --name nginx -v /mydata nginx

$ docker ps -a
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS    PORTS     NAMES
d0306faac16b   nginx     "/docker-entrypoint.…"   2 seconds ago   Created             nginx
```


### **Up**:

This status refers to the container is up and running.

```
$ docker start nginx
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS         PORTS     NAMES
d0306faac16b   nginx     "/docker-entrypoint.…"   About a minute ago   Up 3 seconds   80/tcp    nginx
```

```
$ docker run -dit  --name nginx -v /mydata nginx
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS     NAMES
d9aaa147c753   nginx     "/docker-entrypoint.…"   15 seconds ago   Up 14 seconds   80/tcp    nginx
```

### **Paused**:

```
$ docker pause nginx
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS                       PORTS     NAMES
d9aaa147c753   nginx     "/docker-entrypoint.…"   About a minute ago   Up About a minute (Paused)   80/tcp    nginx

$ docker unpause nginx
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS     NAMES
d9aaa147c753   nginx     "/docker-entrypoint.…"   About a minute ago   Up About a minute   80/tcp    nginx
```

### **Exited**:

```
$ docker stop nginx
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS                     PORTS     NAMES
d9aaa147c753   nginx     "/docker-entrypoint.…"   2 minutes ago   Exited (0) 6 seconds ago             nginx

$ docker start nginx 
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS     NAMES
d9aaa147c753   nginx     "/docker-entrypoint.…"   3 minutes ago   Up 2 seconds   80/tcp    nginx

$ docker kill nginx
nginx
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS                       PORTS     NAMES
b0fe4ba9ee7f   nginx     "/docker-entrypoint.…"   11 seconds ago   Exited (137) 4 seconds ago             nginx
```

### **Deleted**:

```
$ docker stop nginx
$ docker rm nginx
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
$

```
