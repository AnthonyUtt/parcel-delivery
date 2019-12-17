# C950 - Anthony Utt - autt3 - ID#000854797

import math
from priority_queue import PriorityQueue
#from parcel_group import ParcelGroup
#from main import CapacityError

class Truck:
    def __init__(self, id_=None, driver=None, capacity=16, hub_node=None):
        # The Truck object holds all of the necessary attributes of each
        # truck that is in service, as well as some methods related to 
        # the movement of each truck through our simulation.

        # Basic attributes for the object
        self.id = id_
        self.driver = driver
        self.capacity = capacity
        self.hub_node = hub_node
        self.speed = 0.4  # 18 mph converted to miles per minute
        self.total_miles = 0

        self.cargo = PriorityQueue()
        self.current_time = None
        self.arrival_time = None

        self.prev_node = None
        self.curr_node = None
        self.next_node = None

        self.finished = False

    def get_total_miles(self):
        return self.total_miles

    def add_parcel_group(self, parcel_group):
        # This method pushes the ParcelGroup into the PriorityQueue,
        # as well as setting the status of all parcels in the group
        # to show that they have been loaded onto the truck. It has
        # a runtime complexity of O(N), where N is the number of 
        # parcels in parcel_group.
        self.cargo.push(parcel_group)
        for parcel in parcel_group.items():
            parcel.set_status('EN ROUTE - TRUCK ' + str(self.id))

    def deliver_parcels(self):
        # This method grabs the next ParcelGroup from the PriorityQueue
        # and simulates the deliver of each parcel at the destination.
        # It also checks to be sure that the parcels were delivered
        # on-time and sets the status accordingly. It has a runtime
        # of O(N), where N is the number of parcels in this group.
        parcel_group = self.cargo.pop()
        for parcel in parcel_group.items():
            if parcel.delivery_deadline is not None:
                if self.current_time <= parcel.delivery_deadline:
                    parcel.set_status('DELIVERED')
                else:
                    parcel.set_status('DELIVERED LATE')
            else:
                parcel.set_status('DELIVERED')

    def get_next_node(self):
        # This method looks at the next group of parcels to be 
        # delivered and grabs the destination node for that 
        # group. It has a runtime of O(1).
        next_ = self.cargo.peek()
        if next_ is not None:
            return next_.destination
        else:
            return self.hub_node

    def calc_arrival_time(self):
        # This function does a bit of calculations to find the truck's 
        # arrival time at its destination. The result is in minutes,
        # rounded up (assuming slower rather than faster). The method
        # has a runtime of O(1).
        if (self.curr_node is self.next_node):
            return self.current_time
        else:
            the_time = (self.current_time + math.ceil( \
                self.curr_node.get_distance(self.next_node) / self.speed))
            
            if int(str(the_time)[-2:]) >= 60:
                the_time = the_time + 40
            return the_time

    def load_count(self):
        # Getter function, runtime of O(1)
        return self.cargo.count()

    def print_cargo(self):
        # printing all parcels in the cargo, runtime of O(1)
        self.cargo.print_all()

    def get_max_capacity(self):
        #Getter function, runtime of O(1)
        return self.capacity

    def get_arrival_time(self):
        # Getter function, runtime of O(1)
        return self.arrival_time

    def start(self, timestamp):
        # This method sets starting values for the truck. It has
        # a runtime of O(1).
        self.current_time = timestamp
        self.curr_node = self.hub_node
        self.next_node = self.get_next_node()
        self.arrival_time = self.calc_arrival_time()

    def update(self, timestamp):
        # This method updates the truck with the current_time.
        # Then, some logic takes place to see if the truck has arrived 
        # at its destination and whether it should deliver parcels.
        # This method has a runtime of O(1).

        self.current_time = timestamp

        if self.current_time >= self.arrival_time:
            if self.finished is not True:
                self.total_miles += self.curr_node.get_distance(self.next_node)
            self.prev_node = self.curr_node
            self.curr_node = self.next_node

            if self.cargo.count() > 0:
                # Deliver all parcels for current node
                self.deliver_parcels()

                if self.cargo.count() == 0:
                    self.next_node = self.hub_node
                else:
                    self.next_node = self.get_next_node()
                
                self.arrival_time = self.calc_arrival_time()
            else:
                if self.curr_node is self.hub_node:
                    # Returning 1 here will tell the controller that 
                    # the truck has returned to the hub to reload. If 
                    # there are no more parcels to be delivered at the 
                    # hub, the truck will be retired for the day via 
                    # the finish_day() method
                    return 1
                else:
                    return 0
        else:
            # Returning 0 here will tell the controller that the truck 
            # is still in transit to its next destination
            return 0
    
    def finish_day(self):
        # Setter function, runtime O(1)
        self.finished = True
    

    def is_finished(self):
        # Getter function, runtime O(1)
        return self.finished
