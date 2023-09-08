Title: Kubernetes | Autoscaling | Horizontal Pod Autoscaling
Date: 2023-09-08 11:33
Modified: 2023-09-08 11:33
Tags: k8s
Keywords: k8s, autoscaling, kubernetes
Authors: Hephzibah Pon Cellat Arulprakash

This article discusses about Horizontal Pod Autoscaling (HPA), one of the type of autoscaling in kubernetes.

## What is Horizontal Autoscaling

Horizontal autoscaling is that based on the load in CPU and memory, you can scale up or down the number of pods automatically, so that your application can better serve during high or low traffic hours eventually customers can have seemless experience.

For this purpose you would configure the minimum and maximum number of pods to be created based on the metrics like CPU and memory.

There is a concept called vertical autoscaling where you add nodes to increase the infrastructure capacity in terms of CPU, RAM, storage etc.,

## How in Kubernetes

### Deploying sample application using Kubernetes Deployment and Service

Consider below deployment and service definition yaml file `php-apache.yaml`. 

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-apache
spec:
  selector:
    matchLabels:
      run: php-apache
  template:
    metadata:
      labels:
        run: php-apache
    spec:
      containers:
      - name: php-apache
        image: registry.k8s.io/hpa-example
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: 500m
          requests:
            cpu: 200m
---
apiVersion: v1
kind: Service
metadata:
  name: php-apache
  labels:
    run: php-apache
spec:
  ports:
  - port: 80
  selector:
    run: php-apache
```

Assuming you already have a k8s cluster setup, to create deployment and service resource, 

```
$ kubectl apply -f php-apache.yaml
```

This would create a deployment and service as below. From the deployment, replicaset is created and from replicaset, pod is created. so we have a service, deployment, replicaset and a pod.

```
$ kubectl get all
NAME                              READY   STATUS    RESTARTS   AGE
pod/php-apache-7495ff8f5b-gt8r8   1/1     Running   0          4m29s

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/php-apache   ClusterIP   10.100.126.40   <none>        80/TCP    4m29s

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/php-apache   1/1     1            1           4m29s

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/php-apache-7495ff8f5b   1         1         1       4m29s
```

To check if the sample appilication is working, as this service is of type clusterIP, we can either expose the service as nodeport so that it is accessible from host machine, or we can ssh into the cluster and access via the cluster-ip. 

### Testing Application Method 1 (optional)

Expose the service php-apache to a new service of type Nodeport so that it will accessible from your local machine and outside of kubernetes cluster. You can now access the app from local machine using the ip address of cluster followed the port exposed in NodePort.

```
$ kubectl expose service php-apache --port=80 --target-port=80 --name=php-apache-np --type=NodePort
service/php-apache-np exposed
$ kubectl get svc
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
php-apache      ClusterIP   10.100.126.40   <none>        80/TCP         29m
php-apache-np   NodePort    10.102.48.181   <none>        80:30708/TCP   4s
$ minikube ip
192.168.49.2
$ curl http://192.168.49.2:30708
OK!
```

### Testing Application Method 2 (optional)

To ssh into cluster and check the php application, below example assumes the cluster is created using minikube.

```
$ minikube ssh
docker@minikube:~$
```

To check the application, use curl with app ip address. The app ip address can be found in cluster-ip from service. `kubectl get svc`

```
$ minikube ssh
docker@minikube:~$ curl http://10.100.126.40
OK!
```

### Create Metrics Server

Download the latest release of metrics server.

```
curl -LO https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Edit the components.yaml in your favorite text editor, adding below lines

```
  template:
    metadata:
      labels:
        k8s-app: metrics-server
    spec:
      hostNetwork: true
      containers:
      - args:
        - --kubelet-insecure-tls
        - --cert-dir=/tmp
        - --secure-port=4443
```

Apply the components.yaml

```
kubectl apply -f components.yaml
```

Check for the pods in namespace kube-system

```
$ kubectl get pod  -n kube-system
NAME                               READY   STATUS    RESTARTS      AGE
...
metrics-server-77d9b56856-qjxh7    1/1     Running   0             3m32s
...
```

Check if its installed properly by,

```
$ kubectl top nodes

NAME       CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
minikube   389m         19%    901Mi           11%     

$ kubectl top pods
NAME                          CPU(cores)   MEMORY(bytes)   
php-apache-7495ff8f5b-gt8r8   1m           31Mi    
```

If it is installed properly you will see the output about the CPU, memory metrics as shown above.

### Create the Horizontal Pod AutoScaler

Create a Horizontal Pod Autoscaler which would autoscale if the CPU usage goes beyond 50% with the minimum and maximum number of pods to be autoscaled.

```
$ kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
```

View the HPA resource

```
$ kubectl get hpa
NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache   0%/50%    1         10        1          65m
```

As currently the application has no load, the target is 0%. HPA gets this information from the metrics server installed previously.

### Increase the Load

To increase the load we will be using busybox image, which continously access the application in a loop. In a new terminal,
```
$ kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```

In the other terminal, after a while, you can see target % is increased leading to autoscale out the deployment which affects the replicasets which in turn increases the number of pods to handle the load.

```
$ kubectl get all
NAME                              READY   STATUS    RESTARTS      AGE
pod/load-generator                1/1     Running   0             105s
pod/php-apache-7495ff8f5b-gfzhb   1/1     Running   0             68s
pod/php-apache-7495ff8f5b-gt8r8   1/1     Running   1 (72m ago)   4h
pod/php-apache-7495ff8f5b-j8fb9   1/1     Running   0             69s
pod/php-apache-7495ff8f5b-p26g7   1/1     Running   0             53s
pod/php-apache-7495ff8f5b-vhxt8   0/1     Pending   0             8s
pod/php-apache-7495ff8f5b-wzlr4   1/1     Running   0             84s

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/kubernetes      ClusterIP   10.96.0.1       <none>        443/TCP        4h1m
service/php-apache      ClusterIP   10.100.126.40   <none>        80/TCP         4h
service/php-apache-np   NodePort    10.102.48.181   <none>        80:30708/TCP   3h31m

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/php-apache   5/6     6            5           4h

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/php-apache-7495ff8f5b   6         6         5       4h

NAME                                             REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
horizontalpodautoscaler.autoscaling/php-apache   Deployment/php-apache   56%/50%   1         10        5          70m
```

Now stop the load to the application by Ctrl+C in the terminal where busybox was run. After few mins you can see the pods would have autoscaled down, decreasing the number of pods due to less or no traffic to the application.

```
$ kubectl get all
NAME                              READY   STATUS    RESTARTS      AGE
pod/php-apache-7495ff8f5b-gt8r8   1/1     Running   1 (78m ago)   4h7m

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/kubernetes      ClusterIP   10.96.0.1       <none>        443/TCP        4h7m
service/php-apache      ClusterIP   10.100.126.40   <none>        80/TCP         4h7m
service/php-apache-np   NodePort    10.102.48.181   <none>        80:30708/TCP   3h37m

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/php-apache   1/1     1            1           4h7m

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/php-apache-7495ff8f5b   1         1         1       4h7m

NAME                                             REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
horizontalpodautoscaler.autoscaling/php-apache   Deployment/php-apache   0%/50%    1         10        1          76m
```
### Cleanup

- Remove the application deployment and service

```
kubectl delete -f php-apache.yaml
```

- Optionally remove the NodePort service if created

```
kubectl delete svc php-apache-np
```

- Remove the metrics server

```
kubectl delete -f components.yaml
```

- Remove HPAs

```
kubectl delete hpa php-apache
```
