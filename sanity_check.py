
'''

Quick "sanity check" script to test your submission 'mySokobanSolver.py'

This is not an exhaustive test program. It is only intended to catch some major
blunders!

You should design your own test cases and write your own test functions.

Although a different script (with different inputs) will be used for 
marking your code, make sure that your code runs without errors with this script.


'''


from sokoban import Warehouse

#from mySokobanSolver import my_team, taboo_cells, SokobanPuzzle, check_elem_action_seq
#from mySokobanSolver import (solve_sokoban_elem, can_go_there, 
#                               solve_sokoban_macro, solve_weighted_sokoban_elem )

from fredSokobanSolver import my_team, taboo_cells, SokobanPuzzle, check_elem_action_seq
from fredSokobanSolver import (solve_sokoban_elem, can_go_there, 
                               solve_sokoban_macro, solve_weighted_sokoban_elem )


    
def test_taboo_cells():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")
    expected_answer = '####  \n#X #  \n#  ###\n#   X#\n#   X#\n#XX###\n####  '
    answer = taboo_cells(wh)
    fcn = test_taboo_cells    
    print('<<  Testing {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        


def test_check_elem_action_seq():
    wh = Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")
    # first test
    answer = check_elem_action_seq(wh, ['Right', 'Right','Down'])
    expected_answer = '####  \n# .#  \n#  ###\n#*   #\n#  $@#\n#  ###\n####  '
    fcn = test_check_elem_action_seq    
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # second test
    answer = check_elem_action_seq(wh, ['Right', 'Right','Right'])
    expected_answer = 'Impossible'
    fcn = test_check_elem_action_seq    
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)



def test_solve_sokoban_elem():
    puzzle_t1 ='#######\n#@ $. #\n#######'
    wh = Warehouse()    
    wh.from_string(puzzle_t1)
    # first test
    answer = solve_sokoban_elem(wh)
    expected_answer = ['Right', 'Right']
    fcn = test_solve_sokoban_elem
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # second test
    puzzle_t2 ='#######\n#@ $ #.#\n#######'
    wh = Warehouse()
    wh.from_string(puzzle_t2)    
    # second test
    answer = solve_sokoban_elem(wh)
    expected_answer = 'Impossible'
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        

def test_can_go_there():
    puzzle_t1 ='#######\n#@ $. #\n#######'
    wh = Warehouse()    
    wh.extract_locations(puzzle_t1.split(sep='\n'))
    # first test
    answer = can_go_there(wh,(1,2))
    expected_answer = True
    fcn = test_can_go_there
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
    # second test
    answer = can_go_there(wh,(1,5))
    expected_answer = False
    print('<<  Second test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)

  
def test_solve_sokoban_macro():
    puzzle_t2 ='#######\n#@ $ .#\n#######'
    wh = Warehouse()    
    wh.from_string(puzzle_t2)
    # first test
    answer=solve_sokoban_macro(wh)
    expected_answer = [((1, 3), 'Right'), ((1, 4), 'Right')]
    fcn = test_solve_sokoban_macro
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' passed!  :-)\n')
    else:
        print(fcn.__name__, ' failed!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)


def test_solve_weighted_sokoban_elem():
    wh = Warehouse()    
    wh.load_warehouse( "./warehouses/cab320_warehouse_8.txt")
    # first test
    answer=solve_weighted_sokoban_elem(wh, [1,9])

    expected_answer = ['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 
                       'Down', 'Right', 'Right', 'Right', 'Up', 'Left', 'Up', 
                       'Left', 'Down', 'Right', 'Down', 'Left', 'Right', 
                       'Right', 'Right', 'Right', 'Right', 'Right', 'Right']
    fcn = test_solve_weighted_sokoban_elem
    print('<<  First test of {} >>'.format(fcn.__name__))
    if answer==expected_answer:
        print(fcn.__name__, ' answer as expected!  :-)\n')
    else:
        print(fcn.__name__, ' different answer!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        print('Your answer is different but it might still be correct')
        print('Check that you pushed the right box onto the left target!')
        
    

if __name__ == "__main__":
    pass    
#    print(my_team())  # should print your team

    test_taboo_cells() 
#    test_check_elem_action_seq()
#    test_solve_sokoban_elem()
#    test_can_go_there()
#    test_solve_sokoban_macro()   
    test_solve_weighted_sokoban_elem()
