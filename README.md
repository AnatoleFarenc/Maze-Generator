*This project has been created as part of the 42 curriculum by anfarenc, chehir*

# Description
A-Maze-ing is all about, you guessed it, maze generation. In this project, we learn how to create
mazes, the different ways to display them, and how to use them for different purposes such as
pathfinding, or optionally, game loops.

While we were given a good amount of freedom, the project must still meet some core requirements:
- Parse a config file and covert the data to usable values
- Generate a valid maze based on these values
- Save the maze to a file in a hexadecimal encoded format
- Provide a visual representation of the maze
- Organise everything into a re-usable module

On top of the mandatory part, we also implemented a few bonus features, which I will not explain
yet in order to create a feeling of suspense.



# Instructions
In this section we will be explaining how to run our program. The instructions on how to use it
for your own project will be in the **Re-usability** section below.

The first step is to make sure you are in the root folder of the project. Once there, you can run
the command "make install". This will set up a virtual environment will all the dependencies
installed.

Now that the venv is set up, you can run "make lint" to verify the source code. More specifically,
this target will run two linters: flake8, and Mypy. Flake8 makes sure the code is formatted
properly and has proper syntax, while Mypy is a type checker that verifies the type hints are
consistent.

Once that's done, we can get onto the fun part: running the program! To do this, simply run the
command "make run" and follow the instructions within the program. You'll be able to use it to
create new mazes, show the shortest path from start to end, change the maze colors, as well as a
few surprise features :)

Finally, you can run "make clean" to delete the virtual machine, the caches, and the maze.txt file.



# Project Overview
## Project File Organization
Below is a representation of the file structure, aswell as a brief rundown what each folder
contains:
```
A-Maze-ing
|
├── data
│   ├── config.txt
│   ├── maze.txt            # Created maze data will be stored here
│   └── requirements.txt
├── amazing
│   ├── __init__.py         # Marks the src directory as a package
│   └── ...
├── .flake8                 # Marks the venv folder to be excluded by flake8
├── .gitignore              # Marks files to be ignored by git
├── Makefile
└── README.md
```
- The data/ folder holds the config and requirements files. The maze.txt file containing the created
maze information will also be created here.
- The amazing/ folder contains all of the source code.
- Everything else is in the root folder.

## Maze Configuration
The following is an example of a valid config file for our project:
```
# Maze size variables
WIDTH=10
HEIGHT=10

# Start and End coordinates
ENTRY=0,0
EXIT=9,9

# Output file name
OUTPUT_FILE=maze.txt

# If PERFECT is true, there must only be one possible path between two given cells
PERFECT=True

# Seed for maze generation
SEED=0

# Maze display colors
WALLS=WHITE
OBJECTIVES=RED
PATH=BLUE
```

All of these keys are mandatory. If any of them are missing, or have incorrect values, the program
will not run.

Possible values for each key:
- WIDTH & HEIGHT: Any integer. Note that if the maze is too large, the maze generation function may
                  hit the recursion limit. However, this case is managed by Exception handling and
                  will not result in a crash
- ENTRY & EXIT: An x and y coordinate, separated by a comma. The coordinates must be within the
                WIDTH and HEIGHT values
- OUTPUT_FILE: A file name ending in '.txt'
- PERFECT: A boolean (True or False)
- SEED: Any integer. If the seed is 0, the program will ignore it and generate a random maze
- WALLS, OBJECTIVES & PATH: Any color as long as it's White, Red, Green, Blue, Yellow, or Purple


## Re-usability
Blabla


## Maze Generation Algorithm
Blabla


## Bonus Features
And now for the moment you've all been waiting for: the bonus features! These were very fun to
implement and 
- An improved user-interface loop that allows for dynamic config changes and viewing maze data
  and configuration from within the program
- Multiple display options for the generated maze
- Pathfinding animation that shows the path being created
- A fun minigame :D


## Project Management
Coming up with a decent blueprint and equally dividing the work between teammates is one of the
most important steps in any project, and because good management is an essential skill in the
workplace, we wanted to make sure we succeeded in this area. The fact that there were only two
people in the group was definitely a contributing factor, but we nonetheless managed to achieve
this without ***too*** much difficulty.

### Team Roles
Behold, a good old table to demonstrate task distribution:

|           anfarenc           |            chehir            |         Mutual Tasks         |
|:-----------------------------|:-----------------------------|:-----------------------------|
| Maze class implementation    | Parser for the config file   | Cell class implementation    |
| Maze generation algorithm    | User interface loop          | Bug fixes                    |
| Pathfinding algorithm        | Display functions            | Code refactoring             |
| ...                          | ...                          | ...                          |


### Roadmap
The equal division of the workload may have gone great, but we admittedly could have done a better
job at plotting the course of our amazing ***A-Maze-ing*** journey, because the initial timeline we
came up with went something like this:

**Parsing -> Maze Generation -> Maze rendering -> ??? -> Final result**

This, rather self-evidently, is a very lackluster roadmap, and resulted in a few *"What do I do
now?"* or *"I didn't realise we had to do this"* moments.
Some actual examples of this include:
- Having to add color keys to the config file halfway through the project, which involved having
  to update all the parsing code.
- When we decided to have multiple maze formats for the terminal display, which meant adding a
  'style' parameter to the already established display functions.
- Adding the 42 symbol generation ***after*** having already implemented the maze creation algorithm.
- Playing Smash Ultimate instead of working because we didn't know what to do next.

Luckily, because we wrote the code to be easily maintainable and re-usable, this was not too big a
problem, but on a larger project with more people involved it just wouldn't have cut it. It was
a good learning experience, and we now know how to do better for future projects.

Summarized timeline:
1.  Parser
2.  Maze template implementation
3.  Output file creation
4.  User interface
5.  Proper maze generation algorithm
6.  Center 42 symbol addition
7.  Pathfinding algorithm
8.  Lots of refactoring
9.  Makefile
10. Finished README


### Progression
While putting together the pieces of this project, we were both surprised at how well it went.
There were no issues implementing one person's code into the other's, and we were both able to
accomplish our share of the work. Communication played an important role in this: we made sure to
consult the other person on how best to accomplish each task, and reached a consensus before doing
anything. This also meant that we were both happy with the final result and know how the entire
thing works and fits together, even if we each handled our respective parts separately. We also
made sure the code was easily re-usable, which made complex features more easy to implement, as
we could build on top of an already solid foundation.

As mentioned previously, the roadmap could, and should have had more effort put into it, but
even so, it turned out well.


### Tools
No specific tools were used for this project. It runs on the default linux terminal using only
python's standard library.



# Resources

## Research
Below is a list of as many websites, articles, videos, or blogs we found during our research:

[ANSI escape code list](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)

[Seeded random explanation](https://www.w3schools.com/python/ref_random_seed.asp)

[Markdown file structure example](https://stackoverflow.com/questions/19699059/print-directory-file-structure-with-icons-for-representation-in-markdown)

[Readme tutorial](https://www.makeareadme.com/)


## AI
While we wanted to avoid using it as much as possible for pride-related reasons, AI was still used
sparingly for a few cases, in order to avoid spending too much time on the boring parts:
- Debugging
- Researching specific information:
  - Relevant UNICODE symbols
  - Useful libraries
  - Bash commands for Makefile