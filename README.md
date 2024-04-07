※※※※※※※
Please prepare three files:   
***.3dm   
***_crop.png(from FindCoordinate)
coordinates.json

Step1: before start, please put '.3dm' under the directory of 'Trans3dm3json
       
Step2: then create a directory named 'Surface_surface_name' in the same level directory of this file(N0_RunMeOnly.py)
       e.g.: if the surface_name is D23(or S19), then the name of the directory should be: Surface_D23(or Surface_S19)

Step3: put the corresponding .png(the synthesized grid image after crop) and the coordinates.json under the directory above

Step4: open N0_RunMeOnly.py and change the string pass to variable "surface_name"

Step5: click Run

