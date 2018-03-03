import shutil
import os
currentdir = os.curdir

import sys
import codecs

def main():
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
    """
        #compile strings to single lang file - english
        lang_template = lang_templates[i + '.pylng']

        dst_file = codecs.open(os.path.join(lang_dst, i + '.lng'), 'w','utf8')
        lang_content = src_file.read()
        lang_content = lang_content + lang_template(ships=ships, makefile_args=makefile_args)
        dst_file.write(lang_content)
        dst_file.close()
    """

if __name__ == '__main__':
    main()
