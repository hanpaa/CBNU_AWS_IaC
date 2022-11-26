import boto3

from EC2Instance import EC2Instance

class AWSMain:

    def __init__(self):
        self.client = boto3.client('ec2')
        self.ec2Instance = EC2Instance()
        self.instanceList = []
        self.mainMenu()


        
    def mainMenu(self):
        state = True
        while(state):
            print("                                                            ")
            print("                                                            ")
            print("------------------------------------------------------------")
            print("           Amazon AWS Control Panel using SDK               ")
            print("------------------------------------------------------------")
            print("  1. list instance                2. available zones        ")
            print("  3. start instance               4. available regions      ")
            print("  5. stop instance                6. create instance        ")
            print("  7. reboot instance              8. list images            ")
            print("                                 99. quit                   ")
            print("------------------------------------------------------------")

            print("Enter an integer: ")
            inputNumber = input()

            if inputNumber == "1":
                self.describeInstances()

            if inputNumber == "6":
                self.ec2Instance.createInstance()
                self.loadInstanceList()

    def describeInstances(self):
        self.loadInstanceList()
        for index, instance in enumerate(self.instanceList):
            print("----------------------")
            print("instance " + str(index))
            instance.displayInstance()
            print("----------------------")

    def loadInstanceList(self):
        self.instanceList.clear()
        response = self.client.describe_instances()
        for instance in response['Reservations']:
            ec2Instance = EC2Instance()
            ec2Instance.instanceLoad(instance['Instances'][0])
            self.instanceList.append(ec2Instance)


if __name__ == '__main__':
    # Retrieve the list of existing buckets
    AWSMain()
