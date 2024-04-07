import rhinoscriptsyntax as rs
import json

def Project2Space(surface_name):
    print("The surface currently coping with:", surface_name)
    
    json_path = './' + 'Surface_' + surface_name + '/' + 'coordinates_TSed.json'
    with open(json_path, 'r') as f:
        result = json.load(f)
    coordinates = {int(k): tuple(v) for k, v in result.items()}


    
    all_sur = rs.filter.surface  
    sur_ids = rs.ObjectsByType(all_sur, select=True)  
    surface = sur_ids[0]  

    
    projected = {}
    miss_n = 0
    miss_coord_key = []
    for i in range(len(coordinates)):
        print("Processing:%d/%d" %(i, len(coordinates)-1))
        result = rs.ProjectPointToSurface(coordinates[i], surface, (0,0,-1))
        if len(result) > 0:
            result = result[0]  
            projected[i] = [round(result.X,2), round(result.Y,2), round(result.Z,2)]
        else:
            factor = 0.1
            try_ = 0
            while True:
                expand_direct = [[0,1,0], [1,0,0], [0,-1,0], [-1,0,0], [1,1,0], [1,-1,0], [-1,1,0], [-1,1,0]]
                for direct in expand_direct:
                    shift = [sft * factor for sft in direct]
                    new_coord = [v1+v2 for v1,v2 in zip(coordinates[i], shift)]
                    result = rs.ProjectPointToSurface(new_coord, surface, (0,0,-1))
                    if len(result) > 0:
                        result = result[0]
                        projected[i] = [round(result.X,2), round(result.Y,2), round(result.Z,2)]
                        break
                if len(result) > 0: break
                factor += 0.1
                try_ += 1
                if try_ > 50:
                    miss_coord_key.append(i)
                    miss_n += 1
                    break


    json_str = json.dumps(projected, indent=4)
    save_dir = './' + 'Surface_' + surface_name + '/' + 'coordinates_space.json'
    with open(save_dir, 'w') as json_file:
        json_file.write(json_str)
    
    if miss_coord_key != []:
        json_str = json.dumps(miss_coord_key, indent=4)
        save_dir = './' + 'Surface_' + surface_name + '/' + 'coordinates_missing.json'
        with open(save_dir, 'w') as json_file:
            json_file.write(json_str)

    print('General Hou remind you: ALL WORK DONE!')
    print('The generated coordinates_space.json is in directory: Surface_%s' %surface_name)
    print('total_n', len(coordinates), 'missing_n:', miss_n)


if __name__ == '__main__':
    Project2Space(surface_name='1G20')
