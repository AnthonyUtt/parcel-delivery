# C950 - Anthony Utt - autt3 - ID#000854797


"""Module for creating Priority Queue data structure"""

class PriorityQueue:
    """Priority Queue"""

    # This class handles the bulk of the algorithm, which is sorting 
    # the prioritized parcels to ensure that we are delivering them 
    # in the correct order. The heuristic of the algorithm is the 
    # assumption that, if we deliver parcels in order of priority, 
    # we will deliver all parcels on-time.

    def __init__(self):
        # init has a runtime of O(1)
        self.queue = []
        
    def push(self, item):
        # This function has the main sorting algorithm that prioritizes 
        # the parcels and ensures that we are delivering them in the 
        # right order. This algorithm is a version of insertion sort,
        # which has a worst-case runtime of O(N^2).

        if item not in self.queue:
            # queue will stay sorted by having the push
            # method put items in the "correct" place
            added = False
            index = 0
            while not added and index < len(self.queue):
                if item > self.queue[index]:
                    self.queue.insert(index, item)
                    added = True
                else:
                    index = index + 1
            
            if not added:
                self.queue.append(item)

    def remove(self, item):
        # This method has a runtime of O(N) as it looks through the 
        # list linearly to find the item.
        if item in self.queue:
            self.queue.remove(item)
    
    def pop(self):
        # because the queue will always be sorted from largest to smallest,
        # we can make the pop function always run in O(1) time since the
        # largest value is always at index 0
        if len(self.queue) > 0:
            item = self.queue[0]
            del self.queue[0]
            return item

    def peek(self):
        # this method has a runtime of O(1)
        if len(self.queue) > 0:
            return self.queue[0]

    def count(self):
        # this method has a runtime of O(N) where N is the number of items in
        # the data structure already
        count = 0
        for item in self.queue:
            count = count + item.count()
        return count

    def contains(self, item):
        # this method has a runtime of O(N) where N is the number of items in 
        # the data structure already
        for group in self.queue:
            if item in group.items():
                return True
        return False
    
    def items(self):
        # this method has a runtime of O(1)
        return self.queue

    def print_all(self):
        # this method has a runtime of O(N) where N is the number of items in 
        # the data structure already
        for group in self.queue:
            for item in group.items():
                print(str(item))