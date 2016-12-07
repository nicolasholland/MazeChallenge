import random
import numpy as np
from matplotlib import pyplot as plt
from MazeSolver import colorMaze

# Code inspired by Programming Collective Intelligence by Toby Segaran
def geneticoptimize(mLen, mazeLen,costf,popsize=50,step=1,mutprob=0.2,elite=0.2,maxiter=200):
  # Mutation Operation
  def mutate(vec):
    i=random.randint(0, mazeLen-1)
    return vec[0:i]+[random.randint(0,1)]+vec[i+1:]


  # Crossover Operation
  def crossover(r1,r2):
    i=random.randint(1,mazeLen-2)
    return r1[0:i]+r2[i:]

  # Build the initial population
  pop=[]
  for i in range(popsize):
    vec=[random.randint(0,1)
          for i in range(mazeLen)]
    pop.append(vec)

  # How many winners from each generation?
  topelite=int(elite*popsize)

  # Main loop
  for i in range(maxiter):
    scores=[(-costf(v, mLen),v) for v in pop]
    scores.sort( )
    ranked=[v for (s,v) in scores]

    # Start with the pure winners
    pop=ranked[0:topelite]

    # Add mutated and bred forms of the winners
    while len(pop)<popsize:
      if random.random( )<mutprob: 
        # Mutation
        c=random.randint(0,topelite)
        pop.append(mutate(ranked[c]))

      else:
        # Crossover
        c1=random.randint(0,topelite)
        c2=random.randint(0,topelite)
        pop.append(crossover(ranked[c1],ranked[c2]))

    # Print current best score
    print "gen.opt.: ", scores[0][0], i
  return scores[0][1]



def visualizeMaze(maze, mazeLen):
  img = np.zeros((mazeLen, mazeLen, 3), np.uint8)
  for x in range(0, mazeLen):
    for y in range(0, mazeLen):
      if maze[x*mazeLen + y] == 0:
        img[x][y][0] = img[x][y][1] = img[x][y][2] = 255 

  plt.imshow(img)
  plt.axis('off')
  plt.show()

