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
import shutil
import os

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
    parser.add_argument('root', type=Path, help='需要搜索的文件夹路径')
    parser.add_argument('--distance_threshold', '-d', type=int, default=1, help='相似度容差, 越大条件越松')
    parser.add_argument('-r', '--recurse', action='store_true', help='是否递归处理子文件夹')
    parser.add_argument('-j', '--njobs', default=0, type=int, help='并行数量, 加速出来速度, 不要超过机器的核心数')
    parser.add_argument('--move-to', '-t', type=Path, default=None, help='将重复图片移动到的目标目录')
    parser.add_argument('--group-duplicates', '-g', action='store_true', help='是否对文件进行相似度分组')
    parser.add_argument('--keep-one', action='store_true', help='移动图片时是否保留一张')
    return parser.parse_args()


def compute_hash(path, args):
    return path, imagehash.dhash(Image.open(path), hash_size=8)

def generate(args):
    for path in tqdm.tqdm(glob_image(args.root, recursive=args.recurse), desc='searching folder {}'.format(args.root.resolve()), leave=False):
        yield delayed(compute_hash)(path, args)


def target_path(key, path, args):
    target_path = args.move_to / Path(path).name
    if args.group_duplicates:
        target_path = args.move_to / '{}'.format(key) / Path(path).name
    target_path.parent.mkdir(parents=True, exist_ok=True)   
    return target_path

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

    if args.move_to:
        args.move_to.mkdir(parents=True, exist_ok=True)

    
    for k, v in clusters.items():
        if len(v) > 1:
            for p in v :
                print(p)
            if args.move_to:
                # create symlink for first file
                if args.keep_one:
                    os.symlink(v[0], target_path(k, v[0], args))
                    i = 1
                else:
                    i = 0
                # move left files 
                for p in v[i:]:
                    shutil.move(p, target_path(k, p, args))


