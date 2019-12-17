# C950 - Anthony Utt - autt3 - ID#000854797

"""Main entry point of the application
This file will handle the simulation of the day of package 
delivery, as well as manage the resources that are used by 
the simulation.
"""

from __future__ import print_function

import os
#from multiprocessing.process import BaseProcess as Process
#from multiprocessing.synchronize import Lock
from multiprocessing import Process, Lock, Queue
import time

from table import Table
import parcel
import graph
from truck import Truck
import loader

# IMPORTANT: IF YOU ARE USING WINDOWS, PLEASE CHANGE THE 
# VALUE OF clear_function TO "cls" INSTEAD OF "clear"!!!
clear_function = "clear"
clear = lambda: os.system(clear_function)


# The point of the following two classes is to be able to throw 
# a custom Error when the Clock class tries to enter an invalid state
class Error(Exception):
    """Base Error class that inherits from Exception"""
    # pass executes in O(1) time
    pass


class StateError(Error):
    """Error thrown when clock is sent to an invalid state"""
    # this init method executes in O(1) time
    def __init__(self, message):
        self.message = message


class Clock:
    """Clock class that handles the time keeping for the 
    Simulator class.
    """

    # The Clock class has four methods, excluding its init() method. 
    # Each of these methods are designed to simulate the passage of time 
    # during our simulation. With each call of the tick() method, the 
    # clock will update and pass the new time value on to the 
    # Simulation class, which will inform all other components of our 
    # simulation of the new current_time value so that each component 
    # can update its own state and keep the simulation synced.

    # __init__ here executes in O(1) time
    def __init__(self, start_time=800, interval=1):
        self.start_time = start_time
        self.interval = interval

        self.current_time = None
        self.running = False
        self.paused = False
    
    # because there are no loops, only a series of statements, this method
    # will run in O(1) time because only a finite number of statements will 
    # be executed
    def start(self):
        if not self.running:
            self.running = True
            if not self.paused:
                self.current_time = self.start_time
            else:
                self.paused = False
        else:
            raise StateError('Clock is already running!')
    
    # stop runs in O(1) for the same reason as above
    def stop(self):
        if self.running:
            self.running = False
            self.paused = False
        else:
            raise StateError('Clock is not running!')
    
    # tick has a finite number of statements and no loops, so it will 
    # run in O(1) time
    def tick(self):
        if self.running and not self.paused:
            self.current_time = self.current_time + self.interval
        else:
            raise StateError('Clock is not running or paused!')
        
        if str(self.current_time)[-2:] == '60':
            self.current_time = self.current_time + 40
    
    # pause runs in O(1) time
    def pause(self):
        if self.running:
            self.paused = True
        else:
            raise StateError('Clock is not running!')

# Here we initialize a few objects that we will need for the simulation
# The Queue and Lock objects will be used for syncronization between 
# our two threads to ensure the integrity of the reported data.
# The Graph and Table objects are custom data structures that have 
# been created for use with this algorithm.
q = Queue()
lock = Lock()
my_graph = graph.Graph()
my_table = Table()

# Loading nodes and parcels into memory
graph.load('node_list.csv', 'distance_list.csv', my_graph)
parcel.load('parcel_list.csv', my_table)

# Initializing our trucks
truck_1 = Truck(1, 1, hub_node=my_graph.get_node(1))
truck_2 = Truck(2, 2, hub_node=my_graph.get_node(1))
truck_3 = Truck()  # we don't have a driver for this one...

# List for holding truck objects
trucks = [truck_1, truck_2]

# This Loader object will handle sorting the parcels between 
# the trucks so that we can get an even spread on them and 
# ensure that no truck gets bogged down by too many 
# high-priority deliveries
my_loader = loader.Loader(my_table, my_graph)


class Simulator:
    """Simulator class that handles the simulation of a day of 
    package delivery. Uses Clock class to keep track of times.
    """

    # The Simulator class handles the main simulation of our 
    # day of package deliveries. This object will be created 
    # in its own child thread to handle background processing 
    # of the simulation without locking the CLI for the user. 
    # The run() and update() functions carry most of our 
    # functionality, and have higher processing times than 
    # other functions in this solution, simply because of 
    # the number of other methods that are called by them.

    # init runs in O(1)
    def __init__(self, clock):
        self.clock = clock
    
    # This method runs in O(1) time
    def get_current_time(self):
        return self.clock.current_time

    def run(self):
        self.clock.start()  #starting clock

        # This loop runs in O(N) time as it loops through 
        # each parcel in our table
        for p in my_table.items():
            p.set_node(my_graph)
            p.parse_special_instructions()
            if not p.delayed:
                p.set_status('AT HUB')

        my_loader.load()  #initializing loader
        my_loader.run([truck_1, truck_2])  #sending trucks to loader
        #truck.load(truck_3, my_table)

        # starting each truck and giving them the current_time
        truck_1.start(self.clock.current_time)
        truck_2.start(self.clock.current_time)
        #truck_3.start(self.clock.current_time)  # no driver

        # Because this is technically an infinite loop, it is 
        # impossible to define the runtime complexity of this 
        # block of code. Runtime complexity only applies to 
        # algorithms, and algorithms - by definition - must 
        # terminate. While this will eventually be terminated 
        # by the user, it is impossible to formally define when 
        # that will occur, or how many cycles will have passed 
        # by that time. With that in mind, the interior of this 
        # loop will execute in O(1) time because it is a finite 
        # number of simple statements and function calls.
        while True:
            lock.acquire()
            try:
                self.update()
            finally:
                if not q.empty():
                    q.get(False)
                total_miles = truck_1.get_total_miles() + truck_2.get_total_miles()
                q.put((self.clock.current_time, my_table, total_miles))
                lock.release()
                time.sleep(0.05)

    def update(self):
        # This method handles the bulk of the function calls and logic 
        # of the program. Overall, the method runs in O(N) time, which 
        # will be discussed in inline comments further down.

        # updating clock
        if self.clock.running:
            self.clock.tick()

        # updating trucks
        truck_1_response = truck_1.update(self.clock.current_time)
        truck_2_response = truck_2.update(self.clock.current_time)

        # checking responses from trucks
        if truck_1_response == 1:
            truck_1_response = my_loader.run([truck_1])
            truck_1.start(self.clock.current_time)
        if truck_2_response == 1:
            truck_2_response = my_loader.run([truck_2])
            truck_2.start(self.clock.current_time)

        if truck_1_response == 1:
            truck_1.finish_day()
        if truck_2_response == 1:
            truck_2.finish_day()

        # This block has a worst-case runtime of O(N)
        for p in my_table.lookup(status='INFORMATION RECEIVED'):
            if self.clock.current_time >= p.arrival_time:
                p.set_status('AT HUB')

        clear()  # clears console history to reduce clutter

        # printing information to the console to update the user
        print('Time: ' + str(self.clock.current_time))
        print()
        if not truck_1.is_finished():
            print('Truck 1 en route to ' + str(truck_1.next_node) \
                + ', will arrive at ' + str(truck_1.get_arrival_time()))
            print('Load: ' + str(truck_1.load_count()) + '/' + str(truck_1.capacity))
        else:
            print('All parcels have left the hub. Truck 1 is done for the day.')
        if not truck_2.is_finished():
            print('Truck 2 en route to ' + str(truck_2.next_node) \
                + ', will arrive at ' + str(truck_2.get_arrival_time()))
            print('Load: ' + str(truck_2.load_count()) + '/' + str(truck_2.capacity))
        else:
            print('All parcels have left the hub. Truck 2 is done for the day.')

        print('Enter 1 to pause or 0 to exit: ')


class Controller:
    """Controller class that handles a child thread and manages the 
    Simulator object that will run the package delivery simulations.
    """

    # The Controller class spawns the child thread containing the 
    # Simulator object. It also syncs up using the Queue object 
    # to ensure the integrity of our data that is being passed 
    # back and forth between the two threads. All of the methods 
    # in this class run in O(1) time because they simply call other 
    # functions from elsewhere in the program.
    def __init__(self):
        self.clock = Clock()
        self.sim = Simulator(self.clock)
        self.process = Process(target=self.sim.run, args=())

    def start(self):
        self.process.start()

    def interrupt(self):
        lock.acquire()

    def resume(self):
        lock.release()

    def cancel(self):
        self.process.terminate()

    def get_current_time(self):
        return self.sim.get_current_time()
        
# The main() function is where our program begins, as well as handling 
# input from the user. Because there is an infinite loop, it is not 
# possible to define the runtime complexity of this block of code. It
# will eventually be terminated by the user, but it is impossible to 
# estimate when that will be, after how many cycles.
def main():
    # Initializing controller object
    my_controller = Controller()
    my_controller.start()
    
    val = None  # input variable
    while True:
        val = input()

        # input options while running
        if val == '1':
            my_controller.interrupt()
            val = None
        elif val == '0':
            my_controller.cancel()
            break
        
        val = input('Enter 1 to resume, P to print all parcels,'
            + ' or 0 to exit the simulator: ')

        # input options while paused
        if val == '1':
            my_controller.resume()
            val = None
        elif val == 'P' or val == 'p':
            current_time, my_table, total_miles = q.get()
            print('Current Time: ' + str(current_time))
            my_table.print_all()
            print()
            print()
            print('Total miles: %.2f' % round(total_miles, 2))
            print()
            input('Press enter to continue the simulation.')
            my_controller.resume()
        else:
            my_controller.cancel()
            break

main()  # calling main() to begin the program

def test():
    for p in my_table.items():
        p.set_node(my_graph)
        p.parse_special_instructions()
        if not p.delayed:
            p.set_status('AT HUB')

    my_loader.load()
    my_loader.run([truck_1, truck_2])

    truck_1.start(800)
    truck_2.start(800)

    truck_1.update(801)
    truck_2.update(801)

#test()