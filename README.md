The file `en.subject.pdf` describes the task

Steps:
- `python -m venv myvenv`
- `source myvenv\bin\activate`
- `python -m pip install -r requirements.txt`

Commands:
- `python src/npuzzle_gen.py -s > maps/tmp_map.txt`
- `python n_puzzle.py `

Usages:
- `usage: npuzzle_gen.py [-h] (-s | -u) [-i ITERATIONS] size`
- `usage: n_puzzle.py [-h] (-p PATH | -s SIZE) [--result_path RESULT_PATH | -r {snake_top_left_to_right,snake_top_left_to_bottom,snake_top_right_to_left,snake_top_right_to_bottom,snake_bottom_left_to_right,snake_bottom_left_to_top,snake_bottom_right_to_left,snake_bottom_right_to_top,spiral_top_left_to_right,spiral_top_left_to_bottom,spiral_top_right_to_left,spiral_top_right_to_bottom,spiral_bottom_left_to_right,spiral_bottom_left_to_top,spiral_bottom_right_to_left,spiral_bottom_right_to_top,direct_top_left_to_right,direct_top_left_to_bottom,direct_top_right_to_left, direct_top_right_to_bottom,direct_bottom_left_to_right,direct_bottom_left_to_top,direct_bottom_right_to_left,direct_bottom_right_to_top}] [-f {uniform,hamming,manhattan,euclidean,linear_conflict}] [-g] [-v]`

Pep8:
- `pycodestyle *.py --ignore=E501`

Used heuristics:
- Hamming distance (https://en.wikipedia.org/wiki/Hamming_distance)
- Manhattan distance (https://en.wikipedia.org/wiki/Taxicab_geometry)
- Euclidean distance (https://en.wikipedia.org/wiki/Euclidean_distance) 
- Linear Conflict (http://academiccommons.columbia.edu/download/fedora_content/download/ac:141290/CONTENT/cucs-219-85.pdf)
- Uniform distance (=0, -u)
- Greedy search (-g)

Used final states:
- snake 🐍
- spiral 🌀
- direct ☝

Maps are in `maps` directory

Final maps are in `final_maps` directory
