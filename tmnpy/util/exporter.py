

# load threat model
# class Parser(object):
#     def load_yaml(self, file_path):
#         with open(file_path, "r") as file:
#             data = yaml.safe_load(file)
#         return data


class Exporter(object):
    def __init__(self, tm_name: str):
        self.tm = TM(tm_name)

        # if "actors" in self.yaml.keys():
        #     for actor in self.yaml["actors"]:
        #         elem_type, kwargs = self.parse_element(actor)
        #         self.tm.actors.append(elem_type(**kwargs))
        # if "assets" in self.yaml.keys():
        #     for asset in self.yaml["assets"]:
        #         elem_type, kwargs = self.parse_component(asset)
        #         self.tm.components.append(elem_type(**kwargs))
        # if "flows" in self.yaml.keys():
        #     for flow in self.yaml["flows"]:
        #         elem_type, kwargs = self.parse_component(flow)
        #         self.tm.components.append(elem_type(**kwargs))
        # if "boundaries" in self.yaml.keys():
        #     for boundary in self.yaml["boundaries"]:
        #         elem_type, kwargs = self.parse_boundary(boundary)
        #         self.tm.boundaries.append(elem_type(**kwargs)) 




    def convert_boundary(self, boundary):

    def convert_component(self, component):

    def convert_element(self, element):




#iterate through everything 


# return a yaml file

















"""
create a dictionary 



when you read in yaml fil eit read into a dictionary 


figure out a way to convert the objects into dictionaries 



only of hte first high level keys  is assets -. list of assets

query the threat model 
get me all of the assets




2 ways 
- no threat model jus otbject 
- 2 dict 



assets should get name, type (class name), security property, machine, data 
create a function in the assets class classed 2 dict and build the dictionary

create an assets object and 



convert the diction to tmnpy object 
take those tmnpy object turn to dictionary 
and then turn to yaml 



write the reverse opertation from parser 






2 ways:
- wtire 2 dict funtion (NO)
- or serialer 
        - list of objects and write reverse of parser





python 
from tmnpy.dsl import Asset, DataFlow
test = Asset("test")
dir(test)
test.__dict__
import yaml
with open("test.yanml"m "w') as f:
        yaml.safe_dump(test.__dict__, f)
obj_dict = test.__dict__
obj_dict
for k, v, in obj_dict.items():
    if isinstance(v, object):
        print("found!", k)
obj_dict["_Component__security_roperty"]
obj_dict["_Component__security_roperty"].__dict__
#in the case of none, they are those we dont need ot bother with 
if none ifnore and not put in 





run parser in terminal 
have threat model objects 
use those to help write out how you would parse it 

keep iterating down until you find a place where it doesnt have dict  -> basic priminitve
can serialize in yaml 


if this is an object of this type -> stop here



go all the way down 
pass that all back and have massive dictionary 
if nothing return nothing


write that into initial 
return 


recurse for each of the piece apply dict 
for any that doesnt fail get dict error

take the dict and key at the end to the top



start with one asset/workflow/dataflow /different elemtns 

then do list of assets


write test cases before write code 

- create new test file in test directory 
test_serializer.py

from tmnpy.dsl import Asset

import unittest 

class TestSerialiEs (unittest.testcase):
    def setup 

    def test asset)name)only *self
        x = Asset("test)
        serealized = seializer(x)
        seld.assertDictEqual("name":"TEst:m "type":"Asset"), serealized["assets"]) #should output dictionary





serializer.py


"""