import cv2
import json
import numpy as np



class MissingCoorinates:
    def __init__(self, img):
        self.img = img
        self.missing_coordinates = []  
        self.windows_name = 'Click grid corners to pick coordinates(ESC to escape)'

        cv2.namedWindow(self.windows_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.windows_name, self.callback_function)

    
    def callback_function(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.missing_coordinates.append([x, y])
            print(f'The clicked coordinate value is [{x}, {y}]')

    def run(self):
        while True:
            cv2.imshow(self.windows_name, self.img)
            key = cv2.waitKey()
            if key == 27:  
                break
        cv2.destroyAllWindows()
        return self.missing_coordinates


def find_from_coordinates_json(picked_coordinates, folder):
    def calculate_dist(p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    
    with open(f'{folder}/coordinates.json', 'r') as f:
        result = json.load(f)
    
    
    coordinates = {int(k): [v[0], v[1]] for k, v in result.items()}
    for pick_k, pick_v in picked_coordinates.items():
        distance = float('inf')
        for v in coordinates.values():
            temp_dist = calculate_dist(pick_v, v)
            if temp_dist < distance:
                picked_coordinates[pick_k] = v
                distance = temp_dist
            else:
                continue
    return picked_coordinates


def extract_corner(surface_name):
    output_dir = 'Surface_' + surface_name
    
    file_name = output_dir + '/' + surface_name + '_crop.jpg'
    img = cv2.imread(file_name)

    
    corner_coordinates = MissingCoorinates(img).run()

    
    Left, Right = sorted(corner_coordinates)[:2], sorted(corner_coordinates)[-2:]
    LT, LB = sorted(Left, key=lambda x: x[1])[0], sorted(Left, key=lambda x: x[1])[1]
    RT, RB = sorted(Right, key=lambda x: x[1])[0], sorted(Right, key=lambda x: x[1])[1]
    dict_corner_coordinates = {x: y for x, y in zip(['LT', 'LB', 'RT', 'RB'], [LT, LB, RT, RB])}

    
    dict_corner_coordinates = find_from_coordinates_json(dict_corner_coordinates, output_dir)

    dict_corner_coordinates['img_H'] = img.shape[0]
    
    print('Four Coordinates:\n', dict_corner_coordinates)
    json_str = json.dumps(dict_corner_coordinates, indent=4)
    save_dir = output_dir + '/' + 'corner_coordinates_pixel.json'
    with open(save_dir, 'w') as json_file:
        json_file.write(json_str)


if __name__ == '__main__':
    extract_corner(surface_name='S19_0')