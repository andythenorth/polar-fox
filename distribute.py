import shutil
import os
currentdir = os.curdir

import sys
import codecs
from pathlib import Path, PurePosixPath

consumers = [('Iron_Horse', 'iron-horse'),
             ('Road_Hog', 'road-hog'),
             ('Unsinkable_Sam', 'unsinkable-sam')]

def main():
    print("Preparing files for distribution")
    dist_path = os.path.join(currentdir, 'dist')
    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)
    os.mkdir(dist_path)

    dist_header = codecs.open(os.path.join(currentdir, 'src', 'dist_header.txt'), 'r','utf8')
    src_file = codecs.open(os.path.join(currentdir, 'src', 'polar_fox.py'), 'r','utf8')
    dist_file = codecs.open(os.path.join(dist_path, 'polar_fox.py'), 'w','utf8')
    dist_file.write(dist_header.read())
    dist_file.write(src_file.read())
    dist_file.close()

    print("Distributing to downstream consumers")
    # this assumes that consumers are found in a consistent ../../ location, and have a consistent Project_name/repo-name structure
    consumer_root = os.path.dirname(os.path.dirname(os.path.abspath(currentdir)))
    for consumer in consumers:
        print("..." + consumer[0])
        consumer_dst_path = os.path.join(consumer_root, consumer[0], consumer[1], 'src', 'polar_fox.py')
        shutil.copy(os.path.join(dist_path, 'polar_fox.py'), consumer_dst_path)

    print("[DONE]")
    print("Don't forget to test and commit changes for each consumer")
if __name__ == '__main__':
    main()
