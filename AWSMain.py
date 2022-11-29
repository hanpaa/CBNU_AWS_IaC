"""
@author 최제현
@date 2022/11/20
AWS 과제 인스턴스 제어 main 클래스
"""
import boto3

from EC2Instance import EC2Instance

class AWSMain:

    def __init__(self):
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
            print("  9. terminate(delete) instance                                     ")
            print("                                 99. quit                   ")
            print("------------------------------------------------------------")

            print("Enter an integer: ")
            inputNumber = input()

            if inputNumber == "1":
                self.describeInstances()
            elif inputNumber == "3":
                self.startInstanceMenu()
            elif inputNumber == "5":
                self.stopInstanceMenu()
            elif inputNumber == "9":
                self.terminateInstanceMenu()
            elif inputNumber == "6":
                self.ec2Instance.createInstance()
                self.loadInstanceList()
            elif inputNumber == "99":
                exit(0)

    def describeInstances(self):

        self.loadInstanceList()
        for index, instance in enumerate(self.instanceList):
            print("----------------------")
            print("instance index: " + str(index))
            instance.displayInstance()
            print("----------------------")

    def loadInstanceList(self):
        self.instanceList.clear()
        response = self.ec2Instance.getALLInstanceDescribe()
        for instance in response['Reservations']:
            newEC2Instance = EC2Instance()
            newEC2Instance.instanceLoad(instance['Instances'][0])
            self.instanceList.append(newEC2Instance)

    def stopInstanceMenu(self):
        """

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.stop_instances

        :return:
        """
        self.describeInstances()
        print("stop instance")
        print("input instance index : ")
        try:
            selctedIndex = int(input())
        except ValueError:
            print("Please enter a number, not a string.")
            return
        if selctedIndex+1 <= len(self.instanceList):
            self.instanceList[selctedIndex].stopInstance()
        else:
            print("index error..")
            return


    def startInstanceMenu(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.start_instances
        """
        self.describeInstances()
        print("start instance")
        print("input instance index : ")
        try:
            selctedIndex = int(input())
        except ValueError:
            print("Please enter a number, not a string.")
            return
        if selctedIndex+1 <= len(self.instanceList):
            self.instanceList[selctedIndex].startInstance()

        else:
            print("index error..")
            return

    def terminateInstanceMenu(self):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.start_instances
        """
        self.describeInstances()
        print("terminate instance")
        print("input instance index : ")
        try:
            selctedIndex = int(input())
            print("are you sure? press anykey/N")
            answer = input()
            if(answer.lower() == 'n'):
                return
        except ValueError:
            print("Please enter a number, not a string.")
            return
        if selctedIndex+1 <= len(self.instanceList):
            self.instanceList[selctedIndex].terminateInstance()

        else:
            print("index error..")
            return

if __name__ == '__main__':
    # Retrieve the list of existing buckets
    AWSMain()
