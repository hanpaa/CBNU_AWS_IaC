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
        self.instance = None




    def getALLInstanceDescribe(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
        :return: JSON response
        """
        try:
            return self.client.describe_instances()
        except ClientError as err:
            logger.error(
                "Couldn't display your instance. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise



    def displayInstance(self, indent=1):
        """
        Displays information about an instance.

        :param indent: The visual indent to apply to the output.
        """
        ind = '\t'*indent
        print(f"{ind}ID: {self.instance.instance_id}")
        print(f"{ind}Image ID: {self.instance.image_id}")
        print(f"{ind}Image name: {self.instance.image.name}")
        if self.instance.tags is not None:
            for tag in self.instance.tags:
                if(tag.get('Key') == 'Name'):
                    print(f"{ind}instance Name: {tag.get('Value')}")
        else:
            print(f"{ind}instance Name: None")
        print(f"{ind}Key Name: {self.instance.key_name}")
        print(f"{ind}Instance type: {self.instance.instance_type}")
        print(f"{ind}Public IP: {self.instance.public_ip_address}")
        print(f"{ind}Architecture: {self.instance.architecture}")
        print(f"{ind}State: {self.instance.state.get('Name')}")


    def createInstance(self,  imageID = "ami-0b8cb09bfa67f921f", keyName = "ec2keypair"\
                       , instanceType = 't2.micro',securityGroup = None):
        """
        새 ec2인스턴스를 생성함.
        :param imageID: Amazon Machine Image(AMI) 에 대응하는 boto3 Image object의 id
                      default : ami-0b8cb09bfa67f921f condor slave image
        :param instanceType: 인스턴스의 타입. 예) 't2.micro' vCPU와 memory 용량 등이 다름.

        :param keyName: ec2에 접근하기 위한 keypair의 이름
                    default : ec2keypair (installed in laptop)

        :param securityGroup:  boto3 SecurityGroup Object. instance의 권한그룹과 관련된 object list
                               default는 VPC사용
        :return 새로 생성된 boto3 Instance object
        """
    #
        try:
            # ami-07cc74f198bb9e86a : red hat free tier, t2.micro free tier
            instanceParams = {
                'ImageId': imageID, 'InstanceType': instanceType, 'KeyName': keyName
            }
            #
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
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.terminate

        """
        if self.instance is None:
            print("There is no Instance to terminate.")
            return

        if self.instance.state == "terminated":
            print("the instance is already terminated")
        else:
            print("terminating..")
            response = self.instance.terminate()

            print("the instance state is now " + response.get('TerminatingInstances')[0].get('CurrentState').get('Name'))



    def stopInstance(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.stop
        """

        if self.instance is None:
            print("There is no Instance to stop.")
            return

        if self.State == "stopped":
            print("the instance is already stopped")
        elif self.State == "stopping":
            print("the instance is already stopping")
        elif self.State == "terminated":
            print("the instance is already terminated")
        else:
            print("stopping..")
            response = self.instance.stop()
            print("the instance state is now " + response.get('StoppingInstances')[0].get('CurrentState').get('Name'))

    def startInstance(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.start
        """
        if self.instance is None:
            print("There is no Instance to starting.")
            return

        if self.State == "running":
            print("the instance is already running")
        elif self.State == "pending":
            print("the instance is already pending")
        elif self.State == "terminated":
            print("the instance is already terminated")
        else:
            print("starting..")
            response = self.instance.start()
            print("the instance state is now " + response.get('StartingInstances')[0].get('CurrentState').get('Name'))
    def rebootInstance(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.reboot
        """
        if self.instance is None:
            print("There is no Instance to starting.")
            return

        if self.State == "terminated":
            print("the instance is already terminated")
        else:
            print("reboot..")
            # reboot returns None
            self.instance.reboot()


    def instanceLoad(self, instanceInfo):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.load
        :param instanceInfo: boto3 client로 부터 받아온 instance들의 현재 정보

        정보에서 instance의 id를 받아와 instance 변수에 boto3 Instance 객체를 붙인다.

        """
        self.InstanceId = instanceInfo.get('InstanceId')
        # boto3 instance 객체를 불러옴. 해당 객체로 instance 제어 가능.
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#instance
        self.instance = self.ec2Resource.Instance(self.InstanceId)

        self.State = self.instance.state.get('Name')

