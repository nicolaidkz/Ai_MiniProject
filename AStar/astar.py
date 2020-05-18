class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, goal):
    start_node = Node(None, start)
    start_node.f = start_node.g = start_node.h = 0
    goal_node = Node(None, goal)
    goal_node.f = goal_node.g = goal_node.h = 0

    # open list is the possible nodes to choose, but not necessarily the one chosen in the first place
    # these values are saved for revisiting
    # closed list is so that the agent does not unnecessarily backtrack and gets stuck i suppose
    # the closed list needs to be 'purged' when the agent reaches its goal so it can start over
    open_list = []
    closed_list = []

    # start node
    open_list.append(start_node)

    # loop until goal is found
    # get current node with the lowest f value
    # remove current node from open list and place into closed list
    # if current node == goal, grats, now create the path, reach goal and reset somehow

    while len(open_list) > 0:
        current_node = open_list[]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)

        #found goal?
        if current_node == goal_node:
            path = []
            current = current_node


    # tell how to pathfind i.e children nodes (if 8 nodes are available)
    # (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)
    # are the tiles walkable?
    # what about the costs?
        children[]
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0),
                             (-1, -1), (-1, 1), (1, -1), (1, 1)]
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])

    # this is how to calculate f = g + h (read about it in latex) we can use this
           child.g = current_node.g + 1
           child.h = ((child.position[0] - goal_node.position[0]) ** 2)\
                     + ((child.position[1] - goal_node.position[1]) ** 2)
           child.f = child.g + child.h

def main():

    # incomplete
    # maze can be written here manually, or inserted by some other means
    maze = []
    start = ()
    goal = ()
    path = astar(maze, start, goal)
    # send path data to agents

if __name__ == '__main__':
    main()