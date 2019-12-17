# C950 - Anthony Utt - autt3 - ID#000854797

from random import randint

class Parcel:
    """Class that contains information about parcels"""

    # This class is a data structure that holds information about 
    # each parcel to be delivered. Each of the main methods in this 
    # class has a runtime complexity of O(1) because there are a finite 
    # number of statements to be executed for each parcel.

    def __init__(self, id_, address, city, state, zip_, \
                deadline, mass, instr, status):

        # basic attributes of each parcel
        self.id = int(id_)
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_
        self.mass = mass
        self.special_instructions = instr
        self.status = status

        # Parsing the delivery time
        if deadline == 'EOD':
            self.delivery_deadline = None
        else:
            if 'PM' in deadline:
                offset = 1200  # for 24-hour time
            else:
                offset = 0
        
            self.delivery_deadline = int(deadline.replace(' AM', '')\
                .replace(' PM', '').replace(':', '')) + offset

        # priority is set to negative infinity here because that is the 
        # the smallest possible number. Our priority queue will deliver 
        # the highest priority parcels first, and this number will be 
        # changed later
        self.priority = float("-inf")

        # setting delivery_node to None, this will be reassigned by the 
        # system at a later point
        self.delivery_node = None

        # attributes assigned when special instructions are parsed
        # if new possibilities of spec. instructions are added, this 
        # section and parse_special_instructions() will need to be 
        # updated.
        self.delayed = None
        self.arrival_time = None
        self.required_truck = None
        self.wrong_address = None
        self.companion_parcels = None
        self.companions = []
        self.linked = False

    def set_status(self, status):
        self.status = status  # updating status

    def set_node(self, graph):
        # this function gets the delivery node using the graph object
        self.delivery_node = graph.get_node_by_address(self.address, self.zip)

    def set_priority(self, num):
        self.priority = num  # setting priority for the parcel

    def parse_special_instructions(self):
        """Parses special instructions included in parcel file."""

        # This function parses the special instructions that are assigned 
        # to each parcel. Since the logic is a series of if/else blocks 
        # and there are no loops in the function, it has a runtime of 
        # O(1).

        instr = self.special_instructions.upper()

        # These sections are self-evident. Parsing into instr and then 
        # assigning values to the necessary attributes above.
        if 'DELAYED' in instr:
            self.delayed = True

            words = instr.split()
            for word in words:  #string manipulation to get the right time
                if ':' in word:
                    if 'PM' in instr:
                        offset = 1200
                    else:
                        offset = 0
                
                    self.arrival_time = int(word.replace(':', '')) + offset
        elif 'TRUCK' in instr:  #setting required truck
            words = instr.split()
            self.required_truck = int(words[-1])
        elif 'WRONG ADDRESS' in instr:  #setting wrong address
            self.wrong_address = True
        elif 'DELIVERED WITH' in instr:  #setting links
            self.companion_parcels = True
            self.linked = True

            words = instr.split()
            next_ = False
            for word in words:  #string manipulation to get all links
                if next_:
                    self.companions.append(int(word.replace(',', '')))
            
                if 'WITH' in word:
                    next_ = True

    # standard operator overrides
    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        return False

    def __gt__(self, other):
        if self.priority > other.priority:
            return True
        return False

    def __le__(self, other):
        if self.priority <= other.priority:
            return True
        return False
    
    def __ge__(self, other):
        if self.priority >= other.priority:
            return True
        return False

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __ne__(self, other):
        if self.id != other.id:
            return True
        return False

    def __str__(self):
        value = 'Parcel ' + str(self.id) + '\t\t[' + self.status + ']'
        if self.status == 'AT HUB' or self.status == 'DELIVERED':
            value = value + '\t'
        return value


def load(path_to_file, table):
    """Loads parcels from CSV parcel file."""

    # This method reads through the parcel file and creates a parcel 
    # object for each line in the file. It has a runtime complexity of 
    # O(N), where N is the number of lines in the parcel file.

    f = open(path_to_file, 'r', encoding='utf-8')
    content = f.readlines()

    for line in content:
        # here we are doing some string manipulation to parse out the 
        # lines in the parcel file
        split_line = line.split(',')

        # all arguments are being passed as strings
        new_parcel = Parcel(split_line[0], split_line[1], split_line[2], \
                            split_line[3], split_line[4], split_line[5], \
                            split_line[6], split_line[7].strip(), \
                            'INFORMATION RECEIVED')

        table.insert(new_parcel.id, new_parcel)