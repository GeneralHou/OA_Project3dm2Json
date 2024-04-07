import json
import cv2





def shw_img(img, title='default'):
    cv2.namedWindow(title, 0)
    w, h = min(1920, img.shape[1]), min(1080, img.shape[0])
    cv2.resizeWindow(title, w, h) 
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def trans_scale(surface_name):
    output_dir = 'Surface_' + surface_name
    '''''''''LOAD COORDINATES'''''''''
    
    with open(f'{output_dir}/corner_coordinates_pixel.json', 'r') as f:
        result = json.load(f)
    img_H = result['img_H']  
    pixel_corner_coordinates_temp = [result['LB'], result['RT']]
    
    pixel_corner_coordinates = [[x, img_H - y] for x, y in pixel_corner_coordinates_temp]

    
    
    with open(f'{output_dir}/coordinates.json', 'r') as f:
        result = json.load(f)
    
    
    coordinates = {int(k): [v[0], img_H-v[1]] for k, v in result.items()}

    
    with open(f'{output_dir}/corner_coordinates_real.json', 'r') as f:
        result = json.load(f)
    real_corner_coordinates = [result['LB'], result['RT']]

    '''''''''AID FUNCTION'''''''''
    
    def align_coordinates(coordinate):
        align_crd = {}
        for i in range(len(coordinate)):
            temp = [coordinate[i][0] - mv_x, coordinate[i][1] - mv_y]
            align_crd[i] = temp
        return align_crd


    '''''''''ADJUST TRANS DISTANCE'''''''''
    
    pixel_lf_bt = pixel_corner_coordinates[0]
    real_lf_bt = real_corner_coordinates[0]
    mv_x = pixel_lf_bt[0] - real_lf_bt[0]
    mv_y = pixel_lf_bt[1] - real_lf_bt[1]
    print(f'■■■PART ONE: The default translate in x and y direction: {mv_x}, {mv_y}')
    
    print("Adjust the trans distance above when can't fully project to get z coordinate.")
    print("Coordinate system is same as Gaussian coordinate in Rhino.")
    adjust_x = input("Adjust in x direction['Enter' to confirm or quit]:")
    adjust_y = input("Adjust in y direction['Enter' to confirm or quit]:")
    if adjust_x: mv_x = mv_x - float(adjust_x)  
    if adjust_y: mv_y = mv_y - float(adjust_y)

    
    aligned_coordinates = align_coordinates(coordinates)


    '''''''''ADJUST SCALE FACTOR'''''''''
    
    aligned_corner = align_coordinates(pixel_corner_coordinates)

    
    scale_factor_x = (aligned_corner[1][0]-aligned_corner[0][0])/(real_corner_coordinates[1][0]-real_corner_coordinates[0][0])
    scale_factor_y = (aligned_corner[1][1]-aligned_corner[0][1])/(real_corner_coordinates[1][1]-real_corner_coordinates[0][1])
    print(f'\n■■■PART TWO: The default scale factor in x and y direction: {scale_factor_x}, {scale_factor_y}')
    
    print("Adjust the scale factor above when can't fully project to get z coordinate.")
    new_factor_x = input("Adjust in x direction['Enter' to confirm or quit]:")
    new_factor_y = input("Adjust in y direction['Enter' to confirm or quit]:")
    new_factor_x = float(new_factor_x) if new_factor_x else scale_factor_x  
    new_factor_y = float(new_factor_y) if new_factor_y else scale_factor_y

    
    scaled_coordinates = {}
    for i in range(len(aligned_coordinates)):
        temp_x = (aligned_coordinates[i][0] - aligned_corner[0][0]) / new_factor_x + real_corner_coordinates[0][0]
        temp_y = (aligned_coordinates[i][1] - aligned_corner[0][1]) / new_factor_y + real_corner_coordinates[0][1]
        scaled_coordinates[i] = [round(temp_x, 2), round(temp_y, 2), 0]
    
    
    '''''''''SAVE FINAL RESULT'''''''''
    json_str = json.dumps(scaled_coordinates, indent=4)
    save_dir = output_dir + '/' + 'coordinates_TSed.json'
    with open(save_dir, 'w') as json_file:
        json_file.write(json_str)


if __name__ == '__main__':
    trans_scale(surface_name='4-000')