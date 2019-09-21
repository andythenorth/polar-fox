import shutil
import os
currentdir = os.curdir

from PIL import Image
# note that we have to have copies of pix and graphics_units in /bin, can't use the ones in /src
from pixa import Spritesheet, pixascan
from graphics_units import SimpleRecolour, AppendToSpritesheet

import polar_fox
import constants

generated_files_path = polar_fox.generated_files_path

DOS_PALETTE = Image.open('palette_key.png').palette

cargo_graphics_maps = [("tarps_1", "tarps_blue_1",
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
grey = 2

container_recolour_1CC = {40: CC1, 41: CC1+1, 42: CC1+2, 43: CC1+3, 44: CC1+4, 45: CC1+5, 46: CC1+6, 47: CC1+7}
container_recolour_2CC = {40: CC2, 41: CC2+1, 42: CC2+2, 43: CC2+3, 44: CC2+4, 45: CC2+5, 46: CC2+6, 47: CC2+7}
container_recolour_red = {40: red, 41: red+1, 42: red+2, 43: red+3, 44: red+4, 45: red+5, 46: red+6, 47: red+7}
container_recolour_grey = {40: grey, 41: grey+1, 42: grey+3, 43: grey+4, 44: grey+6, 45: grey+8, 46: grey+10, 47: grey+12}

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
                                      ("box_40_foot", "box_40_foot_red", container_recolour_red),
                                      ("tank_20_foot", "tank_20_foot_1CC", container_recolour_1CC),
                                      ("tank_30_foot", "tank_30_foot_1CC", container_recolour_1CC),
                                      ("tank_40_foot", "tank_40_foot_1CC", container_recolour_1CC)]

for label, cargo_recolour_map in constants.bulk_cargo_recolour_maps:
    body_recolour_maps = {'1CC': container_recolour_1CC, '2CC': container_recolour_2CC,
                          'red': container_recolour_red, 'grey': container_recolour_grey}
    for body_colour_suffix, body_recolour_map in body_recolour_maps.items():
        recolour_map = cargo_recolour_map.copy()
        for k,v in body_recolour_map.items():
            recolour_map[k] = v
        intermodal_container_graphics_maps.append(("bulk_20_foot", label + "_20_foot_" + body_colour_suffix, recolour_map))

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
    for graphics_type_path, graphics_maps in {'cargo_graphics': cargo_graphics_maps, 'intermodal_container_graphics': intermodal_container_graphics_maps}.items():
        graphics_input_path = os.path.join(currentdir, 'src', graphics_type_path)
        graphics_output_path = os.path.join(generated_files_path, graphics_type_path)
        if os.path.exists(graphics_output_path):
            # do destroy all of graphics output path
            shutil.rmtree(graphics_output_path)
        os.mkdir(graphics_output_path)
        for graphics_map in graphics_maps:
            input_image = Image.open(os.path.join(graphics_input_path, graphics_map[0] + '.png')).crop((0, 0, 300, 440))
            units = [SimpleRecolour(knockout_guides_map), SimpleRecolour(graphics_map[2])]
            result = render(graphics_map[1], input_image, units, graphics_output_path)

    print("[DONE]")

if __name__ == '__main__':
    main()
