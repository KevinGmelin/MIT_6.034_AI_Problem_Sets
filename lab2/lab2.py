# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
# ANSWER1 = True
# ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph


## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    if start == goal:
        return [start]

    agenda = [[start]]
    extended_set = {}
    while len(agenda) > 0:
        path_to_extend = agenda.pop(0)
        if path_to_extend[-1] == goal:
            return path_to_extend
        new_paths = []
        for node in graph.get_connected_nodes(path_to_extend[-1]):
            if node in path_to_extend or node in extended_set:
                continue

            extended_set[node] = True
            new_paths.append(path_to_extend + [node])
        agenda.extend(new_paths)
    return []


## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    if start == goal:
        return [start]

    agenda = [[start]]
    extended_set = {}
    while len(agenda) > 0:
        path_to_extend = agenda.pop(0)
        if path_to_extend[-1] == goal:
            return path_to_extend
        new_paths = []
        for node in graph.get_connected_nodes(path_to_extend[-1]):
            if node in path_to_extend or node in extended_set:
                continue

            extended_set[node] = True
            new_paths.append(path_to_extend + [node])
        agenda = new_paths + agenda
    return []


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    if start == goal:
        return [start]

    agenda = [[start]]
    while len(agenda) > 0:
        path_to_extend = agenda.pop(0)
        if path_to_extend[-1] == goal:
            return path_to_extend
        new_paths = []
        for node in graph.get_connected_nodes(path_to_extend[-1]):
            if node in path_to_extend:
                continue

            new_paths.append(path_to_extend + [node])
        new_paths.sort(key=lambda x: graph.get_heuristic(x[-1], goal))
        agenda = new_paths + agenda
    return []


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    if start == goal:
        return [start]

    agenda = [[start]]
    while len(agenda) > 0:
        new_agenda = []
        for path_to_extend in agenda:
            if path_to_extend[-1] == goal:
                return path_to_extend
            for node in graph.get_connected_nodes(path_to_extend[-1]):
                if node in path_to_extend:
                    continue
                new_agenda.append(path_to_extend + [node])
        new_agenda.sort(key=lambda x: graph.get_heuristic(x[-1], goal))
        agenda = new_agenda[0:beam_width]
    return []


## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    if len(node_names) == 1:
        return 0
    length = 0
    for i in range(1, len(node_names)):
        length += graph.get_edge(node_names[i - 1], node_names[i]).length
    return length


def branch_and_bound(graph, start, goal):
    if start == goal:
        return [start]

    agenda = [[start]]
    while len(agenda) > 0:
        path_to_extend = agenda.pop(0)
        if path_to_extend[-1] == goal:
            return path_to_extend
        new_paths = []
        for node in graph.get_connected_nodes(path_to_extend[-1]):
            if node in path_to_extend:
                continue
            new_paths.append(path_to_extend + [node])
        agenda.extend(new_paths)
        agenda.sort(key=lambda x: path_length(graph, x))
    return []


def a_star(graph, start, goal):
    if start == goal:
        return [start]

    agenda = [[start]]
    extended_set = {}
    while len(agenda) > 0:
        path_to_extend = agenda.pop(0)
        if path_to_extend[-1] == goal:
            return path_to_extend
        new_paths = []
        for node in graph.get_connected_nodes(path_to_extend[-1]):
            if node in path_to_extend or node in extended_set:
                continue
            extended_set[node] = True
            new_paths.append(path_to_extend + [node])
        agenda.extend(new_paths)
        agenda.sort(key=lambda x: path_length(graph, x) + graph.get_heuristic(x[-1], goal))
    return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for node in graph.nodes:
        shortest_path = a_star(graph, node, goal)
        if path_length(graph, shortest_path) < graph.get_heuristic(node, goal):
            return False
    return True


def is_consistent(graph, goal):
    for edge in graph.edges:
        h1 = graph.get_heuristic(edge.node1, goal)
        h2 = graph.get_heuristic(edge.node2, goal)
        if edge.length < abs(h1 - h2):
            return False
    return True


HOW_MANY_HOURS_THIS_PSET_TOOK = '4'
WHAT_I_FOUND_INTERESTING = 'How different search algorithms can be implemented with very similar code'
WHAT_I_FOUND_BORING = 'Nothing'
