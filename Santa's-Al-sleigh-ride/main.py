import screen_manager
from game_manager import GameManager
import sys
from PyGameInputHandler import PygameInputManager

def __main__():
    arg = sys.argv
    search_type = 'bd_bfs'
    
    if len(arg) > 1:
        if arg[1] in ['a_star', 'bd_bfs', 'ucs', 'ids']:
            search_type = arg[1]
        else:
            print('\n\nUse "a_star" or "bd_bfs" or "ucs" or "ids" as argument.')
            return
    Num = PygameInputManager.get_selected_number()
    for z in ['a_star', 'bd_bfs', 'ucs','ids']:
        print(z+" :")
        search_type = z
        game_manager = GameManager(Num)
        # Finding way
        result, depth, cost = game_manager.start_search(search_type)

        # Printing outputs
        directions = {(1, 0): 'D', (-1, 0): 'U', (0, 1): 'R', (0, -1): 'L'}
        p1 = game_manager.init_state.santa
        for i in range(len(result)):
            p2 = result[i].santa
            print(directions[(p2[0]-p1[0], p2[1]-p1[1])], end='')
            # print(p2, p1, (p2[0]-p1[0], p2[1]-p1[1]))
            p1 = result[i].santa
        print('\nTotal moves:', depth)
        print('Total cost:', cost)
        game_manager.display_states(result)


__main__()
