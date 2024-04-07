

from geomdl import exchange
from geomdl import multi
import json


def extract_corner(surface_name):
    output_dir = 'Surface_' + surface_name
    
    file_name = surface_name + '.json'
    data = exchange.import_json(f"./Trans3dm2json/{file_name}")

    
    surf_cont = multi.SurfaceContainer(data)

    surface = surf_cont[0]

    
    corners = [surface.evaluate_single([i,j])[:2] for i,j in [[0,0], [1,0], [0,1], [1,1]]]
    corner_coordinates = [[round(x,2), round(y,2)] for x,y in corners]
    
    Left, Right = sorted(corner_coordinates)[:2], sorted(corner_coordinates)[-2:]
    LT, LB = sorted(Left, key=lambda x: x[1])[1], sorted(Left, key=lambda x: x[1])[0]
    RT, RB = sorted(Right, key=lambda x: x[1])[1], sorted(Right, key=lambda x: x[1])[0]

    dict_corner_coordinates = {x: y for x, y in zip(['LT', 'LB', 'RT', 'RB'], [LT, LB, RT, RB])}
    json_str = json.dumps(dict_corner_coordinates, indent=4)
    save_dir = output_dir + '/' + 'corner_coordinates_real.json'
    with open(save_dir, 'w') as json_file:
        json_file.write(json_str)

if __name__ == '__main__':
    extract_corner(surface_name='S19_0')

