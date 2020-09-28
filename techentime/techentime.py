from collections import namedtuple
from collections.abc import Sequence
from numbers import Number
from functools import reduce
from datetime import datetime, date, timezone
from dateutil.parser import isoparse

### CLASSY SECTION ################################### BEGINS

class Techentime (namedtuple("Techentime", ["n","unit",])):

    def weights (self, unit: int) -> (int, int):
        if not isinstance(unit,int):
            raise TypeError(f"unit must be of type int; not {type(unit)}")
        
        if unit == 0:
            return (10, 60)
        elif unit == 1:
            return (60, 24)
        elif unit == 2:
            return (24, 365)
        elif unit == 3:
            return (365, 10)
        elif unit < 0 or unit > 3:
            return (10, 10)
        else:
            raise Exception("Congrats! You managed to pass techentime rebase operation an int that was not < 0, 0, 1, 2, 3, > 3. You should publish a paper on this.\nMagic number = {unit}") 
        
    def __new__ (cls, n: Number, unit: int)-> tuple:
        # type checking
        if not isinstance(n, Number):
            raise TypeError(f"n must be a number not {type(n)}")
        if not isinstance(unit, int):
            raise TypeError(f"unit must be a number not {type(unit)}")
        obj = super(Techentime, cls).__new__(cls, n, unit)
        return obj


    def __add__ (self, other: Number or Sequence):
        if isinstance(other, Number):
            n    = other
            unit = self[1]
        else:
            n, unit = other
        if unit != self[1]:
            raise ValueError(f'{self} cannot be added to techentime like object with unit {unit}')
        return Techentime(self[0]+n,self.unit)

    def __sub__ (self, other):
        if isinstance(other, Number):
            n    = -1*other
            unit = self[1]
        else:
            n    = -1*other[0]
            unit = other[1]
        if unit != self[1]:
            raise ValueError(f'{self} cannot be added to techentime like object with unit {unit}')
        return Techentime(self[0]+n,self.unit)


    def __lshift__(self, other: int):
        if other < 0:
            raise ValueError("Cannot shift by negative number ({other}).")
        operation = lambda x, y: x*(self.weights(y)[1]**-1)
        cofactor=reduce(operation, range(self.unit, self.unit+other), 1)
        return Techentime(cofactor*self.n, self.unit+other)

    def __rshift__(self, other: int):
        if other < 0:
            raise ValueError("Cannot shift by negative number ({other}).")
        operation = lambda x, y: x*(self.weights(y)[0])
        cofactor=reduce(operation, range(self.unit, self.unit-other, -1), 1)
        return Techentime(cofactor*self.n, self.unit-other)
 
### CLASSY SECTION ################################### ENDS

#### FUNCTION SECTION ################################ BEGINS
   

def datetime_to_techentime (dt: datetime, unit=0) -> Techentime:
    epoch = datetime(1970,1,1).astimezone(timezone.utc)
    utcdt = dt.astimezone(timezone.utc)
    time = Techentime(int((utcdt - epoch).total_seconds()), 0)
    return time << unit if unit >=0 else time >> abs(unit)

def date_to_techentime(d: date, unit=0) -> Techentime:
    return datetime_to_techentime(datetime.combine(d, datetime.min.time()), unit)
    
def now(unit=0):
    return datetime_to_techentime(datetime.now().astimezone(timezone.utc), unit=unit)

def timestamp_to_techentime(timestamp: str) -> Techentime:
    return datetime_to_techentime(isoparse(timestamp))

def ttime_to_pytime (ttime: Techentime) -> datetime:
    rewind = ttime >> ttime.unit if ttime.unit >= 0 else ttime << ttime.unit
    return datetime.fromtimestamp(rewind.n)
        
    
#### FUNCTION SECTION ################################ ENDS


#### GLOBAL SECTION ################################## BEGINS
'''
Jeff time transform digraph

                              ¯infinity    →×10→  ¯infinity

                                ...

        ¯2 (hundreths) ←×10←  ¯1 (tenths)  →÷10→  0 (seconds)

        ¯1 (tenths)    ←×10←  0 (seconds)  →÷60→  +1 (hours)
        
        0 (seconds)    ←×60←  +1 (hours)   →÷24→  +2 (days)

        +1 (hours)     ←×24←  +2 (days)    →÷356→ +3 (years)

        +2 (days)      ←×365← +3 (years)   →÷10→  +4 (10years)

                                ...

        +infinity      ←÷10←  +infinity
'''
#### GLOBAL SECTION ################################## BEGINS
