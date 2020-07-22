# Pyomo-QAOA #
- - -
## How to run ##
+ make sure that `pyomo-nonlinsol.py` is in the same directory as `qaoa_graph.py`
+ `./pyomo-nonlinsol.py graph_filename.qaoa <integer number of vertices>`
+ example: `python3 pyomo-nonlinsol.py test_graph.qaoa 2` runs the program on `testgraph.qaoa` having `2` vertices.
- - -
## To Do ##
+ double check objective expression for correctness
+ This program runs one graph at a time, so it could either be run within another bash script if multiple files are desired, or could be extended
+ CLI interface requires number of vertices to be specified independently of input file, and this could be changed if desired, so that it reads `n_vertices` from `graph_filename.qaoa` automatically.
+ dependency list

