
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2020-08-09  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search
import sokoban
import numpy as np


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

movement=[(1,0),(-1,0),(0,1),(0,-1)]

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def direction(move):
    if move == (1,0):
        return 'Right'
    if move == (-1,0):
        return "Left"
    if move == (0,1):
        return 'Down'
    if move == (0,-1):
        return 'Up'

def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag one as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    ##         "INSERT YOUR CODE HERE"
    corners=[]
    target=[]
    warehouse=warehouse.splitlines()
    nrows=len(warehouse)
    ncols=len(warehouse[0])

    # print(zero)
    # zero[:][:]=' '
    # for col,row in wall:
    #     zero[row][col]='#'
    # print(zero)

    for i in range(1,nrows-1):
        for j in range(1,ncols-1):
            if(warehouse[i][j]==' ' or warehouse[i][j]=='@'):
                if(
                    (warehouse[i][j-1]=='#' and (warehouse[i-1][j]=='#' or warehouse[i+1][j]=='#'))
                    or
                    (warehouse[i][j+1]=='#' and (warehouse[i-1][j]=='#' or warehouse[i+1][j]=='#'))):
                    corners.append((j,i))
                    line = warehouse[i]
                    warehouse[i] = line[:j]+"X"+line[j+1:]




    warehouse="\n".join(["".join(line) for line in warehouse])


    return warehouse

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    
    def __init__(self, initial,goal):

        self.initial = initial
        self.goal = goal.replace('@', ' ')
        self.cost= 1

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        warehouse = sokoban.Warehouse()
        warehouse.extract_locations(state.splitlines())
        # print(warehouse)
        # print(state)
        taboo = set(sokoban.find_2D_iterator(taboo_cells(str(warehouse)).splitlines(),"X"))
        for box in warehouse.boxes:
            for move in movement:
                worker_position = (box[0]-move[0],box[1]-move[1])
                box_after_pushed = (box[0]+move[0],box[1]+move[1])
                # print(taboo)
                if( can_go_there(warehouse,worker_position)
                    and box_after_pushed not in taboo
                    and box_after_pushed not in warehouse.walls
                    and box_after_pushed not in warehouse.boxes
                ):
                    yield (box,direction(move))




    def result(self, state, action):

        warehouse = sokoban.Warehouse()
        warehouse.extract_locations(state.splitlines())
        # print(action)

        box_position = action[0]
        action = action[1]

        box_id=warehouse.boxes.index(box_position)
        warehouse.boxes.remove(box_position)
        if action == 'Right':
            move = movement[0]
            new_box_position = (box_position[0]+move[0],box_position[1]+move[1])

        if action == "Left":
            move = movement[1]
            new_box_position = (box_position[0]+move[0],box_position[1]+move[1])

        if action == 'Down':
            move = movement[2]
            new_box_position = (box_position[0]+move[0],box_position[1]+move[1])

        if action == 'Up':
            move = movement[3]
            new_box_position = (box_position[0]+move[0], box_position[1]+move[1])

        warehouse.worker = box_position

        warehouse.boxes.insert(box_id, new_box_position)
        # print(str(warehouse))
        return str(warehouse)

    def goal_test(self, state):
        return state.replace('@', ' ') == self.goal

    def h(self,n):
        # print(node)
        # print(' ')
        # print(self.initial)
        h=0

        wh=sokoban.Warehouse()
        wh.extract_locations(n.state.splitlines())
        # print(wh.boxes)
        # print(wh.boxes)
        # print(n.state)
        for target in wh.targets:
            for box in wh.boxes:
                # print(box)
                h=manhattan_distance(box,target)+h
        return h

    def path_cost(self, c, state1, action, state2):

        # print(s)
        return c+1


    def value(self, state):
        return 1



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def Draw_Org_Map(warehouse):
    wh = str(warehouse).splitlines()

    rows = len(wh)
    cols = len(wh[0])
    map = [[' ' for j in range(cols)] for i in range(rows)]
    for wall in warehouse.walls:
        wall_col, wall_row = wall
        map[wall_row][wall_col] = '#'

    for target in warehouse.targets:
        target_col, target_row = target
        map[target_row][target_col] = '.'


    return map


def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"

    coll={
        'Left':   (-1,0),
        'Right':   (1,0),
        'Up':   (0,-1),
        'Down':   (0,1)
    }
    worker_position = warehouse.worker
    map_array=Draw_Org_Map(warehouse)

    for action in action_seq:
        move = coll[action]
        # print(worker_position)
        # print(move)
        if action=='Left':
            worker_position = (worker_position[0]+move[0],worker_position[1]+move[1])

        elif action == 'Right':
            worker_position = (worker_position[0]+move[0],worker_position[1]+move[1])

        elif action == 'Up':
            worker_position = (worker_position[0]+move[0],worker_position[1]+move[1])

        elif action == 'Down':
            worker_position = (worker_position[0]+move[0],worker_position[1]+move[1])

        if worker_position in warehouse.walls:
            return 'invaild action'

        if worker_position in warehouse.boxes:

            # print(worker_position)
            box_id = warehouse.boxes.index(worker_position)

            box_new_position = (warehouse.boxes[box_id][0]+move[0],warehouse.boxes[box_id][1]+move[1])

            if box_new_position in warehouse.boxes or box_new_position in warehouse.walls:
                return 'invaild action'
            else:
                warehouse.boxes.remove(worker_position)
                warehouse.boxes.insert(box_id,box_new_position)

        # print(worker_position)

    if (worker_position in warehouse.targets):
        map_array[worker_position[1]][worker_position[0]] = '!'
    else:
        map_array[worker_position[1]][worker_position[0]] = '@'

    for box in warehouse.boxes:
        if box in warehouse.targets:
            map_array[box[1]][box[0]]='*'
        else:
            map_array[box[1]][box[0]]='$'

    new_warehouse = "\n".join(["".join(line) for line in map_array])
    # print(new_warehouse)
    return new_warehouse
    # raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using A* graph search algorithm and elementary actions
    the puzzle defined in the parameter 'warehouse'.
    
    In this scenario, the cost of all (elementary) actions is one unit.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    macros = solve_sokoban_macro(warehouse)

    def WorkerGoal(box,direction):
        # print(direction)
        if direction == 'Right':
            move = (-1,0)
        if direction == "Left":
            move = (1,0)
        if direction == 'Down':
            move = (0,-1)
        if direction == 'Up':
            move = (0,1)
        return (box[0]+move[0],box[1]+move[1])


    if macros == 'Impossible' :
        return macros
    elif macros is None:
        return 'impossible'


    worker_movement = []
    # print(macros)
    for macro in macros[1:]:

        box = macro[0]
        direction = macro[1]
        # print(direction)
        worker_goal = WorkerGoal(box,direction)


        def heuristic(position):
            state = position.state
            # print(state,'111')
            res = manhattan_distance(state, worker_goal)
            return res

        nodes = search.astar_graph_search(WorkerPath(warehouse.worker,warehouse,worker_goal),heuristic)


        if nodes is None:
            return 'Impossible'

        # print(nodes.path())

        for node in nodes.path()[1:]:
            if node.action == (1, 0):
                move = "Right"
            elif node.action == (-1,0):
                move = "Left"
            elif node.action == (0, 1):
                move = "Down"
            elif node.action == (0, -1):
                move = "Up"
            worker_movement.append(move)

        if macro[1] == 'Left':
            base = (-1,0)
        elif macro[1] == 'Right':
            base = (1,0)
        elif macro[1] == 'Up':
            base = (0,-1)
        elif macro[1] == 'Down':
            base = (0,1)

        worker_old_position = nodes.state

        box_be_pushed = (worker_old_position[0]+base[0],worker_old_position[1]+base[1])
        box_id = warehouse.boxes.index(box_be_pushed)
        warehouse.boxes.remove(box_be_pushed)
        box_new_position= (box_be_pushed[0]+base[0], box_be_pushed[1]+base[1])
        warehouse.boxes.insert(box_id,box_new_position)
        warehouse.worker = box_be_pushed

        # print(nodes.state, 'state')
        # print(macro,'action')
        #
        # print(warehouse.worker,'woker')
        # print(warehouse.boxes,'box')


        worker_movement.append(direction)
        # print(worker_movement)

        # print(worker_movement)
    return worker_movement
    # raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    
    ##         "INSERT YOUR CODE HERE"


    # def heuristic(position):
    #     state=position.state
    #     # print(state,'111')
    #     return manhattan_distance(state,dst)

    node = search.astar_graph_search(WorkerPath(warehouse.worker,warehouse,dst))

    if node is not None:
        return True
    else:
        return False


    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using using A* algorithm and macro actions the puzzle defined in 
    the parameter 'warehouse'. 
    
    A sequence of macro actions should be represented by a list M of the form
    
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
            
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    In this scenario, the cost of all (macro) actions is one unit. 

    @param warehouse: a valid Warehouse object

    @return
        If the puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    str_warehouse = str(warehouse)
    goal = str_warehouse.replace("$", " ").replace(".", "*")

    # def heuristic(node):
    #     # print(node)
    #     # print(' ')
    #     h=0
    #     warehouse=sokoban.Warehouse()
    #     warehouse.extract_locations(node.state.splitlines())
    #     for target in warehouse.targets:
    #         for box in warehouse.boxes:
    #             h=manhattan_distance(box,target)+h
    #     return h

    macros=search.astar_graph_search(SokobanPuzzle(str_warehouse,goal))
    # print(M.path())


    if macros is None or macros=='Impossible':
        return str('Impossible')

    elif macros.path()[-1] == str_warehouse :
        return []


    else:
        actions_list = [node.action for node in macros.path()]
        # print(actions_list)
        return actions_list



    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban_elem(warehouse, push_costs):
    '''
    In this scenario, we assign a pushing cost to each box, whereas for the
    functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were 
    simply counting the number of actions (either elementary or macro) executed.
    
    When the worker is moving without pushing a box, we incur a
    cost of one unit per step. Pushing the ith box to an adjacent cell 
    now costs 'push_costs[i]'.
    
    The ith box is initially at position 'warehouse.boxes[i]'.
        
    This function should solve using A* algorithm and elementary actions
    the puzzle 'warehouse' while minimizing the total cost described above.
    
    @param 
     warehouse: a valid Warehouse object
     push_costs: list of the weights of the boxes (pushing cost)

    @return
        If puzzle cannot be solved return 'Impossible'
        If a solution exists, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    macros = solve_sokoban_macro_weight(warehouse,push_costs)

    def WorkerGoal(box, direction):
        # print(direction)
        if direction == 'Right':
            move = (-1, 0)
        if direction == "Left":
            move = (1, 0)
        if direction == 'Down':
            move = (0, -1)
        if direction == 'Up':
            move = (0, 1)
        return (box[0] + move[0], box[1] + move[1])

    if macros == 'Impossible' or macros is None:
        return 'Improssible'

    elif macros.path()[-1] == str(warehouse):
        return []



    worker_movement = []
    # print(macros)

    for macro in macros[1:]:

        box = macro[0]
        direction = macro[1]
        # print(direction)
        worker_goal = WorkerGoal(box, direction)

        def heuristic(position):
            state = position.state
            # print(state,'111')
            res = manhattan_distance(state, worker_goal)
            return res

        nodes = search.astar_graph_search(WorkerPath(warehouse.worker, warehouse, worker_goal), heuristic)

        if nodes is None:
            return 'Impossible'

        # print(nodes.path())

        for node in nodes.path()[1:]:
            if node.action == (1, 0):
                move = "Right"
            elif node.action == (-1, 0):
                move = "Left"
            elif node.action == (0, 1):
                move = "Down"
            elif node.action == (0, -1):
                move = "Up"
            worker_movement.append(move)

        if macro[1] == 'Left':
            base = (-1, 0)
        elif macro[1] == 'Right':
            base = (1, 0)
        elif macro[1] == 'Up':
            base = (0, -1)
        elif macro[1] == 'Down':
            base = (0, 1)

        worker_old_position = nodes.state

        box_be_pushed = (worker_old_position[0] + base[0], worker_old_position[1] + base[1])
        box_id = warehouse.boxes.index(box_be_pushed)
        warehouse.boxes.remove(box_be_pushed)
        box_new_position = (box_be_pushed[0] + base[0], box_be_pushed[1] + base[1])
        warehouse.boxes.insert(box_id, box_new_position)
        warehouse.worker = box_be_pushed

        # print(nodes.state, 'state')
        # print(macro,'action')
        #
        # print(warehouse.worker,'woker')
        # print(warehouse.boxes,'box')

        worker_movement.append(direction)
    return worker_movement

def solve_sokoban_macro_weight(warehouse,push_costs):

    str_warehouse = str(warehouse)
    goal = str_warehouse.replace("$", " ").replace(".", "*")

    macros = search.astar_graph_search(Weighted_sokoban(str_warehouse, goal,push_costs))

    if macros is None:
        return str('Impossible')
    elif macros.path()[-1] == str_warehouse:

        return []

    else:
        actions_list = [node.action for node in macros.path()]

        return actions_list



class WorkerPath(search.Problem):

    def __init__(self,initial,warehouse,goal=None):
        self.initial=initial
        self.warehouse=warehouse
        self.goal=goal

    def actions(self, state):
        # print(state)
        for move in movement:
            new_position=(state[0]+move[0],state[1]+move[1])
            if ((new_position not in self.warehouse.walls) and (new_position not in self.warehouse.boxes) ):
                yield move

    def result(self, state, action):
        # print(action)
        new_position = (state[0] + action[0], state[1] + action[1])
        # print(new_position)
        return new_position

    def h(self,n):
        # wh=sokoban.Warehouse()
        # wh.extract_locations(n.state)
        # print(n.state,self.goal)
        h=manhattan_distance(n.state,self.goal)
        # print(self.goal)
        return h

    def value(self, state):
        return 1

class Weighted_sokoban(search.Problem):

    def __init__(self, initial, goal,push_cost):

        self.initial = initial
        self.goal = goal.replace('@', ' ')
        self.push_cost = push_cost
        wh=sokoban.Warehouse()
        wh.extract_locations(initial.splitlines())
        self.initial_box =wh.boxes
        self.targets = wh.targets
        self.coll ={
            'Left':   (-1,0),
            'Right':   (1,0),
            'Up':   (0,-1),
            'Down':   (0,1)
        }
        self.box_push_cost = 0
    def actions(self, state):

        warehouse = sokoban.Warehouse()
        warehouse.extract_locations(state.splitlines())
        taboo = set(sokoban.find_2D_iterator(taboo_cells(str(warehouse)), "X"))
        for box in warehouse.boxes:
            for move in movement:
                worker_position = (box[0] - move[0], box[1] - move[1])
                box_after_pushed = (box[0] + move[0], box[1] + move[1])

                if (can_go_there(warehouse, worker_position)
                        and box_after_pushed not in taboo
                        and box_after_pushed not in warehouse.walls
                        and box_after_pushed not in warehouse.boxes
                ):
                    yield (box, direction(move))

    def result(self, state, action):

        warehouse = sokoban.Warehouse()
        warehouse.extract_locations(state.splitlines())


        box_position = action[0]
        action = action[1]

        box_id = warehouse.boxes.index(box_position)
        warehouse.boxes.remove(box_position)
        if action == 'Right':
            move = movement[0]
            new_box_position = (box_position[0] + move[0], box_position[1] + move[1])

        if action == "Left":
            move = movement[1]
            new_box_position = (box_position[0] + move[0], box_position[1] + move[1])

        if action == 'Down':
            move = movement[2]
            new_box_position = (box_position[0] + move[0], box_position[1] + move[1])

        if action == 'Up':
            move = movement[3]
            new_box_position = (box_position[0] + move[0], box_position[1] + move[1])

        warehouse.worker = box_position

        warehouse.boxes.insert(box_id, new_box_position)
        # print(str(warehouse))
        return str(warehouse)

    def goal_test(self, state):
        return state.replace('@', ' ') == self.goal

    # def path_cost(self, c, state1, action, state2):

    def path_cost(self, c, state1, action, state2):


        if(action[0] in self.initial_box):
            ith_box=self.initial_box.index(action[0])
            box_position = action[0]
            base=self.coll[action[1]]
            box_new_position=(box_position[0]+base[0],box_position[1]+base[1])
            self.initial_box.remove(box_position)
            self.initial_box.insert(ith_box,box_new_position)
            self.box_push_cost = self.push_cost[ith_box]

        return c+ self.box_push_cost




    def h(self, n):

        h = 0
        wh = sokoban.Warehouse()
        self.initial_box


        # print(wh.boxes)
        for target in self.targets:
            for box in self.initial_box:
                # print(box)
                ith_box = self.initial_box.index(box)
                h = (manhattan_distance(box, target)*push_cost[ith_box]) + h
        return h

    def value(self, state):
        return 1


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__=='__main__':
    puzzle_t3 = '''
    #######
    #@ $ .#
    #. $  #
    #######'''
    problem_file = "./warehouses/warehouse_03_impossible.txt"
    wh = sokoban.Warehouse()
    wh.load_warehouse(problem_file)
    push_cost=[1,10]
    # wh.extract_locations(puzzle_t1.split(sep='\n'))
    print('\nElementary solution')
    answer = solve_sokoban_elem(wh)
    print(answer)