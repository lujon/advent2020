import fileinput
from collections import defaultdict
from itertools import groupby
from math import prod

import numpy as np

input_rows = [line.rstrip() for line in fileinput.input('input.txt')]


def parse_tile(tile_rows):
    tile_id = int(tile_rows[0].split()[1][:-1])
    image_rows = tile_rows[1:]

    image = np.array([[1 if c == '#' else 0 for c in row] for row in image_rows], int)

    return tile_id, image, [
        tuple(image[0]),
        tuple(reversed(image[0])),
        tuple(image[-1]),
        tuple(reversed(image[-1])),
        tuple(image[:, 0]),
        tuple(reversed(image[:, 0])),
        tuple(image[:, -1]),
        tuple(reversed(image[:, -1]))
    ]


tiles = map(parse_tile, [list(rows) for k, rows in groupby(input_rows, bool) if k])

tiles_by_edge = defaultdict(list)

for tile_id, _, edges in tiles:
    for edge in edges:
        tiles_by_edge[edge].append(tile_id)

matched_edges_by_tile = defaultdict(list)

for edge, tile_ids in tiles_by_edge.items():
    if len(tile_ids) > 1:
        for tile_id in tile_ids:
            matched_edges_by_tile[tile_id].append(edge)

print(prod([tile_id for tile_id, matched_edges in matched_edges_by_tile.items() if len(matched_edges) == 4]))
