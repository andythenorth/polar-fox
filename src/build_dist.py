import shutil
import os
currentdir = os.curdir
import sys

import codecs
import polar_fox

# add dir to path so we can do relative import of the Polar Fox python content for integrity checks
sys.path.insert(0,currentdir)
import src.constants as constants

dist_container_path = polar_fox.dist_container_path
dist_package_path = polar_fox.dist_package_path
dist_graphics_path = polar_fox.dist_graphics_path

def main():
    print("Integrity checks")
    # cargos must not be defined twice
    for label in set(constants.cargo_labels):
        assert constants.cargo_labels.count(label) == 1, ("Cargo %s is defined more than once") % label

    print("Preparing files for distribution")
    if os.path.exists(dist_container_path):
        print("Cleaning: removing", dist_container_path)
        shutil.rmtree(dist_container_path)
    os.mkdir(dist_container_path)
    if os.path.exists(dist_package_path):
        print("Cleaning: removing", dist_package_path)
        shutil.rmtree(dist_package_path)
    os.mkdir(dist_package_path)
    os.mkdir(os.path.join(dist_package_path, 'graphics'))

    dist_file_header = codecs.open(os.path.join(currentdir, 'src', 'dist_file_header.txt'), 'r','utf8').read()
    for filename in ['__init__.py', 'constants.py', 'git_info.py', 'graphics_units.py', 'pixa.py']:
        src_file = codecs.open(os.path.join(currentdir, 'src', filename), 'r','utf8')
        dist_file = codecs.open(os.path.join(dist_package_path, filename), 'w','utf8')
        dist_file.write(dist_file_header)
        dist_file.write(src_file.read())
        dist_file.close()
    for dir_name in ['piece_cargos', 'intermodal_containers']:
        dist_dir_path =  os.path.join(dist_graphics_path, dir_name)
        shutil.copytree(os.path.join(currentdir, 'generated', dir_name), dist_dir_path)
        shutil.copy(os.path.join(currentdir, 'src', 'dist_dir_header.txt'), os.path.join(dist_dir_path, '_files_here_are_generated.txt'))
    for filename in ['LICENSE.txt', 'README.txt']:
        shutil.copy(os.path.join(currentdir, filename), os.path.join(dist_package_path, filename))
    print("[DONE]")

if __name__ == '__main__':
    main()
