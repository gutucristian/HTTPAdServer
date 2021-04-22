# Simulmedia Take Home Coding Project

The project and presentation must show knowledge around:

- Coding
- Testing
- Architecture and design
- Scalability
- Security

## Project Description

Advertisers would like to run ad campaigns that target video game players based on the country they're in and the language they speak.

The ask is to design and implement an **HTTP ad server** that a video game can use to determine **which ad to show next (if any)** given the **country**, and the **language** of the player.

The game can provide those two parameters as part of the ad request (e.g. `GET http://localhost:8080/ad_request?country=us&lang=eng`).

If there is an ad available, the response must include the id and the url of the ad. Otherwise, an appropriate error should be returned.

### Ad campaign service

There already is a *fake* service that provides all available ads. You can retrieve them through a `GET` call to `https://gist.githubusercontent.com/victorhurdugaci/22a682eb508e65d97bd5b9152f564ab3/raw/dbf27ef217dba9bbd753de26cdabf8a91bdf1550/sm_ads.json`

Example:

```
{
    "ads": [
        {
            "id": "59d4fb16",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "country": "us",
            "lang": "eng",
            "start_hour": 1,
            "end_hour": 14
        },
        ...
```

This ad is available in the `US`, for `English` speakers, between `1:00:00AM` and `1:59:59PM` (inclusive).

# Presentation

[Link](https://docs.google.com/presentation/d/1MiJB5L6GREHVRUmlwdw0aFR1VU6ayJ6rgooTki8Ry7Q/edit?usp=sharing) to the Google Slides presentation

# Usage

## Using Sample API Client

Run `python3 client.py`

This makes a call to Cognito, authenticates the user, receives a JWT token and uses it to hit the HTTP ad server at `https://api.gutucristian.com/ad_request?country=us&lang=eng`

```
import requests
import json

user_data = {
  'AuthParameters' : {
    'USERNAME' : 'foo', 
    'PASSWORD' : 'fooBarBaz1!'
  }, 
  'AuthFlow' : 'USER_PASSWORD_AUTH', 
  'ClientId' : '6p0to3eafoghamofcdv7mntf3g'
}

headers = {'Content-Type': 'application/x-amz-json-1.1', 'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth' }
resp = requests.post('https://cognito-idp.us-east-1.amazonaws.com', data=json.dumps(user_data), headers=headers)

token = json.loads(resp.content)['AuthenticationResult']['AccessToken']

response = requests.get('https://api.gutucristian.com/ad_request?country=us&lang=eng', headers={'Authorization': token})

print('Response status code: {}'.format(response.status_code)) # prints 200
print('Response data: {}'.format(response.text)) # prints {"id":"a0ae3f4279ea4e099b0d668220aba373","videoUrl":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
```

## Using `curl` and Postman 

```
curl -X POST --data @userData.json \
-H 'X-Amz-Target: AWSCognitoIdentityProviderService.InitiateAuth' \
-H 'Content-Type: application/x-amz-json-1.1' \
https://cognito-idp.us-east-1.amazonaws.com/
```

File `userData.json`:

```
{"AuthParameters" : {"USERNAME" : "foo", "PASSWORD" : "fooBarBaz1!"}, "AuthFlow" : "USER_PASSWORD_AUTH", "ClientId" : "6p0to3eafoghamofcdv7mntf3g"}
```

Response:

```
{"AuthenticationResult":{"AccessToken":"eyJraWQiOiJhSFdMcGtpUFlKc1NhTWM5VDNuelZRWkh1ZmlRMENQdDdNclhVUUJDMnBjPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI1ZjM1ODJmYS0zMDljLTQyNzgtYWUwZC05MjA5NjA5YjRkMzEiLCJldmVudF9pZCI6ImM3YzMwMzI1LWY4YzUtNDcxNi1hYWEwLTcwOGRlNGU1NTgwYiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2MTkxMDY5MjQsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX2txdUphUnBKVSIsImV4cCI6MTYxOTE5MzMyNCwiaWF0IjoxNjE5MTA2OTI0LCJqdGkiOiI5ZGFmYjZkMC0zNTZkLTQ3ZGEtODVlOS1iZTE5MGE3ZGVlOTgiLCJjbGllbnRfaWQiOiI2cDB0bzNlYWZvZ2hhbW9mY2R2N21udGYzZyIsInVzZXJuYW1lIjoiZm9vIn0.TzAvvAqwvkc4jsTblnBQ0HeFr-DutytmQKyIhamfnlSA40guaBOq38DAq8wn7-hatIW1CgT-GM19b0BdQZywWMJtooOzTZm9lLHcJhUd3FjO9B_J65t4UpN_i0SNXJAd5I4pYZDFj-1n0J6fA9ezknhFrtE2Aa1meOSJjMCvstT6P2t7CLK5qpZtC1T905NcN4VClGW6XCsYhZ7wKw8vx1Kq-qf8Mgg7J_1MxhqihT8lGCvJSoF5B4Zz5fAvBfsPvGVmwd6mVeYRHdW8v5LUlu3DZ-lx-YVkS-98EW3o_JaUAZrJulx10TUJk-Q8AHMlEJhbecg9B6j4t_D1B9POag","ExpiresIn":86400,"IdToken":"eyJraWQiOiI3NzFoSWNpeG5OQU1KMVJZY3FiQWVWVWt1UTkzTW5taDAwYVhhdkJjNWZNPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI1ZjM1ODJmYS0zMDljLTQyNzgtYWUwZC05MjA5NjA5YjRkMzEiLCJhdWQiOiI2cDB0bzNlYWZvZ2hhbW9mY2R2N21udGYzZyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJldmVudF9pZCI6ImM3YzMwMzI1LWY4YzUtNDcxNi1hYWEwLTcwOGRlNGU1NTgwYiIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjE5MTA2OTI0LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9rcXVKYVJwSlUiLCJjb2duaXRvOnVzZXJuYW1lIjoiZm9vIiwiZXhwIjoxNjE5MTEwNTI0LCJpYXQiOjE2MTkxMDY5MjQsImVtYWlsIjoiZ3V0dWNyaXN0aWFuMjdAZ21haWwuY29tIn0.CcmQhWApg-k9_SCoS8tJg0eqdTNMN0dyFqzprJWqZYmpyLIYVJIW0Jwas9Z8yOxLcqoW2Mi-ZDHvzNl5xVUZyE37pEHlzWHb3em0lvwbSSAjL4Y57Q_Ddx1PbHwj0gRBSDMVYd-bCYibfBwa8ftnlSr70qtzo7BRnKz6Whu0_IrISaQC-nbP6eS8jntf0yCEwuZr6FFpRvgM_pKTdXis5vVAfSDh1mJv6kMcazJnI8VRjvYUKryGzxBCsnzftkUYdXVMAGKMWW-yrBTmpM35XhIzS7FW8UrC-n7GN-_sL1t5l3pLozT3RMd0FeFGmnDfrePY6U-2nOtJtCdV6q7Z5Q","RefreshToken":"eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.XrZBVdscMkcdYVDs2vwJBpQBexs47OFOM0drD36y4OJK4uPcbEjzY0Mrw7hHjc5uW1sR_E0bIMx62hur6B6dmNCeGcrOMK0JPCx2Vkrj1ghZd0p_DZuGB8NwGr0yoDjIXU-pQGkj1h2errJtjSf-rWe6gI_EK5puyZvuFWI432AFmxpd334lBEJEDanqyfeUsnLzanA4dkruWGko1x9inIDrhPGY64MZmY7Kg6VNIrOPMunBMZeVOMQi4cTD6g0GEwIJntVR9GR2ptMByK8TYQuoofmNEEXoOOfMd9AarYoHj0ZR2HNKACu3bvd93d1uKy5aYts6sJFRjjUcaug_Cw.HYAvBHP9T7Lg6qih._93W4z7GOa2Ging6B8YJhYVfObKos5joig0p15gWv0Wc3l3TWI-ZoPYEnhZDKGRCATsZzfsPRKpND5jYWBl4ecfCOEeqonb4ORSXD3dfvD_M0SkFyMrrrOlcPu_O9_IFOH0gAGXIFJnAi3mAvH5L7bGKxzSbV2wem31V3n9Vo8x9gR3ydiE2r8tHMQFol3WfkYTMt74QfJcrrysQjuX7jkGJo4tibAf5Xm4e3ozIzp4fgs1LjXjCLo5WIeL8xPB9x5cqrW6PbVbfCCw2jEJ4lSrm104S4uq3s2QUe59raTlCcwDumQHw1eivW37LXCrdxMYhyeJbfugeKVAy7Is3oa7MAq-nj3XDpEOt5mWpEmBE2BH_BCySsvEMHzODAwMtwkFuAYjGqmQlbd4tRYn83IH5J6sjeBotkjOfC55DhDBeiEzSOGSKjtvVC_V1MBxZ0XxBphlzZESoHvzTock1BUkAVQHK9eC5Y8-CJSqDC6HBg5oU06C5xyjnfSLlE8G62-5WKJrqN9ZqDpZW0V6z-WQJqAMVuwbYuqMcR7qQ-hSQ5oU9oIzpW2vYsd4qFelFVV4OZHdwkBv_5r6tr7rhRFAjbRJnrDsmEbXR_ocTMzeNdgD8yc0ez8Nr55zKW8ffvg08-zq6vuHI9e0Kyv7xioafeF25Msc0gEhaBgIhCWARzHExatRnw5DBDrogXr2SB69qkb5uxOjK0RkQvgW-4APcTGtuE7lxg2WvxpmuWWMTOMVBMvPZD79l0JylSIHsLqiGmk8gkuxVH0Iva9rFHAgUk7F4Mbah3OiK6Gs54lt1mAwDR6XURl5-oQGmGGNwSnqbtVbsvdxbpAnrH0gch_3dsZ2bELceu0DTUL54HHENgCllJsKGG6PUmdnKamboyl9jcdMxCun6HWDrV92cDG3o0qcFlMlkIJYThz3ljp5MeY7DmZ9NmvGyvBMDlnsJEHN5KQ-mnPA1h_sIZu_R2zSXcz4UKXAGYj3yR7shYn28ITKOl4F0U6W1spQxZPXegUNuQ869eIgc0OVWIXU3SK6Ewm15-snHviJlfypMwmhXr-ru94E4fYZ31JxvKTxrIi0aAnOYyluYiFlef1lOreTHuvCDqtKtbHyruMk_x6c88ty3HoDmpmYTIi7sb232lWyOJJGbISANxhGEu0HJd0Tkm2xmelJ6GSsoBzFMBi07wlkFSW9NPTiS0jSxD7HOGe_MP50aNHlXtTitl_ym9p71UqffRcjQhn7FaTvT0a9vRcQgHTUsZqRO6y6GnmlANf8.lV2ntKo_xZoEzEO9e1P_VQ","TokenType":"Bearer"},"ChallengeParameters":{}}
```

Use the JWT token in the `Authorization` header to make a `HTTP GET` request to `https://api.gutucristian.com/ad_request?country=us&lang=eng`.

### Making Call Using Postman:

![](https://sm-project.s3.amazonaws.com/CallingAPI.png)

**Note:** JWT token will expire after one day

# Solution Architecture
        
![](https://sm-project.s3.amazonaws.com/SolutionArchitecture.png)

# Setting Up AWS Architecture

Setting up the architecture is a long and manual process. If time permitted, I would build a CloudFormation template to do this automatically.

We will use the following AWS Services:
* Elastic Container Service
* Elastic Load Balancer (specifically an Application Load Balancer)
* API Gateway
* ElastiCache (for Redis cluster)
* S3
* Cognito
* AWS Parameter Store
* CloudWatch
* IAM
    
## Creating ElastiCache Redis Cluster

Before we create the Redis cluster, we must first create its security group:

![](https://sm-project.s3.amazonaws.com/RedisSG.png)

By default, the Redis server is configured to run on the port `6379`.

For security, I configured the Redis cluster to **only allow inbound traffic on TCP port `6379` from our HTTP ad server containers** running on ECS.

Now we can create the Redis cluser. 

To do so, we must specify:
* Cluster engine
* Location (Amazon Cloud or On-Premise)
* Cluster name (`http-ad-server-redis-cluster`)
* Engine version compatibility
* Port (`6379` for Redis)
* Node type (to lower costs, I selected `cache.t2.micro` which has `0.5GiB`)
* Number of replicas
* Multi-AZ
* Security Group (`http-ad-server-redis-cluster-sg` -- we will create it below)

![](https://sm-project.s3.amazonaws.com/CreatingRedisCluster.png)

Redis cluster being provisioned:

![](https://sm-project.s3.amazonaws.com/ProvisioningRedis.png)

Redis cluster:

![](https://sm-project.s3.amazonaws.com/RedisCluster.png)

**Note:** ElastiCache Multi-AZ provides enhanced high availability through automatic failover to a read replica, cross AZs, in case of a primary node failover. To reduce cost, I left this disabled. For SLA guarantees, this would be good to have in a production environment.

## Creating Elastic Container Service (ECS) Cluster

To run and manage the HTTP ad server instances, I decided to use Amazon ECS with AWS Fargate -- a serverless compute offering for containers. Fargate is a good option because it removes the need to provision and manage servers, lets us specify and pay for resources per application, and improves security through application isolation by design.

Provisioning a `dev` cluster in ECS:

![](https://sm-project.s3.amazonaws.com/ProvisioningECSCluster.png)

Because the HTTP ad server will run as a Docker container on ECS we need to provide an **ECS task definition** for it. A task definition describes the container(s) that form our application.

The following are the parameters we will specify in our task definition:
* The Docker image to use (e.g. `255286435885.dkr.ecr.us-east-1.amazonaws.com/http-ad-server`)
* How much CPU and memory to use with each task
* The launch type to use (which determines the infrastructure on which your tasks are hosted)
* The Docker networking mode to use
* The logging configuration to use
* Whether the task should continue to run if the container finishes or fails
* The command the container should run when it is started
* The IAM role that our tasks should use

However, before we can proceed with the task definition, we first need to create an Elastic Container Registry (ECR) repository that will contain our HTTP ad server Docker image.

ECR is a fully managed container registry that allows us to store, manage, share, and deploy container images and artifacts anywhere (the AWS equivalent of [Docker Hub](https://hub.docker.com/)).

![](https://sm-project.s3.amazonaws.com/ECRRepo.png)

To authenticate and push our `http-ad-server` Docker image to the repository we will need to execute these commands:

1. Retrieve authentication token and authenticate Docker client to our registry:

`aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 255286435885.dkr.ecr.us-east-1.amazonaws.com`

2. Build `http-ad-server` Docker image using:

`docker build -t http-ad-server .`

3. Tag the image so we can push to the ECR repository:

`docker tag http-ad-server:latest 255286435885.dkr.ecr.us-east-1.amazonaws.com/http-ad-server:latest`

4. Finally, push the image to our ECR repository:

`docker push 255286435885.dkr.ecr.us-east-1.amazonaws.com/http-ad-server:latest`

Now the ECR repository is created and it has our `http-ad-server` Docker image. We can go ahead and create the ECS task definition.

## Creating the ECS Task Definition

First we have to select a launch type configuration. Since we are using Fargate, select "Fargate".

![](https://sm-project.s3.amazonaws.com/TaskDefinitionCompatibilityType.png)

Next we configure the task and container definitions.

To do so, we must provide:
* A task definition name (`http-ad-server-task`)
* A task IAM role which tasks use to make API requests to authorized AWS services (`http-ad-server-task-role`)
* Network mode (`awsvpc`)
* A task execution role which is used by tasks to pull container images and publish container logs to Amazon CloudWatch (`ecsTaskExecutionRole`)
* Task size in terms of memory and CPU (to keep costs low, I chose `0.5GB` as the task memory and `0.25 vCPU` as the task CPU)
* The container definition

![](https://sm-project.s3.amazonaws.com/HTTPAdServerTaskDefinition.png)

The `http-ad-server-task-role` IAM role:

![](https://sm-project.s3.amazonaws.com/HTTPAdServerTaskRole.png)

Since the HTTP ad server makes calls to ElastiCache and S3 it has the following managed roles attached to its IAM role:
1. `AmazonElastiCacheFullAccess`, and
2. `AmazonS3FullAccess`

The last step in the task definition process is to configure the container definition.

For this we must provide:
* Container name (`http-ad-server-container`)
* Image (`255286435885.dkr.ecr.us-east-1.amazonaws.com/http-ad-server:latest`)
* Memory limit (hard limit of `512MiB` -- to keep costs low)
* Port mapping (our HTTP ad server container exposes port `80`)
* Environment variables (e.g. the Redis cluster primary endpoint URL)        

![](https://sm-project.s3.amazonaws.com/TaskDefinitionContainerConfig.png)

### Sidenote on ECS Task vs Service

A **task definition** is a collection of one or more container configurations.

A **service** is used to guarantee that you always have some number of tasks running at all times. If a task's container exits due to error, or the underlying EC2 instance fails and is replaced, the ECS service will replace the failed task. This is why we create **clusters** so that the service has plenty of resources in terms of CPU, Memory and Network ports to use. To us it doesn't really matter which instance tasks run on so long as they run. A service configuration references a task definition. A service is responsible for creating tasks.

**Services are typically used for long running applications like web servers.**

For example, our HTTP ad server will be deployed in the region `us-east-1` with at least three tasks running across three Availability Zones (AZs) to guarantee **high availability** and **fault tolerance**; if one task fails our entire service does not go down with it. In fact, we would still have another two tasks running and the failed one would be replaced (self-healing property).

## Setting Up The Application Load Balancer (ALB)

To distribute load across the various HTTP ad web servers running in different AZs I decided to use an ALB.

Before we can provision the ALB we must create a security group to go along with it.

However, before we can create a security group for our ALB, we will first need to create a security group for our VPC link. 

The reason we first need to provision the VPC link security group is because we want to define the ALB security group such that it **only accept traffic from the VPC link**.

**Why do we need a VPC link?**

We need a VPC link so that we can connect our ALB to API Gateway. API Gateway is the entity that will expose our application to the outside world. The reason we are interested in using API Gateway:
* Allows us to use API Keys
* Has built in DDOS protection using Web Application Firewall (WAF)
* Allows for SSL Termination -- ultimately reducing compute burden on downstream infrastructure and, thus, reducing latency
* Secure API by authenticating client JWT token at edge

So, lets go ahead and first create the VPC link security group (`http-ad-server-vpc-link-sg`). 

Configure the inbound rule to allow HTTP traffic from anywhere:

![](https://sm-project.s3.amazonaws.com/VPCLinkSG.png)

Now that we have our VPC link security group we can create the ALB security group:

![](https://sm-project.s3.amazonaws.com/CreatingALBSG.png)

**Note:** the reason we had to create a VPC link security group first was so that we could select it when defining the inbound traffic rule for the ALB. We are configuring the ALB inbound traffic to only be allowed to come from the VPC link (see the `http-ad-server-vpc-link` option in the dropdown "Security Groups" section in the image above)

Finally, we can go ahead and provision our ALB (`http-ad-server-alb`).

When creating the ALB select the **internal** radio box. The ALB **will not** get a public IP which is what we want: it should receive all traffic from API Gateway via the VPC link. 

Also, for high availability, we configure three AZs (`us-east-1a`, `us-east-1b`, and `us-east-1c`). The load balancer will route traffic to the **ECS targets** in these AZs only:

![](https://sm-project.s3.amazonaws.com/CreatingALB.png)

For the security group, select the `http-ad-server-alb-sg` that we created from before:

![](https://sm-project.s3.amazonaws.com/ALBSG.png)

Next we configure the ALB routing. For this, we create a new target group `http-ad-server-tg` (a target group tells the load balancer where to direct traffic to). The target group will eventually contain the IP addresses of the Fargate containers that traffic should be routed to:

![](https://sm-project.s3.amazonaws.com/ALBConfigureRouting.png)

Provisioning:

![](https://sm-project.s3.amazonaws.com/ProvisioningALB.png)

In summary, we created an **internal** ALB (no public IP) and configured it's security group rule such that it only allows inbound HTTP traffic from the VPC link (`http-ad-server-vpc-link-sg`). We also defined the ALB routing to send traffic to all instances part of the `http-ad-server-tg` target group.

## Creating the ECS HTTP Ad Server Service

Having the task definition defined and the ALB provisioned, we can go ahead and create the HTTP ad server ECS service (`http-ad-server-service`).

![](https://sm-project.s3.amazonaws.com/ConfiguringECSService.png)

Select the ALB we created earlier (`http-ad-server-alb`) to front our ECS Service (i.e. distribute inbound traffic across the tasks running in our service):

![](https://sm-project.s3.amazonaws.com/ConfiguringECSALB.png)

We also have to configure the container to load balance. In this case, we do this by selecting the target group name `http-ad-server-tg` which we created from before. All of the tasks created under the service `http-ad-server-service` will automatically be registered (by AWS) under the specified target group (`http-ad-server-tg`):

![](https://sm-project.s3.amazonaws.com/SettingContainerToLoadBalance.png)

Select the subnets in which the ECS service can spawn the tasks:

![](https://sm-project.s3.amazonaws.com/ECSSubnets.png)

**Important:** we need to select the same subnets that the `http-ad-server-alb` was configured to load balance to. In this case, we correctly chose subnets in the AZs we expect our containers to run in (`us-east-1a`, `us-east-1b`, and `us-east-1c`) and the ones the ALB can forward to

Next we configure a security group for our ECS service. Since our containers should only receive traffic from the `http-ad-server-alb`, we configure the ALB security group (with id `sg-00a6051b552cd8c3b`) as the inbound source group:

![](https://sm-project.s3.amazonaws.com/ALBSG.png)

![](https://sm-project.s3.amazonaws.com/CreatingECSServiceSG.png)

To leverage scale in / out capabilities for our ECS service based on real-time performance metrics we must enable Service Auto Scaling. 

Service Auto Scaling cares about three parameters:
* Minimum number of tasks (the lower boundary to which Service Auto Scaling can adjust your service’s desired count)
* Desired number of tasks (the initial desired count to start with before Service Auto Scaling begins adjustment)
* Maximum number of tasks (the upper boundary to which Service Auto Scaling can adjust your service’s desired count)

![](https://sm-project.s3.amazonaws.com/ECSServiceSetAutoScaling.png)

The scaling action will be defined by the scaling policy type. There are two types of scaling policy types: 
1. **Target Auto Scaling**, and 
2. **Step scaling**

Our `http-ad-server-ecs-service` will be configured to use **Target Tracking Scaling**. 

With target tracking scaling policies, you select a scaling metric and set a target value. The Service Auto Scaling will create and manage the CloudWatch alarms that trigger the scaling policy. Behind the scenes it will calculate and determine when to scale in or out based on the CloudWatch metric and the target value we set.

![](https://sm-project.s3.amazonaws.com/ECSServiceTargetScaling.png)

Our ECS service being provisioned:

![](https://sm-project.s3.amazonaws.com/HTTPAdServerECSService.png)

## Creating the VPC Link

We need to create a VPC Link to be able to link API Gateway to the internal ALB.

In API Gateway, create a VPC link. Give it a name (`http-ad-server-vpc-link`), select subnets (the same three subnets our ALB forwards to), and a security group (choose `http-ad-server-vpc-link-sg` which we created earlier):

![](https://sm-project.s3.amazonaws.com/CreateVPCLink.png)

Create an API Gateway HTTP API (`http-ad-server`):

![](https://sm-project.s3.amazonaws.com/CreateAPIGatewayHTTPAPI.png)

Create the `ad_request` route in the `http-ad-server` API and configure to only allow `HTTP GET` requests:

![](https://sm-project.s3.amazonaws.com/CreateAPIRoute.png)

For the `ad_request` route, create an integration by choosing the VPC link we created and making it point to the private ALB listener to send the requests to:

![](https://sm-project.s3.amazonaws.com/ConfigureRouteIntegration.png)

Finally we can test our HTTP ad server. Send a `HTTP GET` to `https://3ubjt2luxi.execute-api.us-east-1.amazonaws.com/ad_request?country=us&lang=eng`. Response should be:

![](https://sm-project.s3.amazonaws.com/TestingAPIWithDefaultAPIGatewayDomain.png)

Now, lets use Route53 and AWS Certificate Manager to configure a _custom domain_ for our API (`https://3ubjt2luxi.execute-api.us-east-1.amazonaws.com` is a bit ugly).

First we will need to go to AWS Certificate Manager and provision a certificate for the domain we would like to use. Since I own the root domain `gutucristian.com` I can also provision a certificate for the subdomain `api.gutucristian.com`:

![](https://sm-project.s3.amazonaws.com/AWSCertificateManager.png)

Having this, go to the API Gateway "Custom domain names" section to create the custom domain. We will need to provide:
* Our custom domain name
* Minimum TLS version (TLS 1.2 recommeded)
* API Gateway endpoint type (e.g. `Region` in our case)
* The ACM certificate provisioned from before

![](https://sm-project.s3.amazonaws.com/APIGatewayCustomDomainName.png)

After this is created, go into the "API Mappings" section for the custom API Gateway domain and add a new mapping to the `$default` stage of our API:

![](https://sm-project.s3.amazonaws.com/ConfigureAPIMappings.png)

Finally we link the custom domain to our API Gateway in Route53 via a `Type A` record with an `Alias` to our API:

![](https://sm-project.s3.amazonaws.com/Route53AliasToAPIGatewayHTTPAPI.png)

Now we can visit our API over HTTPS using: `https://api.gutucristian.com/ad_request?country=ca&lang=eng`:

![](https://sm-project.s3.amazonaws.com/TestingAPIWithCustomDomain.png)

## Securing API using Cognito

1. First create a Cognito User Pool

2. Next create an app client

3. Create a Cognito User (this represents one instance of a HTTP ad server end user)

4. The user will need to reset their default password. You can do this via `aws cli` using:

```
aws cognito-idp admin-set-user-password
  --user-pool-id <your-user-pool-id> \
  --username <username> \
  --password <password> \
  --permanent
```

A user will need to have the following information to submit an auth request to Cognito (our authentication service) and get a JWT token (see `Usage` section):

* Username
* Password
* UserPoolId
* ClientId

# Improvements

* CI/CD workflow
    * GitHub webhook on merge or push to master
    * Run tests
    * Automatically build new Docker image and push to ECR
    * Create updated ECS task and update service (rolling restart or blue green deploy)
* Infrastructure as code: build CloudFormation template to automate infrastructure creation process
* Implement unit tests
