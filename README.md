# MEQ Software Challenge

Python developer software challenge for MEQ. A very simple solution that begins by randomly searching the tree and making note of what states have been encountered and the path taken to reach them. Over time, the program adapts to what has been found and narrows down the search criteria until all 25 states have been fully explored.

When running the program multiple times, I saw that it took anywhere in the range of 3 to 15 seconds to completely map the state machine.

This is by no means a perfect solution. With an infinite amount of time, a perfect algorithm could be created to solve this problem in record speed. However, due to the small scope of the problem, I felt as though this approach was not inappropriate.

## Prerequisites

Graphviz must be installed on your system before the Python script will work properly. Graphviz can be installed by navigating to the [downloads site](https://graphviz.org/download/) and installing the right version for your system.

The Graphviz executable location (`path/to/graphviz/bin`) needs to be set in your system's PATH, or the Graphviz Python module won't work properly. 

Python 3 is also required before this script can be executed.

## Installation

1. Clone the repository with `git clone https://github.com/Tamookk/MEQ`
2. Navigate into the new `MEQ` folder
3. From the command line, install requirements with `pip install graphviz`
4. Copy the IP address of the server into `settings.txt` 
5. Run the program by running `python3 main.py` from the command line.
6. When finished, a file `output.pdf` will be generated and saved in the program's directory. This file contains a basic visualisation of the state machine. 