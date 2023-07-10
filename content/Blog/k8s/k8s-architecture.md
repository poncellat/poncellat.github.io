Title: Kubernetes Architecture
Date: 2022-05-21 21:36
Modified: 2022-07-10 17:09
Tags: k8s
Keywords: k8s, architecture, kubernetes
Authors: Hephzibah Pon Cellat Arulprakash
Summary: K8S components in master and worker nodes

A kubernetes cluster is made up of one or more control plane and worker nodes.

## Control Plane

Components of control plane are,

* kube-apiserver
* etcd
* controller manager
* kube-scheduler

## Worker Nodes

Components of a worker node are,

* kubelet
* kube proxy
* container runtime