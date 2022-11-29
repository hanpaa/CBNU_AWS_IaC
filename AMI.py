"""
Amazon Machine Image(AMI) 에 대응하는 boto3 Image object
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#image
"""
import boto3

class AMI:

    def __init__(self):

        self.ec2Resource = boto3.resource('ec2')
        self.client = boto3.client('ec2')
        self.imageId = None
        self.image = None

    def getALLAMIDescribe(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images
        :return: JSON response
        """

        return self.client.describe_images(
            Owners=[
                # owner ID
                '762615318476'
            ]
        )

    def displayAMI(self, indent=1):
        """
        Displays information about an AMI.
        :param indent: The visual indent to apply to the output.
        :return:
        """
        ind = '\t'*indent
        print("stub")
        print(f"{ind}ID: {self.image.image_id}")
        print(f"{ind}Name: {self.image.name}")
        print(f"{ind}Description: {self.image.description}")
        print(f"{ind}Architecture: {self.image.architecture}")
        print(f"{ind}Hypervisor: {self.image.hypervisor}")
        print(f"{ind}State: {self.image.state}")
        print(f"{ind}Platform: {self.image.platform_details}")

    def imageLoad(self, amiJson):
        self.imageId = amiJson['ImageId']
        self.image = self.ec2Resource.Image(self.imageId)

