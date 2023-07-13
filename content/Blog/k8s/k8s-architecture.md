Title: Kubernetes Architecture
Date: 2022-07-13 15:24
Modified: 2022-07-13 15:24
Tags: k8s
Keywords: k8s, architecture, kubernetes
Authors: Hephzibah Pon Cellat Arulprakash

A kubernetes cluster is made up of one or more control plane and worker nodes.

## Control Plane

Components of control plane are,

* **kube-apiserver:** It is the frontend for the control plane exposing the Kubernetes API.
* **etcd:** Consistent and highly available key-value store used as Kubernetes backing store for all cluster data.
* **controller manager:** Brain, it takes the decisions to bring up containers. Logically each controller is a separate process, but to reduce complexity, they are all compiled into single binary and run in a single process, some types of these controllers are,
    * **Node controller:** Responsible for noticing and responding when nodes goes down.
    * **Job controller:** Watches for job objects that represent one-off tasks, then creates pods to run those tasks to completion.
    * **EndpointSlice controller:** Populates EndpointSlice objects (to provide a link between service and nodes).
    * **ServiceAccount controller:** Creates default service accounts for new namespaces.
* **kube-scheduler:** Control plane component that watches for newly created pods with no assigned node and selects a node for them to run on. Factors taken into account for scheduling decision includes,
    * individual and collective resource requirements
    * hardware/software/policy constraints
    * affinity and anti-affinity specifications
    * data locality
    * inter-workload interference, and 
    * deadlines

## Worker Nodes

Components of a worker node are,

* **kubelet:** An agent that runs on each worker node in the cluster. It makes sure that containers are running in a Pod. It takes a set of PodSpecs that are provided through various mechanisms (like definition yaml file) and ensures that the containers described in those PodSpecs are running and healthy. It doesnot manage containers which were not created by Kubernetes.
* **kube proxy:** It is a network proxy implementing Kubernetes Service concept. It maintains network rules on nodes. These network rules allow network communication to your Pods from network sessions inside or outside of your cluster. kube-proxy uses the operating system packet filtering layer if available or else forwards the traffic itself.
* **container runtime:** It is responsible for running containers. Kubernetes supports container runtimes such as containerd, CRI-O and any other implementation of Kubernetes CRI (Container Runtime Interface).

## References

* [Kubernetes Documentation](https://kubernetes.io/docs/home/)