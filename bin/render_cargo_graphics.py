import shutil
import os
currentdir = os.curdir

import global_constants

generated_files_path = global_constants.generated_files_path
cargo_graphics_input_path = os.path.join(currentdir, 'src', 'cargo_graphics')
cargo_graphics_output_path = os.path.join(generated_files_path, 'cargo_graphics')

def main():
    print("Render cargo graphics")

    if not os.path.exists(generated_files_path):
        # don't destroy all of generated, other scripts might have built things into it
        os.mkdir(generated_files_path)
    if os.path.exists(cargo_graphics_output_path):
        # do destroy all of graphics output path
        shutil.rmtree(cargo_graphics_output_path)
    os.mkdir(cargo_graphics_output_path)

    print("[DONE]")

if __name__ == '__main__':
    main()
