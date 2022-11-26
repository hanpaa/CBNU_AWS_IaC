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
        :param ec2Resource: boto3 Amazon EC2 resource. 저수준 EC2 서비스의 action을 감싸기 위한
        고수준 boto3 리소스.
        :param instance: boto3 Instance object . instance 정보들을 감싸기 위한
        고수준 object
        """
        self.ec2Resource = boto3.resource('ec2')


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

        if self.instance is None:
            print("There is no Instance to terminate.")
            return

        try:
            instanceID = self.instance.id
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.terminate
            self.instance.terminate()
            self.isntance.wait_until_terminate()
            self.instance = None
        except ClientError as err:
            logging.error(
                "Couldn't terminate instance %s. Here's why: %s: %s", instanceID,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def instanceLoad(self, instanceInfo):
        self.InstanceId = instanceInfo['InstanceId']
        self.ImageId = instanceInfo['ImageId']
        self.InstanceType = instanceInfo['InstanceType']
        self.PublicIpAddress = instanceInfo['PublicIpAddress']
        self.Architecture = instanceInfo['Architecture']
        self.State = instanceInfo['State']['Name']
