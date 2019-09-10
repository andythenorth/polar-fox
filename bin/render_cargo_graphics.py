import shutil
import os
currentdir = os.curdir

from PIL import Image
# note that we have to have copies of pix and graphics_units in /bin, can't use the ones in /src
from pixa import Spritesheet, pixascan
from graphics_units import SimpleRecolour, AppendToSpritesheet

import global_constants

generated_files_path = global_constants.generated_files_path

DOS_PALETTE = Image.open('palette_key.png').palette

piece_cargo_graphics_maps = [("tarps_1", "tarps_blue_1",
                             {136: 145, 137: 146, 138: 147, 139: 148,
                             140: 149, 141: 150, 142: 151, 143: 152}),
                             ("tarps_1", "tarps_2cc_1",
                             {136: 198, 137: 199, 138: 200, 139: 201,
                             140: 202, 141: 203, 142: 204, 143: 205}),
                             ("tarps_1", "tarps_gold_1",
                             {136: 60, 137: 61, 138: 62, 139: 63,
                             140: 64, 141: 65, 142: 66, 143: 67}),
                             ("tarps_1", "tarps_red_1",
                             {136: 40, 137: 41, 138: 42, 139: 43,
                             140: 44, 141: 45, 142: 46, 143: 47}),
                             ("barrels_silver", "barrels_silver", {}),
                             ("coffee", "coffee", {}),
                             ("crates_1", "crates_1", {}),
                             ("fruit", "fruit", {}),
                             ("logs", "logs", {}),
                             ("lumber_planks", "lumber_planks", {}),
                             ("nuts", "nuts", {}),
                             ("coils_1", "paper_coils",
                             {136: 8, 137: 9, 138: 10, 139: 11,
                             140: 12, 141: 13, 142: 14, 143: 15}),
                             ("coils_1", "steel_coils",
                             {136: 3, 137: 16, 138: 17, 139: 18,
                             140: 19, 141: 20, 142: 21, 143: 22}),
                             ("coils_1", "copper_coils",
                             {136: 60, 137: 112, 138: 62, 139: 115,
                             140: 117, 141: 118, 142: 119, 143: 120})]

# eh note that it's CC1 not 1CC here because python var names can't start with digit, but 1CC everywhere else :P
CC1 = 198
CC2 = 80
red = 40

container_recolour_1CC = {136: CC1, 137: CC1+1, 138: CC1+2, 139: CC1+3, 140: CC1+4, 141: CC1+5, 142: CC1+6, 143: CC1+7}
container_recolour_2CC = {136: CC2, 137: CC2+1, 138: CC2+2, 139: CC2+3, 140: CC2+4, 141: CC2+5, 142: CC2+6, 143: CC2+7}
container_recolour_red = {136: red, 137: red+1, 138: red+2, 139: red+3, 140: red+4, 141: red+5, 142: red+6, 143: red+7}

intermodal_container_graphics_maps = [("empty_20_foot", "empty_20_foot", container_recolour_1CC),
                                      ("empty_30_foot", "empty_30_foot", container_recolour_1CC),
                                      ("empty_40_foot", "empty_40_foot", container_recolour_1CC),
                                      ("box_20_foot", "box_20_foot_1CC", container_recolour_1CC),
                                      ("box_20_foot", "box_20_foot_2CC", container_recolour_2CC),
                                      ("box_20_foot", "box_20_foot_red", container_recolour_red),
                                      ("box_30_foot", "box_30_foot_1CC", container_recolour_1CC),
                                      ("box_30_foot", "box_30_foot_2CC", container_recolour_2CC),
                                      ("box_30_foot", "box_30_foot_red", container_recolour_red),
                                      ("box_40_foot", "box_40_foot_1CC", container_recolour_1CC),
                                      ("box_40_foot", "box_40_foot_2CC", container_recolour_2CC),
                                      ("box_40_foot", "box_40_foot_red", container_recolour_red)]

knockout_guides_map = {k: 0 for k in range(215, 227)}

def make_spritesheet_from_image(input_image):
    spritesheet = Spritesheet(width=input_image.size[0], height=input_image.size[1] , palette=DOS_PALETTE)
    spritesheet.sprites.paste(input_image)
    return spritesheet

def render(filename, input_image, units, graphics_output_path):
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

    # this is a bit crude, but eh, if it works it works
    for graphics_type_path, cargo_graphics_maps in {'cargo_graphics': piece_cargo_graphics_maps, 'intermodal_container_graphics': intermodal_container_graphics_maps}.items():
        graphics_input_path = os.path.join(currentdir, 'src', graphics_type_path)
        graphics_output_path = os.path.join(generated_files_path, graphics_type_path)
        if os.path.exists(graphics_output_path):
            # do destroy all of graphics output path
            shutil.rmtree(graphics_output_path)
        os.mkdir(graphics_output_path)
        for cargo_graphics_map in cargo_graphics_maps:
            input_image = Image.open(os.path.join(graphics_input_path, cargo_graphics_map[0] + '.png')).crop((0, 0, 300, 440))
            units = [SimpleRecolour(knockout_guides_map), SimpleRecolour(cargo_graphics_map[2])]
            result = render(cargo_graphics_map[1], input_image, units, graphics_output_path)

    print("[DONE]")

if __name__ == '__main__':
    main()
