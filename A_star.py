import numpy as np

# define the possible movements
delta = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

# define the heuristic function
def heuristic(a, b):
    return min (np.abs(a[0] - b[0]), np.abs(a[1] - b[1]))*(np.sqrt(2)-1) + max (np.abs(a[0] - b[0]), np.abs(a[1] - b[1]))

# function to get the path from the came_from dict
def get_path(came_from, start, end):
    current = end
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# function to perform the A* search
def A_star(grid, start, end):
    # create the closed set
    closed_set = set()
    # create the open set
    open_set = {start}
    # create the came_from dict
    came_from = {}
    # create the g_score dict and set the g_score for the start position to 0
    g_score = {start: 0}
    # create the f_score dict and set the f_score for the start position using the heuristic function
    f_score = {start: heuristic(start, end)}

    sequence = list()

    # loop until the open set is empty
    while open_set:
        # get the position with the lowest f_score
        current = min(open_set, key=lambda x: f_score[x])
        temp_set = list()
        for cell in open_set:
            if (f_score[cell]==f_score[current]):
                temp_set.append(cell)
        current = min (temp_set,key=lambda x: f_score[x]-g_score[x] )

        sequence.append((current,dict()))
        # if the current position is the end position, return the path
        if current == end:
            return get_path(came_from, start, end), closed_set.union(open_set), sequence
        # remove the current position from the open set and add it to the closed set
        open_set.remove(current)
        closed_set.add(current)
        # iterate over the possible movements
        for move in delta:
            # calculate the new position
            next = (current[0] + move[0], current[1] + move[1])
            # if the new position is out of bounds or is an obstacle, skip it
            if next[0] < 0 or next[0] >= grid.shape[0] or next[1] < 0 or next[1] >= grid.shape[1] or grid[next[0], next[1]] == 1:
                continue
            # if the new position is already in the closed set, skip it
            if next in closed_set:
                continue
            # calculate the tentative g_score for the new position
            if (abs(move[0])+abs(move[1]))==1:
                tentative_g_score = g_score[current] + 1
            else:
                tentative_g_score = g_score[current] + np.sqrt(2)
            # if the new position is not in the open set, add it to the open set
            if next not in open_set:
                open_set.add(next)
            # if the tentative g_score is not lower than the current g_score for the new position, skip it
            elif tentative_g_score >= g_score[next]:
                continue
            # update the came_from, g_score, and f_score values for the new position
            came_from[next] = current
            g_score[next] = tentative_g_score
            f_score[next] = tentative_g_score + heuristic(next, end)
            sequence[len(sequence)-1][1][next] = (g_score[next],f_score[next])
    # if the open set is empty, return an empty path
    return None, closed_set.union(open_set), sequence