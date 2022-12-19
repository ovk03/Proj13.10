"""functions to convert files to game data"""

import pathlib
from .structures import tri_normal

"""Onni Kolkka 
150832953 (student number)
created 16.12.2022 13.32
"""

# designed for blender exported .obj files. May not be compatible with every .obj file
def obj_parse(path):
    """reads and parses .obj file"""
    with open(path) as file:
        string=file.read()
        vertices=[]
        polygons=[]
        mats={}
        current_mat=""
        for i in string.split("\n"):
            if len(i) == 0: continue
            if i[0:6] == "mtllib":mats=mtl_parse(pathlib.Path(path).parent.joinpath(pathlib.Path(path).name[0:-4]+".mtl"))
            if i[0:2] == "v ":
                coords=i.split(" ")
                vertices.append((float(coords[1]),float(coords[2]),float(coords[3])))
            elif len(vertices)==0:
                continue
            elif i[0:6] == "usemtl":
                current_mat = i.split()[1]
            elif current_mat == "":
                continue
            elif i[0]=="f":
                face=i.split(" ")[1:]
                final_polygon=[]
                for f in face:
                    f=f.split("/")[0]
                    final_polygon.extend(vertices[int(f)-1])
                while len(final_polygon)<12:
                    print("filling tri to quad")
                    final_polygon.extend(final_polygon[0:3])

                normal = tri_normal(tuple(final_polygon[0:9]))
                polygons.append((*final_polygon[0:12],*mats[current_mat],*normal))

        print(len(polygons[0]))
        return polygons

# designed for blender exported .mtl files. May not be compatible with every .mtl file
def mtl_parse(path):
    """reads and parses .mtl file"""
    with open(path) as file:
        string=file.read()
        mats={}
        current_mat=""
        for i in string.split("\n"):
            if i[0:6] == "newmtl":
                current_mat = i.split()[1]
            if i[0:2] == "Kd":
                mats[current_mat]=(int(float(i.split()[1])*216),
                                   int(float(i.split()[2])*216),
                                   int(float(i.split()[3])*216))
        print(mats)
        return mats
