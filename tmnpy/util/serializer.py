import re

from enum import Enum
from tmnpy.dsl.element import Element

class TMNTSerializer(object):

    def serialize(self, element, pos, result_dict):
        obj_dict = element.__dict__

        type_name = type(element).__name__
        if (
            (type_name == "Asset") or \
            (type_name == "Actor") or \
            (type_name == "Boundary") or \
            (type_name == "DataFlow") or \
            (type_name == "ExternalEntity") or \
            (type_name == "Process") or \
            (type_name == "WorkFlow")
        ):
            result_dict["type"] = type_name

        keys = list(obj_dict.keys())
        if pos >= len(keys) or pos < 0:
            return result_dict
        else:
            if "__" in keys[pos]: 
                index = re.search("__", keys[pos]).end()
                key = keys[pos][index:]
            else:
                key = keys[pos]

            new_obj = obj_dict[keys[pos]]
            try:
                new_obj.__dict__
                if isinstance(new_obj, Enum):
                    raise AttributeError
            except AttributeError:
                if (isinstance(new_obj, list)) and (len(new_obj) > 0):
                    if isinstance(new_obj[0], Element):
                        obj_lst = []
                        for obj in new_obj:
                            obj_lst.append(self.serialize(obj, 0, {}))
                        result_dict[key] = obj_lst
                    else:
                        result_dict[key] = new_obj
                elif (
                    (new_obj != None) and \
                    (new_obj != "N/A") and \
                    (new_obj != []) and \
                    (new_obj != set())
                ):
                    result_dict[key] = new_obj
            else:
                result_dict[key] = self.serialize(new_obj, 0, {})
                
            return self.serialize(element, pos+1, result_dict)


    def serialize_list(self, lst, result_dict):
        elem_lst = []
        for elem in lst:
            elem_lst.append(self.serialize(elem, 0, {}))
        
        type_name = type(lst[0]).__name__
        if ((type_name == "DataFlow") or (type_name == "WorkFlow")):
            result_dict["flows"] = elem_lst
        elif (type_name == "Boundary"):
            result_dict["boundaries"] = elem_lst
        else:
            name = type_name.lower() + "s"
            result_dict[name] = elem_lst
            
        return result_dict
    