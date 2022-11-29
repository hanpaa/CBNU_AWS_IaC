"""
@author 최제현
@date 2022/11/20
AWS 과제 인스턴스 제어 main 클래스
"""
import boto3

from EC2Instance import EC2Instance
from AMI import AMI
class AWSMain:

    def __init__(self):
        self.ec2Instance = EC2Instance()
        self.ami = AMI()
        self.instanceList = []
        self.imageList = []
        self.keyPairList = []
        self.mainMenu()

    def mainMenu(self):
        state = True
        self.showMenu()

        print("Select Menu Enter an integer: ")
        inputNumber = input()

        while(state):

            if inputNumber == "1":
                self.describeInstances()
            elif inputNumber == "2":
                self.describeAvailableZones()
            elif inputNumber == "3":
                self.startInstanceMenu()
            elif inputNumber == "4":
                self.describeAvailableRegions()
            elif inputNumber == "5":
                self.stopInstanceMenu()
            elif inputNumber == "6":
                self.ec2Instance.createInstance()
                self.loadInstanceList()
            elif inputNumber == "7":
                self.rebootInstanceMenu()
            elif inputNumber == "8":
                self.describeImages()
            elif inputNumber == "9":
                self.terminateInstanceMenu()
            elif inputNumber == "98":
                inputNumber = self.showMenu()
            elif inputNumber == "99":
                exit(0)

            print("Select Menu Enter an integer: ")
            inputNumber = input()

    def showMenu(self):
        print("                                                            ")
        print("                                                            ")
        print("------------------------------------------------------------")
        print("           Amazon AWS Control Panel using SDK               ")
        print("------------------------------------------------------------")
        print("  1. list instance                2. available zones        ")
        print("  3. start instance               4. available regions      ")
        print("  5. stop instance                6. create instance        ")
        print("  7. reboot instance              8. list images            ")
        print("  9. terminate(delete) instance  10. Show Menu              ")
        print("  98. Show Menu                  99. quit                   ")
        print("------------------------------------------------------------")

    def describeInstances(self):

        self.loadInstanceList()
        for index, instance in enumerate(self.instanceList):
            print("------------------------------------------------------------")
            print("instance index: " + str(index))
            instance.displayInstance()
            print("------------------------------------------------------------")

    def loadInstanceList(self):
        self.instanceList.clear()
        try:
            response = self.ec2Instance.getALLInstanceDescribe()
        except:
            return
        for instance in response['Reservations']:
            newEC2Instance = EC2Instance()
            newEC2Instance.instanceLoad(instance['Instances'][0])
            self.instanceList.append(newEC2Instance)


    def describeImages(self):

        self.loadImageList()
        for index, image in enumerate(self.imageList):
            print("------------------------------------------------------------")
            print("image index: " + str(index))
            image.displayAMI()
            print("------------------------------------------------------------")
    def describeAvailableZones(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_availability_zones
        :return:
        """
        print("------------------------------------------------------------")
        print("Available Zone")
        client = boto3.client('ec2')
        response = client.describe_availability_zones()
        for zone in response['AvailabilityZones']:
            print("Zone name : " + zone.get('ZoneName'))

        print("------------------------------------------------------------")

    def describeAvailableRegions(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_regions
        :return:
        """
        print("------------------------------------------------------------")
        print("Available Region")
        client = boto3.client('ec2')
        response = client.describe_regions()
        for zone in response['Regions']:
            print("Region name : " + zone.get('RegionName'))

        print("------------------------------------------------------------")

    def loadImageList(self):
        self.imageList.clear()
        try:
            response = self.ami.getALLAMIDescribe()
            for image in response['Images']:
                newAMI = AMI()
                newAMI.imageLoad(image)
                self.imageList.append(newAMI)
        except:
            return

    def stopInstanceMenu(self):
        """

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.stop_instances

        :return:
        """
        print("stop instance insert q if you want escape")
        selectedIndex = self.getInstanceByIndex()
        if selectedIndex is not None:
            self.instanceList[selectedIndex].stopInstance()
        else:
            return

    def startInstanceMenu(self):
        print("start instance insert q if you want escape")
        selectedIndex = self.getInstanceByIndex()
        if selectedIndex is not None:
            self.instanceList[selectedIndex].startInstance()
        else:
            return

    def terminateInstanceMenu(self):
        print("terminate instance insert q if you want escape")
        selectedIndex = self.getInstanceByIndex()
        if selectedIndex is not None:
            self.instanceList[selectedIndex].terminateInstance()
        else:
            return

    def rebootInstanceMenu(self):
        print("reboot instance insert q if you want escape")
        selectedIndex = self.getInstanceByIndex()
        if selectedIndex is not None:
            self.instanceList[selectedIndex].rebootInstance()
        else:
            return
    def getInstanceByIndex(self):
        self.describeInstances()
        print("input instance index : ")
        try:
            selctedIndex = input()

            if(selctedIndex == "q"):
                return None
            else:
                selctedIndex = int(selctedIndex)
                if selctedIndex+1 <= len(self.instanceList):
                    return selctedIndex
                else:
                    print("index error..")
                    return None

        except ValueError:
            print("Please enter a number, not a string.")
            return None

if __name__ == '__main__':
    # Retrieve the list of existing buckets
    AWSMain()
