# Locuster

> Example how with [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html) you can deploy a
> load test infrastructure using [Locust.io](https://locust.io/)

> The infrastructure code is written in [Python](https://www.python.org/), it executes a master\slave Locust infrastructure

> I totally love LOCUST and CDK!

### Installation and requirements:

Install the CDK framework

```bash
npm install -g aws-cdk
```

Install the Python dependencies

```bash
pip install -r requirements.txt
```

Authenticate in your AWS account:

> Follow this guide: [Configuring the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

Bootstrap AWS CDK (if needed)

```bash
cdk bootstrap --region eu-west-1
```

## Usage

Deploy locust:

```bash
export AWS_PROFILE="profilename"
export AWS_DEFAULT_REGION="eu-west-1"
cdk deploy locuster

.....

 ✅  locuster

Outputs:
locuster.LocustWebConsole = http://locus-nbala-15IY958M7LUVF-ab8bf6ee96743c80.elb.eu-west-1.amazonaws.com:8089
```

> After the deployment you need to wait for a 1-minute maximum, you can start the load using the output address


Destroy locust:

```bash
cdk destroy locuster
```

Local test:

> You can try locally the platform:

```bash
cd docker
docker-compose up --scale worker=2 --build
```

Customize the loucustfile test code:

> You can customize the code inside the docker/code directory

Have fun!
