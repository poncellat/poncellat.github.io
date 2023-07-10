Title: Troubleshoot high latency database
Date: 2022-07-10 19:39
Modified: 2022-07-10 19:39
Tags: troubleshoot
Keywords: troubleshoot, debug, high latency, latency, database
Authors: Hephzibah Pon Cellat Arulprakash

## Problem Statement

How would you troubleshoot a high latency database application, consider a user is experiencing delays per hits to an application due to database latency.

## Troubleshooting

Latency describes the amount of delay on a network or Internet connection. Low latency implies that there are no or almost no delays. High latency implies that there are many delays. One of the main aims of improving performance is to reduce latency.

Latency can be due to external or internal factors, below are few points to troubleshoot,

* **Database Type:** Use proper database type
* **Disk Latency:** Check if the storage hardware is efficient
* **Geo Distributed:** Ensure to use geo distributed for low latency and high availability
* **Scaling:** Based on traffic, scale in or scale out, horizontal or vertical

### Database Type

nosql has low latency compared to traditional RDBMS

### Disk Latency

The type of storage hardware used to store plays a major role, choose the best volume among ssd, network share, or cloud based like EBS

### Geo Distributed

Having replicas in various geographical location ultimately reduce latency as the request from users hits the nearest location.

### Scaling

Horizontal scaling, adding more instance.
Vertical scaling, adding more CPU, RAM.
Checkout the logs for the memory, CPU used.


## Reference

* https://developer.mozilla.org/en-US/docs/Web/Performance/Understanding_latency