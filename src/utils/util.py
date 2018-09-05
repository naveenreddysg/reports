from sqlalchemy.orm.mapper import class_mapper
from sqlalchemy import inspect
import time
from random import randint

def model_to_dict(obj, visited_children=None, back_relationships=None):
    if visited_children is None:
        visited_children = set()
    if back_relationships is None:
        back_relationships = set()
    serialized_data = {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
    relationships = class_mapper(obj.__class__).relationships
    visitable_relationships = [(name, rel) for name, rel in relationships.items() if name not in back_relationships]
    for name, relation in visitable_relationships:
        if relation.backref:
            back_relationships.add(relation.backref)
        relationship_children = getattr(obj, name)
        if relationship_children is not None:
            if relation.uselist:
                children = []
                for child in [c for c in relationship_children if c not in visited_children]:
                    visited_children.add(child)
                    children.append(model_to_dict(child, visited_children, back_relationships))
                serialized_data[name] = children
            else:
                serialized_data[name] = model_to_dict(relationship_children, visited_children, back_relationships)
    return serialized_data

def toD36(dec):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    hex_str = ''
    if dec == 0:
       return '0'

    while dec != 0:
        hex_str += digits[dec % 36]
        dec = dec // 36

    return hex_str[::-1]

uniqueId = 0
def uid():
    global uniqueId
    utime = int(time.time());
    if uniqueId == utime :
        time.sleep(1)
        utime = int(time.time());
    uniqueId = utime;
    return toD36(utime);


def random_number(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)