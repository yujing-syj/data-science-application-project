"""
CS 121: Language shifts

Yujing Sun

Functions for language shift simulation.

This program takes the following parameters:
    grid _file (string): the name of a file containing a sample region
    R (int): neighborhood radius
    A (float): the language state transition threshold A
    Bs (list of floats): a list of the transition thresholds B to
      use in the simulation
    C (float): the language state transition threshold C
      centers (list of tuples): a list of community centers in the
      region
    max_steps (int): maximum number of steps

Example use:
    $ python3 language.py -grid_file tests/writeup-grid-with-cc.txt
	  --r 2 --a 0.5 --b 0.9 --c 1.2 --max_steps 5
While shown on two lines, the above should be entered as a single command.
"""

import copy
import click
import utility


# 1.whether within a community center.
def in_center(i, j, centers):
    """
    Check whether location(i, j) this is the community center.
    Inputs:
      i,j : the location of each cell
      centers (list of tuples): a list of community centers in the region
    Returns: True or False
    """
    if len(centers) == 0:
        return False
    in_or_not = False
    for center in centers:
        if abs(center[0][0]-i)<=center[1] and abs(center[0][1]-j)<=center[1]:
            in_or_not = True
            break
    return in_or_not


# 2. the engagement level of a home.
def engagement_level(grid, R, i, j):
    """
    Calculate the engagement level of grid
    Inputs:
      grid (list of lists of ints): the grid
      R (int): neighborhood radius
      i,j : the location of each cell
    Returns: the engagement level of each location
    """
    lenth = len(grid)
    engagement = []
    for m in range(max(0, i - R), min(i + R + 1, lenth)):
        for n in range(max(0, j - R), min(j + R + 1, lenth)):
            engagement.append(grid[m][n])
    num_engagement = sum(engagement) / len(engagement)
    return num_engagement


# 3. the language state of the next generation.
def next_generation(grid, R, centers, thresholds, i, j):
    """
    Get the next generation for the whole grid.
    Inputs:
      grid (list of lists of ints): the grid
      R (int): neighborhood radius
      thresholds (float, float, float): the language
        state transition thresholds (A, B, C)
      centers (list of tuples): a list of community centers in the
        region
      i,j : the location of each cell
    Returns: the next generation.
    """
    engage = engagement_level(grid, R, i, j)
    # the change of state_0
    if grid[i][j] == 0:
        if engage > thresholds[1]:
            grid[i][j] = 1
    # the change of state_1
    elif grid[i][j] == 1:
        if engage<thresholds[1] and in_center(i,j,centers) is False:
            grid[i][j] = 0
        elif engage > thresholds[2]:
            grid[i][j] = 2
    # the change of state_2
    elif grid[i][j] == 2:
        if engage<=thresholds[0] and in_center(i,j,centers) is False:
            grid[i][j] = 0
        elif thresholds[0]<engage<thresholds[1] and in_center(i,j,centers) is False:
            grid[i][j] = 1

    return grid[i][j]



# 4. simulate a step of the simulation
def step_one(grid, R, centers, thresholds):
    """
    Get the next generation for the whole grid.
    Inputs:
      grid (list of lists of ints): the grid
      R (int): neighborhood radius
      thresholds (float, float, float): the language
        state transition thresholds (A, B, C)
      centers (list of tuples): a list of community centers in the
        region
    Returns: the next generation.
    """

    for i in range(len(grid)):
        for j in range(len(grid)):
            next_generation(grid, R, centers, thresholds, i, j)
    return grid

# 5. run the steps until one of the stopping conditions is met.
def stop_condition(grid, R, centers, thresholds, max_steps):
    """
    Stop the simulation at final state.
    Inputs:
      grid (list of lists of ints): the grid
      R (int): neighborhood radius
      thresholds (float, float, float): the language
        state transition thresholds (A, B, C)
      centers (list of tuples): a list of community centers in the
        region
      max_steps (int): maximum number of steps
    Returns: the final grid
    """
    step = 0
    if max_steps == 1:
        return step_one(grid, R, centers, thresholds)
    while step < max_steps:
        grid_old = copy.deepcopy(grid)
        grid = step_one(grid, R, centers, thresholds)
        if grid != grid_old:
            step += 1
        else:
            break
    return grid


# 6. calculate the final outcome
def run_simulation(grid, R, thresholds, centers, max_steps):
    """
    Do the simulation and caculate the final frequency of each state.
    Inputs:
      grid (list of lists of ints): the grid
      R (int): neighborhood radius
      thresholds (float, float, float): the language
        state transition thresholds (A, B, C)
      centers (list of tuples): a list of community centers in the
        region
      max_steps (int): maximum number of steps
    Returns: the frequency of each language state (int, int, int)
    """
    final = stop_condition(grid, R, centers, thresholds, max_steps)
    print(final)
    state_0 = 0
    state_1 = 0
    state_2 = 0
    for i in range(len(final)):
        for j in range(len(final)):
            if final[i][j] == 0:
                state_0 += 1
            elif final[i][j] == 1:
                state_1 += 1
            else:
                state_2 += 1
    return (state_0, state_1, state_2 )


def simulation_sweep(grid, R, A, Bs, C, centers, max_steps):
    """
    Run the simulation with various values of threshold B.

    Inputs:
      grid (list of lists of ints): the grid
      R (int): neighborhood radius
      A (float): the language state transition threshold A
      Bs (list of floats): a list of the transition thresholds B to
        use in the simulation
      C (float): the language state transition threshold C
      centers (list of tuples): a list of community centers in the
        region
      max_steps (int): maximum number of steps

    Returns: a list of frequencies (tuples) of language states for
      each threshold B.
    """
    sweep = []
    for B in Bs:
        grid_new = copy.deepcopy(grid)
        sweep.append(run_simulation(grid_new,R,(A,B,C),centers,max_steps))
    return sweep


@click.command(name="language")
@click.option('--grid_file', type=click.Path(exists=True),
              default="tests/writeup-grid.txt", help="filename of the grid")
@click.option('--r', type=int, default=1, help="neighborhood radius")
@click.option('--a', type=float, default=0.6, help="transition threshold A")
@click.option('--b', type=float, default=0.8, help="transition threshold B")
@click.option('--c', type=float, default=1.6, help="transition threshold C")
@click.option('--max_steps', type=int, default=1,
              help="maximum number of simulation steps")
def cmd(grid_file, r, a, b, c, max_steps):
    '''
    Run the simulation.
    '''

    grid, centers = utility.read_grid(grid_file)
    print_grid = len(grid) < 20

    print("Running the simulation...")

    if print_grid:
        print("Initial region:")
        for row in grid:
            print("   ", row)
        if len(centers) > 0:
            print("With community centers:")
            for center in centers:
                print("   ", center)

    # run the simulation
    frequencies = run_simulation(grid, r, (a, b, c), centers, max_steps)

    if print_grid:
        print("Final region:")
        for row in grid:
            print("   ", row)

    print("Final language state frequencies:", frequencies)

if __name__ == "__main__":
    cmd()
