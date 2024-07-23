from uuid import uuid4, UUID
import time
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import train_test_split
from math import e




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
        
        transition_matrix = self.MLModel()

        self.previous_events.append(event_type)
        
        self.lastevent = time.time()


        return


    def MLModel(self) -> list:

        nodes_count = random.randint(2, 10)

        transitionmatrix = []

        for i in range(6):
            transitionmatrix.append([])

        for i in transitionmatrix:
            for j in range(6):
                i.append(0.0)

        #generates random graphs for now 
 
        anotherlist = ["Asset1", "Server", "Data Store", "Lambda", "Process", "External Entity"]

        randnum = random.randint(0, 5)

        the_graph = self.dataCollection(anotherlist[randnum])

        the_workflows = []

        add_indicator = 0; randworkflows = random.randint(1, (nodes_count - 1))
        
        for index in range(randworkflows):
            the_workflows.append([])

        for i in the_workflows:
            while(len(i) == 0 or len(i) == 1):
                for j in the_graph:
                    add_indicator = random.randint(0, 1)
                    if add_indicator == 1:
                        i.append(j)
            
        #removed the random sequences and the associated transition matrix

        asset_dict = {0: "Asset1", 1: "Server", 2: "Data Store", 3: "Lambda", 4: "Process", 5: "External Entity"}

        data = []
        
        index_col = []

        for num in range(36):
            index_col.append(num)
            data.append([])
    
        index = 0
        for i in range(6):
            for j in range(6):
                data[index].append(transitionmatrix[i][j]) 
                if i == j:
                    data[index].append(1)
                else:
                    data[index].append(0)

                index += 1

        for j in the_workflows:
            for i in range(6):
                for k in j:
                    if asset_dict[i] == k:
                        for m in j:
                            for l in range(6):
                                if asset_dict[l] == m and len(data[(i * 6) + l]) < 3:
                                    data[(i * 6) + l].append(1)

        for i in data:
            if (len(i) < 3):
                i.append(0)

        theindex = 0

        #changing the intercept will enhance accuracy

        for i in range(6):
             for j in range(6):
                transitionmatrix[i][j] = e**(4.5) * e**(0.04433293 * (data[theindex][1])) * e**(0.08243643 * (data[theindex][2]))
                theindex += 1

        index = 0
        for i in range(6):
            for j in range(6):
                data[index][0] = (transitionmatrix[i][j]) 
                index += 1
                
        
        thislist = []

        for num in range(36):
            thislist.append(num)

        relation_df = pd.DataFrame(data, index = thislist, columns = ["O", "Type_Check", "Workflow_Check"])

        check_columns = ["Type_Check", "Workflow_Check"]

        target_columns = "O"

        these_checks = relation_df[check_columns]

        the_target = relation_df[target_columns]

        poisson_regression = PoissonRegressor()

        check_train, check_test, target_train, target_test = train_test_split(these_checks, the_target, test_size = 0.33, random_state = 30)

        poisson_regression.fit(check_train, target_train)

        accuracy_train = poisson_regression.score(check_train, target_train)

        accuracy_test = poisson_regression.score(check_test, target_test)

        print(f"Accuracy train: {accuracy_train}")

        print(f"Accuracy test: {accuracy_test}")

        predicted_outcomes_one = poisson_regression.predict(check_train)

        predicted_outcomes_two = poisson_regression.predict(check_test)

        print(predicted_outcomes_one)

        print(predicted_outcomes_two)

        print(predicted_outcomes_all)

        predicted_outcomes_all = poisson_regression.predict(these_checks)

        new_transition_matrix = []

        these_indexes = 0
        
        for i in range(6):
            new_transition_matrix.append([])
            for j in range(6):
                new_transition_matrix[i].append(predicted_outcomes_all[these_indexes])
                these_indexes += 1

        return new_transition_matrix

        #fit is the coeficcents, predict is the outcomes



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


thisengine = NaturalEngine("ThisName", "Asset1", "ThisDesc")

thisengine.event("Asset1")











    
