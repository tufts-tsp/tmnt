from uuid import uuid4, UUID
import time
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt



class Engine(object):
    def __init__(
        self,
        name: str,
        desc: str = "N/A",
    ):
        self.__id = uuid4()
        if not isinstance(name, str):
            raise ValueError("Engine Name must be a string")
        self.__name = name
        if desc == None:
            desc = "N/A"
        if not isinstance(desc, str):
            raise ValueError("Engine Description must be a string")
        self.__desc = desc

    @property
    def eid(self) -> UUID:
        """Unique ID for the Element"""
        return self.__id

    @property
    def name(self) -> str:
        """Name of the Element"""
        return self.__name

    @name.setter
    def name(self, val: str) -> None:
        self.__name = val

    @property
    def desc(self) -> str:
        """Description of the Element"""
        return self.__desc

    @desc.setter
    def desc(self, val: str) -> None:
        self.__desc = val


class NaturalEngine(Engine):

    """
    NaturalEngine is the system that tracks
    """

    def __init__(
        self,
        name: str,
        currentFocus: str = "None",
        desc: str = "N/A",
    ):
        self.currentFocus = currentFocus
        self.previous_events = []
        self.lastevent = time.time()
        super().__init__(name, desc)

        

    def event(self, event_type: str):
        # Get the event and check what type it is, then plug into markov model to predict new focus.  Update list of previous events to include this.

        transitionmatrix = self.MLModel()

        if event_type == "Asset1":
            value = 0
        elif event_type == "Server":
            value = 1
        elif event_type == "Data Store":
            value = 2
        elif event_type == "Lambda":
            value = 3
        elif event_type == "Process":
            value = 4
        elif event_type == "External Entity":
            value = 5

        largest = transitionmatrix[value][0]; largeindex = 0; largeloc = 0; num_of_times = []

        for i in transitionmatrix[value]:
            if i > largest:
                largest = i
                largeloc = largeindex
            largeindex += 1
        
        for i in range(6):
            if transitionmatrix[value][i] == largest:
                num_of_times.append(i)
            
        suggest_assets = []

        for i in num_of_times:
            if i == 0:
                suggest_assets.append("Asset1")
            elif i == 1:
                suggest_assets.append("Server")
            elif i == 2:
                suggest_assets.append("Data Store")
            elif i == 3:
                suggest_assets.append("Lambda")
            elif i == 4:
                suggest_assets.append("Process")
            elif i == 5:
                suggest_assets.append("External Entity")

        #set a threshold where if there are more than 3 times that a transition from one state to the next occurs, it won't suggest anything and assign currentfocus to event_type

        print("Focus on: ")   # this is TEMPORARY. it will be replaced with actual user inputs so the current focus can be assigned 

        num = 0

        for i in suggest_assets:
            print(i)


        if len(suggest_assets) > 3:
            return
        elif len(suggest_assets) > 1:
           
            
            num = input(f"Pick one (from 1 to {len(suggest_assets)}):")

            while int(num) < 1 or int(num) > len(suggest_assets):
                num = input(f"Pick one (from 1 to {len(suggest_assets)}):")

            print(f"You picked {suggest_assets[(int(num) - 1)]}!")
            
           

        self.currentFocus = suggest_assets[(int(num) - 1)]

        #self.currentFocus = suggest_assets


        self.previous_events.append(event_type)
        
        self.lastevent = time.time()


        return


    def MLModel(self):

        transitionmatrix = [[0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0], 
                            [0, 0, 0, 0, 0, 0], 
                            [0, 0, 0, 0, 0, 0], 
                            [0, 0, 0, 0, 0, 0]]

        thislist = []

        anotherlist = ["Asset1", "Server", "Data Store", "Lambda", "Process", "External Entity"]
        
        for i in range(4):
            thislist.append(self.dataCollection(anotherlist[i]))

        print(thislist)

        asset_dict = {0: "Asset1", 1: "Server", 2: "Data Store", 3: "Lambda", 4: "Process", 5: "External Entity"}

        for i in range(4):
            for j in range(3):  
                l = 0; m = 0
                istrue = True
                while(istrue == True):
                    if(thislist[i][j] == asset_dict[l] and thislist[i][(j + 1)] == asset_dict[m]):
                        transitionmatrix[l][m] += 1

                    if m < 5:
                        m += 1
                    elif l < 5:
                        l += 1
                        m = 0
                    else:
                        istrue = False
                        
        print(transitionmatrix)

        return transitionmatrix




    def dataCollection(self, event_type: str) -> list:

        focus_transitionmatrix = [[], [], [], [], [], []]
        
        for i in focus_transitionmatrix:
            for j in range(6):
                i.append(0.0)   

        for i in range(6):
            self.getRandomNumber(i, focus_transitionmatrix)
            smallest = focus_transitionmatrix[i][0]
            index = 0; theloc = 0
            for j in focus_transitionmatrix[i]:
                if smallest > j:
                    smallest = j
                    theloc = index
                index += 1
            if sum(focus_transitionmatrix[i]) < 1.0:
                focus_transitionmatrix[i][theloc] += (1 - sum(focus_transitionmatrix[i]))
            
        
        focus_transitionnames = [["11", "12", "13", "14", "15", "16"],
                                 ["21", "22", "23", "24", "25", "26"],
                                 ["31", "32", "33", "34", "35", "36"],
                                 ["41", "42", "43", "44", "45", "46"],
                                 ["51", "52", "53", "54", "55", "56"],
                                 ["61", "62", "63", "64", "65", "66"]]
        
        list_of_assets = []
        
        for i in range(6):

            if event_type == "Asset1":
                value = 0
            elif event_type == "Server":
                value = 1
            elif event_type == "Data Store":
                value = 2
            elif event_type == "Lambda":
                value = 3
            elif event_type == "Process":
                value = 4
            elif event_type == "External Entity":
                value = 5


            largest = focus_transitionmatrix[value][0]; secondlargest = 0.0; secindex = 0; secloc = 0; largeindex = 0; largeloc = 0

            for i in focus_transitionmatrix[value]:
                if i > largest:
                    largest = i
                    largeloc = largeindex
                largeindex += 1

            for i in focus_transitionmatrix[value]:
                if i > secondlargest and i != largest:
                    secondlargest = i
                    secloc = secindex
                secindex += 1 

            if (largest - secondlargest) <= 0.4:
                next_event = np.random.choice(focus_transitionnames[value], replace = True, p = focus_transitionmatrix[value])
            else:
                next_event = focus_transitionnames[value][largeloc]

            if next_event[1:2] == "1":
                list_of_assets.append("Asset1")
                event_type = "Asset1"
            elif next_event[1:2] == "2":
                list_of_assets.append("Server")
                event_type = "Server"
            elif next_event[1:2] == "3":
                list_of_assets.append("Data Store")
                event_type = "Data Store"
            elif next_event[1:2] == "4":
                list_of_assets.append("Lambda")
                event_type = "Lambda"
            elif next_event[1:2] == "5":
                list_of_assets.append("Process")
                event_type = "Process"
            elif next_event[1:2] == "6":
                list_of_assets.append("External Entity")
                event_type = "External Entity"

        
        return list_of_assets


    def getRandomNumber(self, index: int, thislist: list):
            
            for i in range(6):
                rand_num = random.random() % 0.5
                if thislist[index][i] == 0.0:
                    while((sum(thislist[index]) + rand_num) > 1.0):
                        rand_num = random.random() % 0.5
                    thislist[index][i] = rand_num

            return



thisengine = NaturalEngine("ThisName", "Server", "ThisDesc")

thisengine.event(thisengine.currentFocus)

thisengine.event(thisengine.currentFocus)

thisengine.event(thisengine.currentFocus)

thisengine.event(thisengine.currentFocus)

thisengine.event(thisengine.currentFocus)

print(thisengine.previous_events)












    