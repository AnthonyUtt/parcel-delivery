# C950 - Anthony Utt - autt3 - ID#000854797

class Table:
    # init method with default value for table size
    def __init__(self, table_size=10):
        self.table = []

        # While this is technically a two-dimensional list, it serves
        # its purpose as a table here. The hash() built-in method
        # will ensure that we are as efficient as possible. The largest
        # time commitment is going to be finding the item in the bucket
        # after the hash() function runs. It will have O(N) runtime,
        # where N is the number of items in the bucket. For a faster 
        # runtime at the expense of greater memory requirements, you
        # could increase the number of buckets with the table_size 
        # parameter.
        for i in range(table_size):
            self.table.append([])

    def insert(self, key, item):
        # Assuming that the key doesn't exist until we find a match. We
        # want to update the entry if the key exists, otherwise we add
        # a new entry to the table.
        key_exists = False
        bucket_index = hash(key) % len(self.table)
        bucket = self.table[bucket_index]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                key_exists = True
                break
        if key_exists:
            bucket[i] = ((key, item))
        else:
            bucket.append((key, item))

    def get(self, key):
        # Here, we hash the key and then perform a linear search on the
        # bucket to find the item that we want. This section has an O(N)
        # runtime where N is the number of items in the bucket. Because
        # of the nature of hash tables, this should only impose on the
        # overall runtime of the application by a negligible amount.
        bucket_index = hash(key) % len(self.table)
        bucket = self.table[bucket_index]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                return v

    def lookup(self, id_=None, address=None, city=None, state=None, \
                zip_=None, mass=None, delivery_node=None, status=None, \
                deadline=None):

            # This method is the lookup method that functions similarly to 
            # a table in a database. Any of the inputs to the method can be 
            # used, but none of them are required. The function returns a 
            # list of items that meet all of the criteria given by the inputs.
            # This method loops through every item in the table, so it has a
            # worst-case runtime complexity of O(N).
            items_to_return = []
            
            # checking inputs
            id_required = id_ is not None
            address_required = address is not None
            city_required = city is not None
            state_required = state is not None
            zip_required = zip_ is not None
            mass_required = mass is not None
            node_required = delivery_node is not None
            status_required = status is not None
            deadline_required = deadline is not None

            for bucket in self.table:  # looping through table contents
                for kv in bucket:
                    k, item = kv
                    include = True

                    # checking attributes based on inputs. We use 'and' 
                    # for all of these checks because we only want to 
                    # return items that meet ALL of the input criteria
                    if id_required:
                        if type(id_) is int:
                            include = include and item.id == id_
                        elif type(id_) is str:
                            split = id_.split(',')
                            for word in split:
                                include = include and item.id == int(word)
                        else:
                            pass
                    if address_required:
                        include = include and item.address == address
                    if city_required:
                        include = include and item.city == city
                    if state_required:
                        include = include and item.state == state
                    if zip_required:
                        include = include and item.zip == zip_
                    if mass_required:
                        include = include and item.mass == mass
                    if node_required:
                        include = include and item.delivery_node \
                            is delivery_node
                    if status_required:
                        split = status.split(',')
                        for word in split:
                            if word[0:1] == '-':
                                include = include and word[1:] not in \
                                    item.status
                            else:
                                include = include and word in item.status
                    
                    if deadline_required:
                        if deadline == "None":
                            include = include and item.delivery_deadline is None
                        elif deadline == "not None":
                            include = include and item.delivery_deadline is not None
                        else:
                            include = include and item.delivery_deadline == deadline
                    

                    #adding item to output list if it meets all criteria
                    if include:
                        items_to_return.append(item)
            
            return items_to_return

    def remove(self, key):
        # This method loops through each item in the table to find a 
        # match for the specified key. If a match is found, it removes 
        # that item from the table. This method has a runtime complexity
        # of O(N).
        key_exists = False
        bucket_index = hash(key) % len(self.table)
        bucket = self.table[bucket_index]
        for i, kv in enumerate(bucket):
            k, v = kv
            if key == k:
                key_exists = True
                break

        if key_exists:
            del bucket[i]

    def items(self):
        # This method loops through each item in the table and returns 
        # a list of all items. It has a runtime complexity of O(N)
        items = []

        for bucket in self.table:
            for kv in bucket:
                k, item = kv
                items.append(item)

        return items

    def print_all(self):
        # This method loops through all the items in the table and prints
        # the string value of each item. It has a runtime complexity of
        # O(N).
        items = self.items()

        for i in range(0, len(items), 2):
            print(str(items[i]) + '\t\t' + str(items[i+1]))