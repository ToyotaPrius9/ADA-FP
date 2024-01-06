import random
from collections import deque
import time
# Kenny: Added timeit and matplotlib module
import timeit
import matplotlib.pyplot as plt
import sys



class Package:

    def __init__(self, id, arrival_time, processing_time, deadline=None, weight=None): # initialize attributes of  packages
  
        self.id = id # identifier for package
       
        self.arrival_time = arrival_time # set time for when package arrives for processing
        
        self.processing_time = processing_time # set time for package processing

        self.deadline = deadline # set deadline for package processing
        
        self.weight = weight # set weight of package


class Scheduler: #for managing schedulings for packages
    
    def __init__(self): #initialize da scheduler for packages
        
        self.queue = deque() # create a double-ended deque for holding dem packages

    
    def add_package(self, package): # function to add a package to de queue
        
        self.queue.append(package) # shove in dat pack
    



#### SCHEDULING ALGORITHMS!!! #####

def fcfs_schedule(packages):
    scheduler = Scheduler()
    for package in packages:
        scheduler.add_package(package)
    end = time.time()
    return scheduler.queue

def sjn_schedule(packages):
    scheduler = Scheduler()
    packages.sort(key=lambda x: x.processing_time)
    for package in packages:
        scheduler.add_package(package)
    return scheduler.queue

def rr_schedule(packages, time_quantum):
    scheduler = Scheduler()
    package_index = 0
    current_time = 0

    while package_index < len(packages):
        current_package = packages[package_index]
        scheduler.add_package(current_package)

        current_time = max(current_time, current_package.arrival_time)
        remaining_processing_time = max(0, current_package.processing_time - time_quantum)

        if remaining_processing_time > 0:
            packages[package_index] = Package(
                current_package.id,
                current_time,
                remaining_processing_time,
                current_package.deadline,
                current_package.weight
            )
            package_index += 1  # Increment the index only if the package has remaining processing time
        else:
            package_index += 1

        current_time += min(current_package.processing_time, time_quantum)

    return scheduler.queue



def lst_schedule(packages):
    scheduler = Scheduler()
    packages.sort(key=lambda x: x.deadline - (x.arrival_time + x.processing_time))
    for package in packages:
        scheduler.add_package(package)
    return scheduler.queue

def pss_schedule(packages):
    scheduler = Scheduler()
    packages.sort(key=lambda x: (x.weight, x.id), reverse=True)
    for package in packages:
        scheduler.add_package(package)
    return scheduler.queue


### SCHEDULING ALGORITHMS END ###






# function to calculate TT
def calculate_turnaround_time(scheduled_packages): # function to calculate TT

    # create variables for turnaround time and current time
    turnaround_time = 0
    current_time = 0

    # loop through each package in de scheduled packages
    for package in scheduled_packages:
        
        current_time = max(current_time, package.arrival_time) # update current time to be the max of current and arrival time of package
        
        turnaround_time += current_time + package.processing_time - package.arrival_time # calculate TT for de current package and add it to the variable 
        
        # Update the current time to reflect the completion of the current package
        current_time += package.processing_time 

    # Calculate the average turnaround time by dividing the total turnaround time by the number of packages
    return turnaround_time / len(scheduled_packages)



#function for benchmarking wating time of package delivery
def calculate_waiting_time(scheduled_packages): 
    waiting_time = 0 # initiate variable
    current_time = 0 #initiate variable for ct

    for package in scheduled_packages:# loop packages

        # Add em in    
        current_time = max(current_time, package.arrival_time)
        waiting_time += current_time - package.arrival_time
        current_time += package.processing_time

    return waiting_time / len(scheduled_packages) # Return waiting time value, for benchmark



# Function to generate packages
def generate_packages(num_packages, max_processing_time, max_deadline=None, max_weight=None, task_type='random'): 
    packages = [] #init

    #loop for appropriate package filling
    for i in range(num_packages):
        arrival_time = random.randint(10, 10)

        if task_type == 'short': # for short tasks, assign half or less the processing time of maximum
            processing_time = random.randint(1, max_processing_time // 2)

        elif task_type == 'long': # for long tasks, assign processing time greater than half of maximum processing time
            processing_time = random.randint(max_processing_time // 2 + 5, max_processing_time )

        else: # not really used but assign processing time within the entire range of max processing time
            processing_time = random.randint(1, max_processing_time)

        
        deadline = random.randint(arrival_time + processing_time, max_deadline) if max_deadline else None # Generate random value for deadline

        weight = random.randint(1, max_weight) if max_weight else None # Generate random value for weight

        packages.append(Package(i, arrival_time, processing_time, deadline, weight)) # New package object shoved into da list!
    
    return packages 

# implement!
def run_simulation(algorithm, packages, time_quantum=None): 
       
     # If statements for appropriate action
    if algorithm == 'First Come First Serve':
        result = fcfs_schedule(packages)
        callables = lambda: result
        time_taken = timeit.timeit(callables, number=1)
        space_used = sys.getsizeof(packages) + sys.getsizeof(result)
    elif algorithm == 'Shortest Job First':
        result = sjn_schedule(packages)
        callables = lambda: result
        time_taken = timeit.timeit(callables, number=1)
        space_used = sys.getsizeof(packages) + sys.getsizeof(result)
    elif algorithm == 'Round Robin':
        result = rr_schedule(packages, time_quantum)
        callables = lambda: result
        time_taken = timeit.timeit(callables, number=1)
        space_used = sys.getsizeof(packages) + sys.getsizeof(result)
    elif algorithm == 'Least Slack Time':
        result = lst_schedule(packages)
        callables = lambda: result
        time_taken = timeit.timeit(callables, number=1)
        space_used = sys.getsizeof(packages) + sys.getsizeof(result)
    elif algorithm == 'Proportional Share Schedule':
        result = pss_schedule(packages)
        callables = lambda: result
        time_taken = timeit.timeit(callables, number=1)
        space_used = sys.getsizeof(packages) + sys.getsizeof(result)
    else:
         raise ValueError(f"Unknown algorithm: {algorithm}")

    # Variables containing appropriate functions
    turnaround_time = calculate_turnaround_time(result)
    waiting_time = calculate_waiting_time(result)

    # Return all metrics
    return result, time_taken, space_used, turnaround_time, waiting_time
    


# Print dem! final part
def print_results(algorithms, packages, time_quantum=None, task_type='random'):
    
    algorithm_runtimes = {}
    for algorithm in algorithms: # Loop algorithms to perform each of dem
        (
            scheduled_packages, 
            time_taken, 
            space_used,
            turnaround_time, 
            waiting_time,  

        ) = run_simulation(algorithm, packages, time_quantum)

        algorithm_runtimes[algorithm] = time_taken


        # PRINT SPAAMMMMM!!!
        print(f"Algorithm: {algorithm}")
        print(f"Task Type: {task_type}")
        print(f"Scheduled Packages: {[package.id for package in scheduled_packages]}")
        print(f"Average Turnaround Time: {turnaround_time:.2f}")
        print(f"Average Waiting Time: {waiting_time:.2f}")
        print(f"Time Taken: {time_taken:.8f}")
        print(f"Space Used: {space_used}")      
        print()

    return algorithm_runtimes

if __name__ == "__main__": # heard doing this particular line/chantra is good practice, so  eh, why not?

    # settings
    num_packages = 10
    max_processing_time = 10
    max_deadline = 20
    max_weight = 5
    time_quantum = 2
    algorithms = ['First Come First Serve', 'Shortest Job First', 'Round Robin', 'Least Slack Time', 'Proportional Share Schedule']

    # Generate and print results for short tasks
    short_packages = generate_packages(num_packages, max_processing_time, max_deadline, max_weight, task_type='short')
    short_algorithm_runtimes = print_results(algorithms, short_packages, time_quantum, task_type='short')
    # Seperator line
    print("\n------------------------------------------------------------------------------------------------------------------------------\n------------------------------------------------------------------------------------------------------------------------------\n\n")
    # Generate and print results for long tasks
    long_packages = generate_packages(num_packages, max_processing_time, max_deadline, max_weight, task_type='long')
    long_algorithm_runtimes = print_results(algorithms, long_packages, time_quantum, task_type='long')

    for algorithm in algorithms:
        plt.scatter(['Short', 'Long'], [short_algorithm_runtimes['First Come First Serve'], long_algorithm_runtimes['First Come First Serve']], label=algorithm)
        plt.xlabel('Package Type')
        plt.ylabel('Runtime (seconds)')
        plt.ylim((0, 0.000001))
        plt.title(str(algorithm))
        plt.show()
