"""
@author 최제현
@date 2022/11/20
EC2 인스턴스 클래스
"""
import boto3
import logging
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class EC2Instance:
    def __init__(self):
        """

        """
        self.ec2Resource = boto3.resource('ec2')
        self.client = boto3.client('ec2')
        self.InstanceId = None
        self.ImageId = None
        self.InstanceType = None
        self.PublicIpAddress = None
        self.Architecture = None
        self.State = None


    def getALLInstanceDescribe(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
        :return: response
        """

        return self.client.describe_instances()

    def displayInstance(self, indent=1):
        """
        Displays information about an instance.

        :param indent: The visual indent to apply to the output.
        """
        try:
            ind = '\t'*indent
            print(f"{ind}ID: {self.InstanceId}")
            print(f"{ind}Image ID: {self.ImageId}")
            print(f"{ind}Instance type: {self.InstanceType}")
            print(f"{ind}Public IP: {self.PublicIpAddress}")
            print(f"{ind}Architecture: {self.Architecture}")
            print(f"{ind}State: {self.State}")
        except ClientError as err:
            logger.error(
                "Couldn't display your instance. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def createInstance(self,  imageID = "ami-07cc74f198bb9e86a", instanceType = 't2.micro',securityGroup = None):
        """
        새 ec2인스턴스를 생성함.
        :param image: Amazon Machine Image(AMI) 에 대응하는 boto3 Image object
                      instance의 스토리지 정보와 OS종류등의 정보를 가지고있음.
        or
        :param imageID: Amazon Machine Image(AMI) 에 대응하는 boto3 Image object
                      instance의 스토리지 정보와 OS종류등의 정보를 가지고있음.
        :param instanceType: 인스턴스의 타입. 예) 't2.micro' vCPU와 memory 용량 등이 다름.

        :param securityGroup:  boto3 SecurityGroup Object. instance의 권한그룹과 관련된 object list
                               default는 VPC사용
        :return 새로 생성된 boto3 Instance object
        """
    # :param keyPair: boto3 KeyPair. 인스턴스와 secure connection을 하기  위한 keypair
        try:
            # ami-07cc74f198bb9e86a : red hat free tier, t2.micro free tier
            instanceParams = {
                'ImageId': imageID, 'InstanceType': instanceType
            }
            if securityGroup is not None:
                instanceParams['SecurityGroupIds'] = [group.id for group in securityGroup]
            # 옵션과 함께 인스턴스 생성
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances
            print("create instance")
            self.instance = self.ec2Resource.create_instances(**instanceParams, MinCount=1, MaxCount=1)[0]
            # 인스턴스 생성까지 대기
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.wait_until_running
            print("wait unitll running..")
            self.instance.wait_until_running()
            print("finish.")
        except ClientError as err:
            logging.error(
                "Couldn't create instance with image %s, instance type %s,"
                "Here's why: %s: %s", imageID, instanceType,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return self.instance

    def terminateInstance(self):

        if self.InstanceId is None:
            print("There is no Instance to terminate.")
            return

        if self.State == "terminated":
            print("the instance is already terminated")
        else:
            response = self.client.terminate_instances(
                InstanceIds=[
                    self.InstanceId
                ]
            )

            print("the instance state is now " + response.get('TerminatingInstances')[0].get('CurrentState').get('Name'))


    def stopInstance(self):

        if self.InstanceId is None:
            print("There is no Instance to stop.")
            return

        if self.State == "stopped":
            print("the instance is already stopped")
        elif self.State == "stopping":
            print("the instance is already stopping")
        else:
            response = self.client.stop_instances(
                InstanceIds=[
                    self.InstanceId
                ]
            )

            print("the instance state is now " + response.get('StoppingInstances')[0].get('CurrentState').get('Name'))


    def startInstance(self):

        if self.InstanceId is None:
            print("There is no Instance to starting.")
            return

        if self.State == "running":
            print("the instance is already running")
        elif self.State == "pending":
            print("the instance is already pending")
        else:
            response = self.client.start_instances(
                InstanceIds=[
                    self.InstanceId
                ]
            )
            print("the instance state is now " + response.get('StartingInstances')[0].get('CurrentState').get('Name'))


    def instanceLoad(self, instanceInfo):
        self.InstanceId = instanceInfo.get('InstanceId')
        self.ImageId = instanceInfo.get('ImageId')
        self.InstanceType = instanceInfo.get('InstanceType')
        self.PublicIpAddress = instanceInfo.get('PublicIpAddress')
        self.Architecture = instanceInfo.get('Architecture')
        self.State = instanceInfo.get('State').get('Name')
