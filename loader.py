# C950 - Anthony Utt - autt3 - ID#000854797

from table import Table
from parcel_group import ParcelGroup
import math

class Loader:
    # The Loader class manages the sorting of parcels between the 
    # trucks to make sure that we get an even spread between all 
    # active trucks so that no one truck gets an unfair load

    # init completes in O(1)
    def __init__(self, parcel_table, graph):
        self.parcel_table = parcel_table
        self.graph = graph

    # the function call in this function completes in O(1)
    def get_remaining_parcels(self):
        return self.parcel_table.lookup(status='AT HUB', deadline='None')

    # set_parcel_priority() runs in O(1) time
    def set_parcel_priority(self, parcel):
        priority = 0
        # bit of math to determine how to prioritize the parcels
        if parcel.delivery_deadline is not None:
            priority = 5 - math.ceil((parcel.delivery_deadline - 800) / 60)
        parcel.set_priority(priority)
    
    def create_parcel_group(self, parcel):
        # This method has a worst-case runtime of O(N). It queries the table 
        # to find all parcels going to a given destination and then creates 
        # a ParcelGroup to hold those parcels
        destination = parcel.delivery_node
        group_items = self.parcel_table.lookup(delivery_node=destination)
        new_group = ParcelGroup()
        for item in group_items:
            new_group.add_parcel(item)

        return new_group
        
    def get_all_linked_parcels(self):
        # This method has a worst-case runtime of O(N) as it looks through 
        # each parcel in the system to check whether it is a linked parcel
        values = []
        for parcel in self.parcel_table.items():
            if parcel.linked:
                values.append(parcel)

        return values

    def confirm_links(self, parcel):
        # This method runs in O(N) as it looks through each parcel to 
        # make sure all linked parcels are marked as such
        if parcel.companion_parcels:
            parcel.linked = True
        else:
            for p in self.parcel_table.items():
                if len(p.companions) > 0:
                    if parcel.id in p.companions:
                        parcel.linked = True

    def reorder_parcels(self, load):
        d_node_list = [i.get_destination() for i in load]
        route = []
        curr_node = self.graph.get_node(1)
        while len(d_node_list) > 0:
            next_node = None
            for node in d_node_list:
                if curr_node.get_distance(node) < curr_node.get_distance(next_node):
                    next_node = node
            route.append(next_node)
            d_node_list.remove(next_node)
            curr_node = next_node

        new_load = []
        for i, dest in enumerate(route):
            for parcel_group in load:
                if parcel_group.get_destination() is dest:
                    parcel_group.set_priority(len(load) + parcel_group.max_priority**2 - i)
                    new_load.append(parcel_group)
        return new_load

    def send_to_truck(self, truck, load):
        # This method has a worst-case runtime of O(N) as it adds 
        # parcel groups to the truck
        for parcel_group in load:
            truck.add_parcel_group(parcel_group)
        
    def get_load_count(self, load):
        # This method runs through each ParcelGroup in the load and 
        # takes a cumulative count of the number of parcels in each 
        # ParcelGroup. It has a worst-case runtime of O(N)
        count = 0
        for group in load:
            count = count + group.count()
        
        return count
    
    def check_duplicates(self, load, parcel):
        # This method runs through the parcels in the load to make sure 
        # there are no duplicate groups in the load
        is_duplicate = False

        for group in load:
            if parcel in group.items():
                is_duplicate = True

        return is_duplicate
    
    def build_parcel_list(self, truck, deadline_parcels, remaining_parcels):
        # This method contains the bulk of the processing and sorting of 
        # parcels. It has a worst-case runtime of O(N) when simplified, as 
        # it runs through the list of parcels a finite number of times.

        remaining_parcels.sort(reverse=True)
        
        load = []
        for dl_parcel in deadline_parcels:  # looping through priority parcels
            if self.get_load_count(load) < truck.get_max_capacity():
                if not self.check_duplicates(load, dl_parcel):
                    new_group = self.create_parcel_group(dl_parcel)
                    load.append(new_group)

                    if dl_parcel.linked:  # checking linked parcels
                        for linked_parcel in self.get_all_linked_parcels():
                            if not self.check_duplicates(load, linked_parcel):
                                linked_group = self.create_parcel_group(linked_parcel)
                                load.append(linked_group)

        for parcel in remaining_parcels:  # looping through remaining parcels
            if self.get_load_count(load) < truck.get_max_capacity():
                if not self.check_duplicates(load, parcel):
                    new_group = self.create_parcel_group(parcel)
                    load.append(new_group)

                    if parcel.linked:  # checking linked parcels
                        for linked_parcel in self.get_all_linked_parcels():
                            if not self.check_duplicates(load, linked_parcel):
                                linked_group = self.create_parcel_group(linked_parcel)
                                load.append(linked_group)
        
        offset = 0
        # Here we make sure that the load count doesn't exceed the 
        # capacity of the trucks. We remove non-linked parcels so that 
        # we don't ignore the special instructions
        while self.get_load_count(load) > truck.get_max_capacity():
            if not load[offset].is_linked():  #making sure it's not linked
                load.remove(load[offset])
            else:
                offset = offset + 1
 
        return load


    def load(self):
        # assigning priority and finding links between parcels
        # this method runs in O(N) time
        for parcel in self.parcel_table.items():
            self.set_parcel_priority(parcel)
            self.confirm_links(parcel)

    def run(self, trucks):
        # This method gathers the parcels that still need to be delivered 
        # and separates them out into lists that match the number of 
        # trucks that are currently available to be loaded. Additionally,
        # it calls the method that loads the parcels onto the trucks. 
        # This method runs in O(N) time, where N is the number of trucks 
        # supplied in the trucks variable.
        deadline_parcels = self.parcel_table.lookup(status='AT HUB', deadline='not None')
        dl_parcels_per_truck = (len(deadline_parcels) // len(trucks)) \
            + (len(deadline_parcels) % len(trucks))

        remaining_parcels = self.get_remaining_parcels()

        if len(remaining_parcels) == 0:
            return 1

        for truck in trucks:
            deadline_parcels = self.parcel_table.lookup(status='AT HUB', deadline='not None')
            remaining_parcels = self.get_remaining_parcels()

            dl_parcels_this_truck = []
            if dl_parcels_per_truck < len(deadline_parcels):
                dl_parcels_this_truck = deadline_parcels[:dl_parcels_per_truck]
                deadline_parcels = deadline_parcels[dl_parcels_per_truck:]
            else:
                dl_parcels_this_truck = deadline_parcels

            load = self.build_parcel_list(truck, dl_parcels_this_truck, remaining_parcels)
            new_load = self.reorder_parcels(load)
            self.send_to_truck(truck, new_load)
            
        return 0