from uuid import uuid4, UUID
import time
import numpy as np
import random
import pandas as pd
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import train_test_split
from math import e 
from tmnpy.dsl.flow import DataFlow, WorkFlow






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
        transition_matrix: list = [],
    ):
        self.currentFocus = currentFocus
        self.previous_events = []
        self.asset_dict = {}
        self.transition_matrix = transition_matrix
        self.lastevent = time.time()
        super().__init__(name, desc)

        

    def event(self, event_type: str):
        # Get the event and check what type it is, then plug into markov model to predict new focus.  Update list of previous events to include this.
        
        #transition_matrix = self.MLModel()

        new_matrix = self.transition_matrix

        largest = new_matrix[self.asset_dict[event_type]][0]; loclist = []

        for i in new_matrix[self.asset_dict[event_type]]:
            if largest < i:
                largest = i
                
        index = 0
        for i in new_matrix[self.asset_dict[event_type]]:
            if i == largest:
                loclist.append(index)
            
            index += 1

        isTrue = False

        for i in range(loclist):
            if i == self.asset_dict[event_type]:
                isTrue = True

        if isTrue == True:

            second_largest = new_matrix[self.asset_dict[event_type]][0]

            for i in new_matrix[self.asset_dict[event_type]]:
                if second_largest < i and i != largest:
                    second_largest = i
        
            theindextwo = 0
            for i in new_matrix[self.asset_dict[event_type]]:
                if i == second_largest:
                    loclist.append(theindextwo)

                theindextwo += 1

        
        asset_suggestions = []

        asset_dict_two = {}

        for i, j in self.asset_dict.items():
            asset_dict_two[j] = i

        for i in loclist:
            asset_suggestions.append(asset_dict_two[i])


        self.currentFocus = asset_suggestions
    


        self.previous_events.append(event_type)
        
        self.lastevent = time.time()


        return 


        #fit is the coeficcents, predict is the outcomes

    #This function will have the random transition matrix that can be utilized to obtain the coefficients
    
    
    def getCoefficients(self, current_graph: list, current_flows: list):

        this_transition_matrix = []

        asset_dict = {}; asset_dict_two = {}; the_size = len(current_graph)

        for i in range(the_size):
            asset_dict[i] = current_graph[i]

        for i in range(the_size):
            asset_dict_two[current_graph[i]] = i

        self.asset_dict = asset_dict_two


        for i in range(the_size):
            this_transition_matrix.append([])

        for i in range(the_size):
            for j in range(the_size):
                this_transition_matrix.append(0.0)

        
        #uses previous events to build initial transition matrix
        for i in range(the_size):
            for j in range(the_size):
                for k in range(len(self.previous_events) - 1):
                    if asset_dict[i] == self.previous_events[k] and asset_dict[j] == self.previous_events[(k + 1)]:
                        this_transition_matrix[i][j] += 1
    

        data = []
        
        index_col = []

        for num in range(the_size**2):
            index_col.append(num)
            data.append([])
    
        #outcomes
        for i in range(the_size):
            for j in range(the_size):
                data[index].append(this_transition_matrix[i][j]) 

        #type check
        index = 0
        for i in range(the_size):
            for j in range(the_size):
                data[index].append(this_transition_matrix[i][j]) 
                if i == j:
                    data[index].append(1)
                else:
                    data[index].append(0)

                index += 1

         #checks if they are apart of the same workflow 
        for i in current_flows:
            if isinstance(i, WorkFlow):
                for j in i.path:
                    for k in i.path:
                        data[(asset_dict_two[j] * the_size) + asset_dict_two[k]].append(1)
                                    

        for i in data:
            if (len(i) < 3):
                i.append(0)

        #checks if the assets are neighbors
        for i in current_flows:
            if isinstance(i, DataFlow):
                data[(asset_dict_two[i[0]] * the_size) + asset_dict_two[i[1]]].append(1)


        for i in data:
            if (len(i) < 4):
                i.append(0)

        

        thislist = []

        for num in range(the_size**2):
            thislist.append(num)

        relation_df = pd.DataFrame(data, index = thislist, columns = ["O", "Type_Check", "Workflow_Check", "Neighbor_Check"])
        
        print("\n")

        print(relation_df)


        check_columns = ["Type_Check", "Workflow_Check", "Neighbor_Check"]

        target_columns = "O"

        these_checks = relation_df[check_columns]

        the_target = relation_df[target_columns]

        poisson_regression = PoissonRegressor()

        check_train, check_test, target_train, target_test = train_test_split(these_checks, the_target, test_size = 0.33, random_state = 30)

        poisson_regression.fit(check_train, target_train)

        accuracy_train = poisson_regression.score(check_train, target_train)

        accuracy_test = poisson_regression.score(check_test, target_test)

        print(f"accuracy train: {accuracy_train}")

        print(f"accuracy test: {accuracy_test}")

        the_coefficients = poisson_regression.coef_



        return data, the_coefficients
    

    def newTransitionMatrix(self, the_graph: list, the_flows: list):

        data, these_coefficients = self.getCoefficients(current_graph= the_graph, current_flows= the_flows)

        new_transition_matrix = []; the_size = len(the_graph)

        for i in range(the_size):
            new_transition_matrix.append([])

        for i in range(the_size):
            for j in range(the_size):
                new_transition_matrix[i].append(0.0)

        theindex = 0
        for i in range(the_size):
            for j in range(the_size):
                new_transition_matrix[i][j] = e**(these_coefficients[0] * data[theindex][1]) * e**(these_coefficients[1] * data[theindex][2]) * e**(these_coefficients[2] * data[theindex][3])
                theindex += 1

        return new_transition_matrix











    