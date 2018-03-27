import shutil
import os
currentdir = os.curdir

import sys
import codecs
from pathlib import Path, PurePosixPath

consumers = [('Iron_Horse', 'iron-horse'),
             ('Road_Hog', 'road-hog'),
             ('Unsinkable_Sam', 'unsinkable-sam')]

dist_container_path = os.path.join(currentdir, 'dist')
dist_package_path = os.path.join(dist_container_path, 'polar_fox')

def build_dist():
    print("Preparing files for distribution")
    if os.path.exists(dist_container_path):
        shutil.rmtree(dist_container_path)
    os.mkdir(dist_container_path)
    if os.path.exists(dist_package_path):
        shutil.rmtree(dist_package_path)
    os.mkdir(dist_package_path)

    dist_file_header = codecs.open(os.path.join(currentdir, 'src', 'dist_file_header.txt'), 'r','utf8').read()
    for filename in ['__init__.py', 'constants.py', 'graphics_units.py', 'pixa.py']:
        src_file = codecs.open(os.path.join(currentdir, 'src', filename), 'r','utf8')
        dist_file = codecs.open(os.path.join(dist_package_path, filename), 'w','utf8')
        dist_file.write(dist_file_header)
        dist_file.write(src_file.read())
        dist_file.close()
    for dir_name in ['cargo_graphics']:
        dist_dir_path =  os.path.join(dist_package_path, dir_name)
        shutil.copytree(os.path.join(currentdir, 'src', dir_name), dist_dir_path)
        shutil.copy(os.path.join(currentdir, 'src', 'dist_dir_header.txt'), os.path.join(dist_dir_path, '_files_here_are_generated.txt'))

def distribute_to_consumers():
    print("Distributing to downstream consumers")
    # this assumes that consumers are found in a consistent ../../ location, and have a consistent Project_name/repo-name structure
    consumer_root = os.path.dirname(os.path.dirname(os.path.abspath(currentdir)))
    for consumer in consumers:
        print("..." + consumer[0])
        consumer_dst_path = os.path.join(consumer_root, consumer[0], consumer[1], 'src', 'polar_fox')
        if os.path.exists(consumer_dst_path):
            shutil.rmtree(consumer_dst_path)
        shutil.copytree(os.path.join(dist_package_path), consumer_dst_path)
    print("[DONE]")
    print("Don't forget to test and commit changes for each consumer")

def main():
    build_dist()
    distribute_to_consumers()

if __name__ == '__main__':
    main()
