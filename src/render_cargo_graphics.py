import shutil
import os
currentdir = os.curdir

from PIL import Image
import pixa
from pixa import Spritesheet, PieceCargoSprites, pixascan
from graphics_units import SimpleRecolour, AppendToSpritesheet

import polar_fox
import constants

generated_files_path = polar_fox.generated_files_path

DOS_PALETTE = Image.open('palette_key.png').palette

# eh note that it's CC1 not 1CC here because python var names can't start with digit, but 1CC everywhere else :P
CC1 = 198
CC2 = 80
red = 40
grey = 2
black = 1

piece_cargo_graphics_maps = [("tarps_1", "tarps_blue_1",
                             {136: 145, 137: 146, 138: 147, 139: 148,
                             140: 149, 141: 150, 142: 151, 143: 152}),
                             # simple grey for default, avoids conflicts with most CC
                             ("tarps_1", "tarps_grey_1",
                             {136: 16, 137: 17, 138: 18, 139: 19,
                             140: 20, 141: 21, 142: 22, 143: 23}),
                             ("tarps_1", "tarps_gold_1",
                             {136: 60, 137: 61, 138: 62, 139: 63,
                             140: 64, 141: 65, 142: 66, 143: 67}),
                             ("tarps_1", "tarps_red_1",
                             {136: 40, 137: 41, 138: 42, 139: 43,
                             140: 44, 141: 45, 142: 46, 143: 47}),
                             ("barrels_silver_1", "barrels_silver_1", {}),
                             ("coffee_1", "coffee_1", {}),
                             ("crates_1", "crates_1", {}),
                             ("fruit_1", "fruit_1", {}),
                             ("ingots_1", "ingots_1", {}),
                             ("logs_1", "logs_1", {}),
                             ("lumber_planks_1", "lumber_planks_1", {}),
                             ("nuts_1", "nuts_1", {}),
                             ("pipes_1", "pipes_1", {}),
                             ("steel_wire_rod_1", "steel_wire_rod_1", {}),
                             ("coils_eye_to_sky_1", "paper_coils_eye_to_sky_1",
                             {136: 8, 137: 9, 138: 10, 139: 11,
                             140: 12, 141: 13, 142: 14, 143: 15}),
                             ("coils_eye_longitudinal_1", "steel_coils_eye_longitudinal_1",
                             {136: 3, 137: 16, 138: 17, 139: 18,
                             140: 19, 141: 20, 142: 21, 143: 22}),
                             ("coils_eye_to_sky_1", "steel_coils_eye_to_sky_1",
                             {136: 3, 137: 16, 138: 17, 139: 18,
                             140: 19, 141: 20, 142: 21, 143: 22}),
                             ("coils_eye_longitudinal_1", "copper_coils_eye_longitudinal_1",
                             {136: 60, 137: 112, 138: 62, 139: 115,
                             140: 117, 141: 118, 142: 119, 143: 120}),
                             ("coils_eye_to_sky_1", "copper_coils_eye_to_sky_1",
                             {136: 60, 137: 112, 138: 62, 139: 115,
                             140: 117, 141: 118, 142: 119, 143: 120}
                             )]

container_recolour_1CC = {40: CC1, 41: CC1+1, 42: CC1+2, 43: CC1+3, 44: CC1+4, 45: CC1+5, 46: CC1+6, 47: CC1+7}
container_recolour_2CC = {40: CC2, 41: CC2+1, 42: CC2+2, 43: CC2+3, 44: CC2+4, 45: CC2+5, 46: CC2+6, 47: CC2+7}
container_recolour_red = {40: red, 41: red+1, 42: red+2, 43: red+3, 44: red+4, 45: red+5, 46: red+6, 47: red+7}
container_recolour_grey = {40: grey, 41: grey+1, 42: grey+3, 43: grey+4, 44: grey+6, 45: grey+8, 46: grey+10, 47: grey+12}
container_recolour_black = {40: black, 41: black+1, 42: black+2, 43: black+3, 44: black+4, 45: black+5, 46: black+6, 47: black+7}

# configuration of containers without livery maps ...
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
                                      ("edibles_tank_20_foot", "edibles_tank_20_foot", container_recolour_1CC),
                                      ("edibles_tank_30_foot", "edibles_tank_30_foot", container_recolour_1CC),
                                      ("edibles_tank_40_foot", "edibles_tank_40_foot", container_recolour_1CC),
                                      ("stake_flatrack_20_foot", "stake_flatrack_20_foot", container_recolour_1CC),
                                      ("stake_flatrack_30_foot", "stake_flatrack_30_foot", container_recolour_1CC),
                                      ("stake_flatrack_40_foot", "stake_flatrack_40_foot", container_recolour_1CC),
                                      ("stake_flatrack_ingots_1_20_foot", "stake_flatrack_ingots_1_20_foot", container_recolour_1CC),
                                      ("stake_flatrack_ingots_1_30_foot", "stake_flatrack_ingots_1_30_foot", container_recolour_1CC),
                                      ("stake_flatrack_ingots_1_40_foot", "stake_flatrack_ingots_1_40_foot", container_recolour_1CC),
                                      ("livestock_20_foot", "livestock_20_foot", container_recolour_1CC),
                                      ("livestock_30_foot", "livestock_30_foot", container_recolour_1CC),
                                      ("livestock_40_foot", "livestock_40_foot", container_recolour_1CC),
                                      ("reefer_20_foot", "reefer_20_foot", container_recolour_1CC),
                                      ("reefer_30_foot", "reefer_30_foot", container_recolour_1CC),
                                      ("reefer_40_foot", "reefer_40_foot", container_recolour_1CC),
                                      ("wood_20_foot", "wood_20_foot", container_recolour_1CC),
                                      ("wood_30_foot", "wood_30_foot", container_recolour_1CC),
                                      ("wood_40_foot", "wood_40_foot", container_recolour_1CC)]

container_recolour_maps = {'1CC': container_recolour_1CC, '2CC': container_recolour_2CC,
                           'red': container_recolour_red, 'grey': container_recolour_grey,
                           'black': container_recolour_black}

# ...configuration of containers with cargo-specific liveries or visible cargos with recolouring or piece
cargo_specific_recolour_container_maps = {'bulk': constants.bulk_cargo_recolour_maps_extended,
                                          'chemicals_tank': constants.chemicals_tanker_livery_recolour_maps_extended,
                                          'cryo_tank': constants.cryo_tanker_livery_recolour_maps_extended,
                                          'curtain_side': constants.curtain_side_livery_recolour_maps_extended,
                                          'tank': constants.tanker_livery_recolour_maps_extended}

for container_type, recolour_maps in cargo_specific_recolour_container_maps.items():
    for label, container_recolour_name, cargo_recolour_map in recolour_maps:
        # by design, only 1 body colour is provided for tank containers, bulk containers etc, on trains they look better with a consistent colour
        # for ships, it might be desirable to provide an alt bulk body colour
        # that can be done by adding body_recolour_sufffix to the output filename ['', '_alt'] and specifying both
        recolour_map = cargo_recolour_map.copy()
        for k,v in container_recolour_maps[container_recolour_name].items():
            recolour_map[k] = v
        intermodal_container_graphics_maps.append((container_type + "_20_foot", container_type + "_" + label + "_20_foot", recolour_map))
        intermodal_container_graphics_maps.append((container_type + "_30_foot", container_type + "_" + label + "_30_foot", recolour_map))
        intermodal_container_graphics_maps.append((container_type + "_40_foot", container_type + "_" + label + "_40_foot", recolour_map))

for cargo_sprites_filename, cargo_labels in constants.container_piece_cargo_maps.items():
    for label in cargo_labels:
        container_type = 'stake_flatrack'
        recolour_map = container_recolour_1CC
        intermodal_container_graphics_maps.append((container_type + "_20_foot", container_type + "_" + label + "_20_foot", recolour_map, cargo_sprites_filename))
        intermodal_container_graphics_maps.append((container_type + "_30_foot", container_type + "_" + label + "_30_foot", recolour_map, cargo_sprites_filename))
        intermodal_container_graphics_maps.append((container_type + "_40_foot", container_type + "_" + label + "_40_foot", recolour_map, cargo_sprites_filename))

vehicles_recolour_1CC = {40: CC1, 41: CC1+1, 42: CC1+2, 43: CC1+3, 44: CC1+4, 45: CC1+5, 46: CC1+6, 47: CC1+7}

vehicles_cargo_graphics_maps = [("empty_20_foot", "empty_20_foot", vehicles_recolour_1CC),
                                ("trucks_1", "trucks_1_1CC", vehicles_recolour_1CC)]

knockout_guides_map = {k: 0 for k in range(215, 227)}


def composite_visible_cargo_sprites(input_image, cargo_sprites_filename):
    # provide visible cargo sprites, assumed to be for flatrack intermodal containers, may be extensible in future
    #piece_cargo_sprites = PieceCargoSprites(polar_fox_constants=constants, polar_fox_graphics_path=os.path.join('generated'))
    print(dir(piece_cargo_sprites))

    return input_image

def render(filename, input_image, units, graphics_output_path, cargo_sprites_filename=None):
    # expects to be passed a PIL Image object

    if cargo_sprites_filename is not None:
        composite_visible_cargo_sprites(input_image, cargo_sprites_filename)

    # units is a list of objects, with their config data already baked in (don't have to pass anything to units except the spritesheet)
    # each unit is then called in order, passing in and returning a pixa SpriteSheet
    # finally the spritesheet is saved
    spritesheet = pixa.make_spritesheet_from_image(input_image, DOS_PALETTE)
    for unit in units:
        spritesheet = unit.render(spritesheet)

    output_path = os.path.join(graphics_output_path, filename + '.png')
    # I don't normally leave commented-out code behind, but I'm bored of looking in the PIL docs for how to show the image during compile
    #spritesheet.sprites.show()
    spritesheet.save(output_path)

def main():
    print("Render cargo graphics")

    if not os.path.exists(generated_files_path):
        # don't destroy all of generated, other scripts might have built things into it
        os.mkdir(generated_files_path)

    # this is a bit crude, but eh, if it works it works
    cargo_graphics_items = {'piece_cargos': piece_cargo_graphics_maps,
                            'intermodal_containers': intermodal_container_graphics_maps, # must come after piece cargos as they're a dep for flatrack containers
                            'vehicles_cargos': vehicles_cargo_graphics_maps}
    for graphics_type_path, graphics_maps in cargo_graphics_items.items():
        graphics_input_path = os.path.join(currentdir, 'src', 'graphics', graphics_type_path)
        graphics_output_path = os.path.join(generated_files_path, graphics_type_path)
        if os.path.exists(graphics_output_path):
            # do destroy all of graphics output path
            shutil.rmtree(graphics_output_path)
        os.mkdir(graphics_output_path)
        for graphics_map in graphics_maps:
            input_image = Image.open(os.path.join(graphics_input_path, graphics_map[0] + '.png')).crop((0, 0, 300, 440))
            units = [SimpleRecolour(knockout_guides_map), SimpleRecolour(graphics_map[2])]
            # incredibly stupid and fragile way of detecting if we need to composite visible cargo sprites
            # this entire rendering approach is JFDI and would be better rewritten cleanly *iff* it needs extended again
            if len(graphics_map) > 3:
                cargo_sprites_filename = graphics_map[3]
            else:
                cargo_sprites_filename = None
            result = render(graphics_map[1], input_image, units, graphics_output_path, cargo_sprites_filename)

    print("[DONE]")

if __name__ == '__main__':
    main()
