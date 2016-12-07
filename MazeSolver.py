import numpy as np
from matplotlib import pyplot as plt
from math import sqrt

# inspired by https://en.wikipedia.org/wiki/A*_search_algorithm
def AStar(maze, mLen, start=(0,0), goal=(49,49), visualize=False):
  # define heuristic
  def heuristic_cost_estimate(n,g):
    return sqrt((n[0]-g[0])**2 + (n[1]-g[1])**2)

  # The set of nodes already evaluated.
  closedSet = []

  # The set of currently discovered nodes still to be evaluated.
  # Initially, only the start node is known.
  openSet = [start]  

  # For each node, which node it can most efficiently be reached from.
  # If a node can be reached from many nodes, cameFrom will eventually contain the
  # most efficient previous step.
  cameFrom = dict()

  # For each node, the cost of getting from the start node to that node.
  gScore = dict()  

  # For each node, the total cost of getting from the start node to the goal
  # by passing by that node. That value is partly known, partly heuristic.
  fScore = dict()

  # Set default values in gScore and fScore to infty
  for x in range(0,mLen):
    for y in range(0,mLen):
      gScore[(x,y)] = float('Inf')
      fScore[(x,y)] = float('Inf')

  # The cost of going from start to start is zero.
  gScore[start] = 0

  # For the first node, that value is completely heuristic.
  fScore[start] = heuristic_cost_estimate(start, goal)

  while len(openSet) !=0:
    # loop to find the node in openSet having the lowest fScore[] value
    current = openSet[0]
    minfScore = fScore[current]
    for ind in range(1,len(openSet)):
      if fScore[openSet[ind]] < minfScore:
        current = openSet[ind]
        minfScore = fScore[current]
 
    if current == goal:
      if visualize:
        return reconstruct_path(cameFrom, current) # this returns the found path
      return len(closedSet) + 1000 # this is used for optimization

    openSet.remove(current)
    closedSet.append(current)

    # a cell can have 4 neighbors:
    # (current[0]+1,current[1]) (current[0]-1,current[1])
    # (current[0],current[1]+1) (current[0],current[1]-1)
    # check if neighbor exists and if it is blocked
    neighbors = []
    if current[0]+1 < mLen:
      if maze[(current[0]+1) * mLen + current[1]] == 0:
        neighbors.append((current[0]+1,current[1]))
    if current[0]-1 >= 0:
      if maze[(current[0]-1) * mLen +current[1]] == 0:
        neighbors.append((current[0]-1,current[1]))
    if current[1]+1 < mLen:
      if maze[(current[0]) * mLen + current[1]+1] == 0:
        neighbors.append((current[0],current[1]+1))
    if current[1]-1 >= 0:
      if maze[(current[0]) * mLen + current[1]-1] == 0:
        neighbors.append((current[0],current[1]-1))

    # loop over each neighbor of current
    for neighbor in neighbors:
      if neighbor in closedSet:
        continue  # Ignore the neighbor which is already evaluated.

      # The distance from start to a neighbor
      # dist_between(current, neighbor) is always 1 in our grid
      tentative_gScore = gScore[current] + 1
      if neighbor not in openSet: # Discover a new node
        openSet.append(neighbor)
      elif tentative_gScore >= gScore[neighbor]:
        continue		# This is not a better path.

      # This path is the best until now. Record it!
      cameFrom[neighbor] = current
      gScore[neighbor] = tentative_gScore
      fScore[neighbor] = gScore[neighbor] + heuristic_cost_estimate(neighbor, goal)

  if visualize:
    return closedSet  # this returns the closed set for visualization
  
  return len(closedSet)


def reconstruct_path(cameFrom, current):
  total_path = [current]
  while current in cameFrom.keys():
    current = cameFrom[current]
    total_path.append(current)
  return total_path

def colorMaze(maze, mazeLen, cSet):
  img = np.zeros((mazeLen, mazeLen, 3), np.uint8)
  for x in range(0, mazeLen):
    for y in range(0, mazeLen):
      if maze[x*mazeLen + y] == 0:
        img[x][y][0] = img[x][y][1] = img[x][y][2] = 255
      if (x,y) in cSet:
        img[x][y][0] = 255
        img[x][y][1] = 0
        img[x][y][2] = 0
        

  plt.imshow(img)
  plt.axis('off')
  plt.show()

