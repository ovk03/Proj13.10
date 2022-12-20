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
        normals=[]
        polygons=[]
        mats={}
        current_mat=""
        for i in string.split("\n"):
            if len(i) == 0: continue
            if i[0:6] == "mtllib":mats=mtl_parse(pathlib.Path(path).parent.joinpath(pathlib.Path(path).name[0:-4]+".mtl"))
            if i[0:2] == "v ":
                coords=i.split(" ")
                vertices.append((float(coords[1]),float(coords[2]),float(coords[3])))
            elif i[0]=="f":
                face=i.split(" ")[1:]
                final_polygon=[]
                normal=(0,0,0)
                for f in face:
                    f=f.split("/")
                    final_polygon.extend(vertices[int(f[0])-1])
                    normal=(normals[int(f[2])-1][0]+normal[0],
                            normals[int(f[2])-1][1]+normal[1],
                            normals[int(f[2])-1][2]+normal[2])

                while len(final_polygon)<12:
                    final_polygon.extend(final_polygon[0:3])

                if normal[0]==0 and normal[1] == 0 and normal[2] == 0:
                    normal = tri_normal(tuple(final_polygon[0:9]))

                polygons.append((*final_polygon[0:12],*mats[current_mat],*normal))
            elif i[0:2] == "vn":
                vector=i.split(" ")
                normals.append((float(vector[1]),float(vector[2]),float(vector[3])))
            elif i[0:6] == "usemtl":
                current_mat = i.split()[1]
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
        return mats
