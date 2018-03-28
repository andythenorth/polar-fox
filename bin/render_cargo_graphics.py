import shutil
import os
currentdir = os.curdir

from PIL import Image
# note that we have to have copies of pix and graphics_units in /bin, can't use the ones in /src
from pixa import Spritesheet, pixascan
from graphics_units import SimpleRecolour, AppendToSpritesheet

import global_constants

generated_files_path = global_constants.generated_files_path
graphics_input_path = os.path.join(currentdir, 'src', 'cargo_graphics')
graphics_output_path = os.path.join(generated_files_path, 'cargo_graphics')

DOS_PALETTE = Image.open('palette_key.png').palette

cargo_graphics_maps = [("tarps_1", "tarps_blue_1",
                       {136: 198, 137: 199, 138: 200, 139: 201,
                        140: 202, 141: 203, 142: 204, 143: 205}),
                       ("tarps_1", "tarps_2cc_1",
                       {136: 198, 137: 199, 138: 200, 139: 201,
                        140: 202, 141: 203, 142: 204, 143: 205}),
                       ("tarps_1", "tarps_gold_1",
                       {136: 198, 137: 199, 138: 200, 139: 201,
                        140: 202, 141: 203, 142: 204, 143: 205}),
                       ("tarps_1", "tarps_red_1",
                       {136: 198, 137: 199, 138: 200, 139: 201,
                        140: 202, 141: 203, 142: 204, 143: 205}),
                       ("barrels_silver", "barrels_silver", {}),
                       ("coffee", "coffee", {}),
                       ("crates_1", "crates_1", {}),
                       ("fruit", "fruit", {}),
                       ("logs", "logs", {}),
                       ("lumber_planks", "lumber_planks", {}),
                       ("nuts", "nuts", {}),
                       ("paper_coils_red", "paper_coils_red", {}),
                       ("paper_coils", "paper_coils", {}),
                       ("steel_coils", "steel_coils", {}),
                       ("copper_coils", "copper_coils", {})]

def make_spritesheet_from_image(input_image):
    spritesheet = Spritesheet(width=input_image.size[0], height=input_image.size[1] , palette=DOS_PALETTE)
    spritesheet.sprites.paste(input_image)
    return spritesheet

def render(filename, input_image, units):
    # expects to be passed a PIL Image object
    # units is a list of objects, with their config data already baked in (don't have to pass anything to units except the spritesheet)
    # each unit is then called in order, passing in and returning a pixa SpriteSheet
    # finally the spritesheet is saved
    output_path = os.path.join(graphics_output_path, filename + '.png')
    spritesheet = make_spritesheet_from_image(input_image)

    for unit in units:
        spritesheet = unit.render(spritesheet)
    # I don't normally leave commented-out code behind, but I'm bored of looking in the PIL docs for how to show the image during compile
    #spritesheet.sprites.show()
    spritesheet.save(output_path)

def main():
    print("Render cargo graphics")

    if not os.path.exists(generated_files_path):
        # don't destroy all of generated, other scripts might have built things into it
        os.mkdir(generated_files_path)
    if os.path.exists(graphics_output_path):
        # do destroy all of graphics output path
        shutil.rmtree(graphics_output_path)
    os.mkdir(graphics_output_path)

    print("Rendering not implemented, using straight copy instead")
    for cargo_graphics_map in cargo_graphics_maps:
        print(cargo_graphics_map[0])
        input_image = Image.open(os.path.join(graphics_input_path, cargo_graphics_map[0] + '.png')).crop((0, 0, 300, 300))
        units = [SimpleRecolour(cargo_graphics_map[2])]
        result = render(cargo_graphics_map[1], input_image, units)

    print("[DONE]")

if __name__ == '__main__':
    main()
