
# Q1 Lab1-Land Trading application

class Hello:
    def hello():
        a = 10
        print(Hello)


'''
import math
import pandas as pd 

class Land:
    def __init__(self,land_owner_id,land_owner_name,acre_of_land=0,amount=0):
        self.land_owner_id=land_owner_id
        self.land_owner_name=land_owner_name
        self.acre_of_land=acre_of_land
        self.amount=amount

    def getLandId(self):
        return self.land_owner_id
    def setLandId(self,ownerid):
        self.land_owner_id=ownerid

    def getLandName(self):
        return self.land_owner_name
    def setLandName(self,name):
        self.land_owner_name=name


    def getAcre(self):
        return self.acre_of_land
    def setAcre(self,acreland):
        self.acre_of_land=acreland

    def getAmount(self):
        return self.amount
    def setAmount(self,amount1):
        self.amount=amount1

    def sellLand(self,sell,land_quantity,price):
        self.acre_of_land-=land_quantity
        sell.acre_of_land+=land_quantity
        self.amount+=price
        sell.amount-=price
        return sell
        

    def UserDetails(self,land_owner_id,land_owner_name,acre_of_land,amount):
        print("_______________________________________")
        print("Owner Id:",self.land_owner_id)
        print("Owner Name:",self.land_owner_name)
        print("Total Land:",self.acre_of_land)
        print("Amount:",self.amount)
print("Owner 1")        
print("*********************************************")     
id1=input("Enter Owner ID:")
name1=input("Enter Owner Name:")
land=int(input("Enter Owner Total Land:"))
amount=int(input("Enter Owner Total amount:"))
l1=Land(id1,name1,land,amount)
print("Owner 2")        
print("*********************************************")   
id2=input("Enter Owner ID:")
name2=input("Enter Owner Name:")
land2=int(input("Enter Owner Total Land:"))
amount2=int(input("Enter Owner Total amount:"))
print("*********************************************")  
l2=Land(id2,name2,land2,amount2)
l1.UserDetails(id1,name1,land,amount)
l2.UserDetails(id1,name1,land,amount)

print("Land Trading")
l2=l1.sellLand(l2,int(input("\nEnter land size to sell:")),int(input("Enter price per acre:")))

print("After Trading")
l1.UserDetails(id1,name1,land,amount)
l2.UserDetails(id1,name1,land,amount)

        
    
                  



'''

# ************************************************************************************************************************
# Q2 Lab2-QueueOOP

'''
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)

    def peek(self):
        if not self.is_empty():
            return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def display(self):
        return self.items


q = Queue()
while(1):
    print("____________________________________________")
    print("1.Add element in Queue:")
    print("2.Enqueue")
    print("3.Size of the Queue:")
    print("4.Check if Queue is empty or not:")
    print("5.Display the Queue")
    print("6.Exit")
    print("____________________________________________")
    n = input("Enter your option:")

    if int(n) == 1:
        m = int(input("Enter the element to add in list:"))
        q.enqueue(m)
    elif int(n) == 2:
        print("The Element that is Enqueued:", q.dequeue())
    elif int(n) == 3:
        print("The Size of the Queue:", q.size())
    elif int(n) == 4:
        print("Check if Queue is empty:", q.is_empty())
    elif int(n) == 5:
        print("Display the Queue:", q.display())
    elif int(n) == 6:
        exit(0)
    else:
        print("Invalid Input!!!")


'''

# ************************************************************************************************************************
# Q2 Lab2-StackOOP

'''
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def display(self):
        return self.items


s = Stack()
while(1):
    print("*************************************************")
    print("____________________________________________")
    print("1. Add element in stack:")
    print("2. Pop")
    print("3.Size of the Stack:")
    print("4.Check if Stack is empty or not:")
    print("5.Display the Stack")
    print("5.Enter Other any Digit for Exit")

    n = int(input("Enter your option:"))
    print("____________________________________________")
    if n == 1:
        m = int(input("Enter the element to add in list:"))
        s.push(m)
    elif n == 2:
        print("The Element that popped is:", s.pop())
    elif n == 3:
        print("The Size of the Stack:", s.size())
    elif n == 4:
        print("Check if stack is empty:", s.is_empty())
    elif n == 5:
        print("Display the stack:", s.display())
    else:
        exit(0)

'''

# ************************************************************************************************************************
# Q3 Lab3-bfs
'''

class Search:
    def __init__(self):
        self.list1 = {}

    def add_vertex(self, vertex):
        if vertex not in self.list1:
            self.list1[vertex] = []

    def add_edge(self, vertex1, vertex2):
        self.list1[vertex1].append(vertex2)
        self.list1[vertex2].append(vertex1)

    def BFS(self, start_vertex):
        visited = []
        queue = [start_vertex]

        while queue:
            current_vertex = queue.pop(0)
            if current_vertex not in visited:
                visited.append(current_vertex)
                for neighbor in self.list1[current_vertex]:
                    queue.append(neighbor)

        return visited


g = Search()
g.add_vertex("1")
g.add_vertex("2")
g.add_vertex("3")
g.add_vertex("4")
g.add_vertex("5")
g.add_vertex("5")
g.add_edge("1", "2")
g.add_edge("3", "4")
g.add_edge("1", "5")
g.add_edge("2", "3")

print("Visited Node are:", g.BFS("1"))


'''

# ************************************************************************************************************************
# Q4 Lab4_Uniform_Cost

# ************** Type 1 to performe ******************


'''

import heapq
class Node:
    def __init__(self, name, cost, parent=None):
        self.name = name
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost


class UCS:
    def __init__(self, start, goal, graph):
        self.start = start
        self.goal = goal
        self.graph = graph
        self.visited = []
        self.queue = []
        heapq.heappush(self.queue, (0, self.start))

    def search(self):
        while len(self.queue) > 0:
            (cost, node) = heapq.heappop(self.queue)
            if node.name in self.visited:
                continue
            self.visited.append(node.name)
            if node.name == self.goal:
                return node
            for child in self.graph[node.name]:
                child_node = Node(child[0], cost + child[1], node)
                heapq.heappush(self.queue, (child_node.cost, child_node))
        return None


graph = {
    "A": [("B", 5), ("C", 6)],
    "B": [("D", 8), ("E", 7), ("F", 9)],
    "C": [("G", 7), ("H", 10)],
    "D": [("I", 3)],
    "E": [("I", 2)],
    "F": [("I", 1)],
    "G": [("I", 3)],
    "H": [("I", 2)],
    "I": []
}
start = Node("A", 0)
goal = "I"
ucs = UCS(start, goal, graph)
result = ucs.search()
if result:
    print("Goal node reached with cost", result.cost)
else:
    print("Goal not reached")


'''

# ************************************************************************************************************************
# Q4 Lab4_2-Uniform_Cost

# ************** Type 2 to performe ******************


'''

import queue
def uniform_cost_search(start, goal, graph):
    q = queue.PriorityQueue()
    q.put((0, start))
    visited = set()
    parent = {start: None}

    while not q.empty():
        cost, node = q.get()

        if node in visited:
            continue

        visited.add(node)

        if node == goal:
            return path(parent, start, goal)

        for neighbor, edge_cost in graph[node].items():
            if neighbor not in visited:
                new_cost = cost + edge_cost
                q.put((new_cost, neighbor))
                parent[neighbor] = node

    return None


def path(parent, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


graph = {
    "Vadodara": {"Ahmedabad": 105, "Godhara": 80, "Bharuch": 75},
    "Ahmedabad": {"Udaipur": 130},
    "Godhara": {"Dahod": 30},
    "Bharuch": {"Indore": 250},
    "Dahod": {"Udaipur": 80, "Mandsaur": 120},
    "Udaipur": {"Chittorgarh": 70},
    "Indore": {"Gwalior": 105},
    "Mandsaur": {"Kota": 130},
    "Chittorgarh": {"Kota": 90, "Bhilwara": 100},
    "Kota": {"Jaipur": 140},
    "Gwalior": {"Jaipur": 160, "Agra": 180},
    "Bhilwara": {"Jaipur": 30},
    "Jaipur": {"New Delhi": 150},
    "Agra": {"New Delhi": 160},
    "New Delhi": {}
}

start = "Vadodara"
goal = "New Delhi"
path = uniform_cost_search(start, goal, graph)

print("The Shortest Path from {} to {}: {}".format(start, goal, path))


'''
# ************************************************************************************************************************
# Q5 Lab5-Astar

'''
def astar(graph, start, goal):
    path = []
    pq = [[0, 0, 0, start]]
    visited = []
    while pq:
        f, h, g, cnode = pq.pop(0)
        visited.append([f, h, g, cnode])

        if cnode[-1] == goal:
            path = cnode
            break
        for neigh, wt in graph[cnode[-1]].items():
            g1 = g + wt[0]
            f1 = g1 + wt[1]
            path1 = list(cnode)
            path1.append(neigh)
            pq.append([f1, wt[1], g1, path1])
            pq = sorted(pq)

    return path, f


graph = {
    'Vadodara': {'Godhara': [3, 9], 'Kevadia': [3, 10], 'Chhoata_Udaypur': [4, 12]},
    'Godhara': {'Dahod': [3, 6], 'Jhambua': [2, 5]},
    'Dahod': {'Ujjain': [5, 4]},
    'Ujjain': {'Indore': [2, 0]},
    'Jhambua': {'Dhar': [2, 3]},
    'Dhar': {'Indore': [2, 0]},
    'Kevadia': {'Barwama': [6, 8]},
    'Barwama': {'Indore': [8, 0]},
    'Chhoata_Udaypur': {'Khargoon': [9, 9]},
    'Khargoon': {'Indore': [9, 0]},
    'Indore': {}
}
start = ['Vadodara']
goal = 'Indore'
path, cost = astar(graph, start, goal)
print("The shortest route to reach ", goal, "is", path, "with a cost of", cost, "Units")
      
'''
# ************************************************************************************************************************
# Q6 Lab6-Probability
"""
import pandas as pd
df = pd.read_excel('rainy.xlsx')
total = 30
pj = df.apply(lambda x: x["cloudy day in a month"] /
              total, axis=1)
pp = df.apply(lambda x: x["Rainy day in a month"] /
              total, axis=1)
jp = df.apply(
    lambda x: x["cloudy and rainy days in a month"]/total, axis=1)
df["prob_cloud"] = pj
df["prob_rain"] = pp
df["prob_cloud_and_rain"] = jp
cp = df.apply(lambda x: x["prob_cloud_and_rain"] /
              x["prob_rain"], axis=1)
df["cond_rain_given_cloud"] = cp
cj = df.apply(lambda x: x["prob_cloud_and_rain"] /
              x["prob_cloud"], axis=1)
df["cond_cloud_given_rain"] = cj
bay = df.apply(lambda x: x["cond_cloud_given_rain"]
               * x["prob_cloud"]/x["prob_rain"], axis=1)
df["bayesian cloud given rain"] = bay
print(df)
df.to_csv("new.csv")
"""


# *
# **
# *********
# **************

# ************************************************************************************************************************

# $$$$$$$$$$$$$$$$$$$$$ Jaydeep Sir Program $$$$$$$$$$$$$$$$$$$$$

# ************************************************************************************************************************

# Astar 03

"""# updated A* impl (completed)
def astar(graph, start, goal):
    pq = [[0, 0, 0, start]]  # a queue which store [f,h,g,node] as single unit
    visited = []
    while pq:
        f, h, g, cnode = pq.pop(0)
        visited.append([f, h, g, cnode])

        # Iterate through the neighbors of the current node
        for neigh, wt in graph[cnode[-1]].items():  # wt[0] has g, wt1 has h
            g1 = g+wt[0]
            f1 = g1+wt[1]
            path = cnode+neigh
            pq.append([f1, wt[1], g1, path])
            pq = sorted(pq)
    # Below code extracts path with goal nodes
    visitedf = []
    for x in visited:
        if x[3].endswith(goal):
            visitedf.append(x)
    print(visited)
    print("~~~~~~~~~~~~~~~~~~~~~~~")

    return sorted(visitedf)


# graph = {
#     'A': {'B': [2,3], 'C': [1,6]},
#     'B': {'D': [4,0]},
#     'C': {'D': [7,0]},
#     'D': {}
# }
# Write a program to find best path using A* algorithm
# for below graph
graph = {
    'A': {'B': [3, 8], 'C': [2, 9]},
    'B': {'D': [3, 7], 'E': [4, 6]},
    'C': {'F': [5, 4]},
    'D': {'G': [6, 0]},
    'E': {'G': [9, 0]},
    'F': {'G': [6, 0]},
    'G': {}
}
start = 'A'
goal = 'G'
visitedf = (astar(graph, start, goal))
print("The shortest Path is ", visitedf[0][-1],
      " with a cost of ", visitedf[0][-2], " Units")
"""


# ************************************************************************************************************************

#  2. bestfirst1

"""#Best First Search using Priority Queue - Finalized
from queue import PriorityQueue

graph = {
'A':{'B':12, 'C':4}, #heuristic value A to H is 13, B to H is 12, C to H is 4
'B':{'D':7, 'E':3},#heuristic value D to H is 7, E to H is 3
'C':{'F':8, 'G':2},#heuristic value F to H is 8, E to G is 2
'D':{},
'E':{'H':0},
'F':{'H':0},
'G':{'H':0}
}   

visited = [] # List for visited nodes.

def bestFirstSearch(graph, node, goal): #function for BFS
  visited.append(node)
  
  while True:          
    tn=node
    if(tn==goal):
        break
    pq=PriorityQueue()
    for neighbour,weight in graph[tn].items():  
        pq.put([weight,neighbour])
    
    if neighbour not in visited:
        tw,tn=pq.queue[0] #only high priority value added to visited
        visited.append(tn)   
        node=tn
         
  print("Visited ",visited)#out of while loop

# Driver Code
print("Following is the Best First Search")
bestFirstSearch(graph,'A', 'H')    # A is start state and G is a goal node
"""

# ************************************************************************************************************************
# 03  bfs1
"""graph = {
    '6': ['4', '8'],
    '4': ['3', '5'],
    '8': ['9'],
    '3': [],
    '5': ['9'],
    '9': []
}

visited = []  # List for visited nodes.
queue = []  # Initialize a queue


def bfs(visited, graph, node):  # function for BFS
    queue.append(node)
    visited.append(node)

    while queue:
        m = queue.pop(0)

        for child in graph[m]:  # accessing child or successors
            if child not in visited:  # take care about duplicate entries from multiple paths in a graph
                queue.append(child)
                visited.append(child)

    print("Visited ", visited)  # out of while loop


# Driver Code
print("Following is the Breadth-First Search")
bfs(visited, graph, '6')    # 6 is start state
"""

# ************************************************************************************************************************

# 04 con_prob

"""
df = pd.read_csv('prob.csv')
total = 50
pj = df.apply(lambda x: x["job_at_campus"]/total, axis=1)
pp = df.apply(lambda x: x["learnt_python"]/total, axis=1)
jp = df.apply(lambda x: x["learnt_python_and_job"]/total, axis=1)
df["prob_job"] = pj  # adds columns in pandas dataframe
df["prob_py"] = pp
df["prob_job_and_py"] = jp
cp = df.apply(lambda x: x["prob_job_and_py"]/x["prob_py"], axis=1)
df["cond_job_given_py"] = cp
cj = df.apply(lambda x: x["prob_job_and_py"]/x["prob_job"], axis=1)
df["cond_py_given_job"] = cj
bay = df.apply(lambda x: x["cond_py_given_job"] *
               x["prob_job"]/x["prob_py"], axis=1)
df["bayesian JOb given PYthon"] = bay
print(df)
df.to_csv("new.csv")

"""


# ************************************************************************************************************************

# 05 DFS_01
"""
graph = {
    '5': ['3', '7'],
    '3': ['2', '4'],
    '7': ['8'],
    '2': [],
    '4': [],  # '4' : ['8'],
    '8': []
}

visited = list()  # Set to keep track of visited nodes of graph.


def dfs(visited, graph, node):  # function for dfs
    if node not in visited:
        visited.append(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)


# Driver Code
print("Depth-First Search")
dfs(visited, graph, '5')
print(visited)
"""

# ************************************************************************************************************************

# 06 DFS 02
"""
graph = {
    '6': ['4', '8'],
    '4': ['3', '5'],
    '8': ['9'],
    '3': [],
    '5': ['9'],
    '9': []
}  # dictionary

visited = []  # List for visited nodes.
stack = []  # Initialize a stack


def dfs(visited, graph, node):
    stack.insert(0, node)

    while stack:
        m = stack.pop(0)
        visited.append(m)

        for child in graph[m]:  # accessing child or successors and adding them to stack
            if child not in visited:
                stack.insert(0, child)

    print("Visited ", visited)  # out of while loop


# Driver Code
print("Following is the Depth-First Search")
dfs(visited, graph, '6')    # 6 is start state

"""


# ************************************************************************************************************************
# 07 uniformcost
"""
# updated UCS (completed)
def ucs(graph, start, goal):
    pq = [[0, start]]  # a queue which store [f,h,g,node] as single unit
    visited = []
    while pq:
        g, cnode = pq.pop(0)
        visited.append([g, cnode])
        # Iterate through the neighbors of the current node
        for neigh, wt in graph[cnode[-1]].items():  # wt[0] has g, wt1 has h
            g1 = g+wt
            path = cnode+neigh
            pq.append([g1, path])
            pq = sorted(pq)
    # Below code extracts path with goal nodes
    visitedf = []
    for x in visited:
        if x[1].endswith(goal):
            visitedf.append(x)
    print(visited)
    print("~~~~~~~~~~~~~~~~~~~~~~~")

    return sorted(visitedf)


# graph = {
#     'A': {'B': [2,3], 'C': [1,6]},
#     'B': {'D': [4,0]},
#     'C': {'D': [7,0]},
#     'D': {}
# }
graph = {
    'A': {'B': 3, 'C': 2},
    'B': {'D': 4, 'E': 5},
    'C': {'F': 1},
    'D': {'G': 3},
    'E': {'G': 1},
    'F': {'G': 1},
    'G': {}
}
start = 'A'
goal = 'G'

visitedf = (ucs(graph, start, goal))
print("The shortest Path is ", visitedf[0][-1],
      " with a cost of ", visitedf[0][-2], " Units")


"""
