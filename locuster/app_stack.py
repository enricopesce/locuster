from aws_cdk import (
    core,
    aws_ecs as ecs,
    aws_ecr_assets as ecr_assets,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2
)

class AppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.IVpc, *, slaves=2, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster = ecs.Cluster(self, "cluster", vpc=vpc)

        locust_asset = ecr_assets.DockerImageAsset(self, 'locust', directory="docker", file="app/Dockerfile")

        master_task = ecs.FargateTaskDefinition(
            self,
            "mastert",
            cpu=512,
            memory_limit_mib=1024
        )

        sg_slave = ec2.SecurityGroup(self, "sgslave", vpc=vpc, allow_all_outbound=True)

        sg_master = ec2.SecurityGroup(self, "sgmaster", vpc=vpc, allow_all_outbound=True)
        sg_master.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(8089))
        sg_master.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(5557))

        master_container = master_task.add_container(
            "masterc",
            image=ecs.ContainerImage.from_docker_image_asset(locust_asset),
            logging=ecs.LogDriver.aws_logs(stream_prefix="master"),
            command=["-f", "/mnt/locust/locustfile.py",  "--master"]
        )

        master_container.add_port_mappings(ecs.PortMapping(container_port=8089, host_port=8089))
        master_container.add_port_mappings(ecs.PortMapping(container_port=5557, host_port=5557))

        master_service = ecs.FargateService(
            self, "masters",
            cluster=cluster,
            task_definition=master_task,
            desired_count=1,
            assign_public_ip=True,
            security_group=sg_master
        )

        nlb = elbv2.NetworkLoadBalancer(
            self,
            "nbalancer",
            internet_facing=True,
            vpc=vpc
        )

        listener_master_console = nlb.add_listener(
            "masterconsole",
            port=8089,
            protocol=elbv2.Protocol("TCP")
        )

        listener_console = nlb.add_listener(
            "master",
            port=5557,
            protocol=elbv2.Protocol("TCP")
        )

        listener_master_console.add_targets(
            "consoletarget",
            deregistration_delay=core.Duration.seconds(1),
            port=8089,
            targets=[master_service.load_balancer_target(
                container_name="masterc",
                container_port=8089
            )],
            health_check=elbv2.HealthCheck(
                healthy_threshold_count=2,
                unhealthy_threshold_count=2,
                timeout=core.Duration.seconds(10)
            )
        )

        listener_console.add_targets(
            "mastertarget",
            deregistration_delay=core.Duration.seconds(1),
            port=5557,
            targets=[master_service.load_balancer_target(
                container_name="masterc",
                container_port=5557
            )],
            health_check=elbv2.HealthCheck(
                healthy_threshold_count=2,
                unhealthy_threshold_count=2,
                timeout=core.Duration.seconds(10)
            )
        )

        slave_task = ecs.FargateTaskDefinition(
            self,
            "slavet",
            cpu=2048,
            memory_limit_mib=4096
        )

        slave_task.add_container(
            "slavec",
            image=ecs.ContainerImage.from_docker_image_asset(locust_asset),
            logging=ecs.LogDriver.aws_logs(stream_prefix="slave"),
            command=["-f", "/mnt/locust/locustfile.py", "--worker", "--master-host", nlb.load_balancer_dns_name]
        )

        ecs.FargateService(
            self, "slaves",
            cluster=cluster,
            task_definition=slave_task,
            desired_count=slaves,
            assign_public_ip=True,
            security_group=sg_slave
        )

        core.CfnOutput(self, "LocustWebConsole", value="http://" + nlb.load_balancer_dns_name + ":8089")
