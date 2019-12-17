# C950 - Anthony Utt - autt3 - ID#000854797

from parcel import Parcel

class ParcelGroup:
    """ParcelGroup class
    Holds Parcels that are to be delivered to the same node.
    """

    # This class is a structure to hold multiple parcels 
    # more efficiently than just using a simple list. All 
    # of the methods in this class, with the exception of 
    # the add_parcel method, run in O(1) time.
    def __init__(self):
        self.parcels = []
        self.max_priority = float('-inf')
        self.destination = None
        self.linked = False

    def add_parcel(self, parcel):
        # This method checks the parcel to be added against 
        # the parcels already in the data structure. It also 
        # updates the priority and linked status of the group 
        # to self-adjust and make the program work more fluidly.
        # This method runs in O(N) time, where N is the number of 
        # parcels in the group.
        if parcel not in self.parcels:
            self.parcels.append(parcel)
            if parcel.priority > self.max_priority:
                self.max_priority = parcel.priority
            if self.destination is None:
                self.destination = parcel.delivery_node
            elif self.destination is not parcel.delivery_node:
                raise Exception
            if parcel.linked:
                self.linked = True
    
    # The methods after this point are self-evident getters 
    # and setters, or overridden operator functions.
    def get_destination(self):
        return self.destination
    
    def is_linked(self):
        return self.linked
    
    def count(self):
        return len(self.parcels)
    
    def items(self):
        return self.parcels
    
    def set_priority(self, value):
        self.max_priority = value
    
    def __lt__(self, other):
        if self.max_priority < other.max_priority:
            return True
        return False

    def __gt__(self, other):
        if self.max_priority > other.max_priority:
            return True
        return False
    
    def __le__(self, other):
        if self.max_priority <= other.max_priority:
            return True
        return False
    
    def __ge__(self, other):
        if self.max_priority >= other.max_priority:
            return True
        return False
        