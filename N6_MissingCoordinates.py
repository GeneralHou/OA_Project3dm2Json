import cv2
import json

def missing_coordinates(surface_name):
    output_dir = 'Surface_' + surface_name

    def shw_img(img, title='default'):
        cv2.namedWindow(title, 0)
        w, h = min(1920, img.shape[1]), min(1080, img.shape[0])
        cv2.resizeWindow(title, w, h) 
        cv2.imshow(title, img)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

    img = cv2.imread(F'{output_dir}/{surface_name}_crop.jpg')


    with open(f'{output_dir}/coordinates.json', 'r') as f:
        result = json.load(f)
        
        
        coordinates = {int(k): v for k, v in result.items()}


    with open(f'{output_dir}/coordinates_missing.json', 'r') as f:
        miss_key = json.load(f)

    for k in miss_key:
        cv2.circle(img, tuple(coordinates[k]), 20, (0,0,255), -1)
        cv2.putText(img,str(k), tuple(coordinates[k]), cv2.FONT_HERSHEY_DUPLEX, 4,(130,255,0), 8, cv2.LINE_AA)

    shw_img(img, 'The missing coordinates')
    cv2.imwrite(f'{output_dir}/N6_MissingCoord_Amount{len(miss_key)}.jpg', img)

if __name__ == '__main__':
    missing_coordinates(surface_name='1G20')