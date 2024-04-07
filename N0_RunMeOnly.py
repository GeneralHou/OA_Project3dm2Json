import N1_Trans3dm2json
import N2_ExtractCorner_real
import N3_ExtractCorner_pixel
import N4_TransScale

'''when processing different surface, change the name below and click run then'''
surface_name = '1G20'  


output_dir = 'Surface' + '_' + surface_name


N1_Trans3dm2json.trans_3dm_2_json(surface_name)


N2_ExtractCorner_real.extract_corner(surface_name)


N3_ExtractCorner_pixel.extract_corner(surface_name)


N4_TransScale.trans_scale(surface_name)
