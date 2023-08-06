"""CLI interface for idupes project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
import argparse
import glob
from pathlib import Path
from PIL import Image
import imagehash
import numpy as np
import tqdm
from joblib import Parallel, delayed
from collections import defaultdict
from sklearn.cluster import AgglomerativeClustering


def glob_image(root, recursive=True, ignore_hidden=True):
    exts = ['.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp']
    exts = exts + [v.upper() for v in exts]
    for ext in exts:
        if recursive:
            pattern = str(Path(root) / '**/*{}'.format(ext))
        else:
            pattern = str(Path(root) / '*{}'.format(ext))
        for p in glob.glob(pattern, recursive=recursive):
            if ignore_hidden:
                if not Path(p).stem.startswith('.'):
                    yield Path(p)
            else:
                yield Path(p)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path, help='path to the image folder')
    parser.add_argument('--distance_threshold', '-d', type=int, default=1, help='distance threshold(exclusive) that images to be considered same file')
    parser.add_argument('-r', '--recurse', action='store_true', help='for every directory given follow subdirectories encountered within')
    parser.add_argument('-j', '--njobs', default=0, type=int, help='parallel numbers')
    return parser.parse_args()


def compute_hash(path, args):
    return path, imagehash.dhash(Image.open(path), hash_size=8)

def generate(args):
    for path in tqdm.tqdm(glob_image(args.root, recursive=args.recurse), desc='searching folder {}'.format(args.root.resolve())):
        yield delayed(compute_hash)(path, args)


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m idupes` and `$ idupes `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    args = parse_args()

    if args.njobs <= 1:
        path_list = []
        hash_list = []
        for path in tqdm.tqdm(glob_image(args.root, recursive=args.recurse), desc='searching folder {}'.format(args.root.resolve())):
            path_list.append(path)
            _, hash = compute_hash(path, args)
            hash_list.append(hash)
    else:
        items = Parallel(n_jobs=args.njobs)(generate(args))
        path_list, hash_list = zip(*items)

    # calc distance matrix
    n = len(path_list)
    dist_matrix = np.full((len(path_list), len(path_list)), fill_value=0, dtype=np.int32)

    for i in range(n - 1):
        for j in range(i + 1, n):
            dist_matrix[i, j] = dist_matrix[j, i] = hash_list[i] - hash_list[j]

    
    clustering = AgglomerativeClustering(n_clusters=None, metric='precomputed', distance_threshold=args.distance_threshold, linkage='single')

    clustering.fit(dist_matrix)

    clusters = defaultdict(list)

    labels = clustering.labels_

    for i, label in zip(range(n), labels):
        clusters[label].append(path_list[i])

    for k, v in clusters.items():
        if len(v) > 1:
            for p in v :
                print(p)


