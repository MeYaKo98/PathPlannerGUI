import numpy as np

# define the possible movements
delta = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

# function to get the path from the came_from dict
def get_path(came_from, start, end):
    current = end
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# function to perform the flood search
def flood_fill(grid, start, end):
    # create the closed set
    closed_set = set()
    # create the open set
    open_set = {start}
    # create the came_from dict
    came_from = {}
    # create the score dict and set the score for the start position to 0
    score = {start: 0}

    sequence = list()

    # loop until the open set is empty
    while open_set:
        
        next_set = set()
        sequence.append(dict())
        
        while open_set:

            # remove the current position from the open set and add it to the closed set
            current = open_set.pop()
            closed_set.add(current)        
            
            if current == end:
                return get_path(came_from, start, end), closed_set.union(open_set), sequence
            
            # iterate over the possible movements
            for move in delta:
                # calculate the new position
                next = (current[0] + move[0], current[1] + move[1])
                # if the new position is out of bounds or is an obstacle, skip it
                if next[0] < 0 or next[0] >= grid.shape[0] or next[1] < 0 or next[1] >= grid.shape[1] or grid[next[0], next[1]] == 1:
                    continue
                # if the new position is already reached, skip it
                if next in closed_set or next in open_set:
                    continue
                # calculate the tentative score for the new position
                if (abs(move[0])+abs(move[1]))==1:
                    tentative_score = score[current] + 1
                else:
                    tentative_score = score[current] + np.sqrt(2)
                # if the new position is not in the next set, add it to the nex set
                if (next not in next_set):
                    next_set.add(next)
                # if the tentative score is not lower than the current score for the new position, skip it
                elif tentative_score >= score[next]:
                    continue
        
                # update the came_from, g_score, and f_score values for the new position
                came_from[next] = current
                score[next] = tentative_score
                sequence[len(sequence)-1][next] = score[next]
                
        #set the next set as the new current open set
        open_set = next_set
    # if the open set is empty, return an empty path
    return None, closed_set.union(open_set), sequence

