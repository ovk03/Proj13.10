"""functions to convert files to game data"""
"""Onni Kolkka 
150832953 (student number)
created 16.12.2022 13.32
"""

def obj_parse(string):
    vertices=[]
    polygons=[]
    for i in string.split("\n"):
        if(len(i)==0): continue
        if i[0:2]=="v ":
            coords=i.split(" ")
            vertices.append((float(coords[1]),float(coords[2]),float(coords[3])))
        elif len(vertices)==0:
            continue
        elif i[0]=="f":
            face=i.split(" ")[1:]
            final_polygon=[]
            for f in face:
                f=f.split("/")[0]
                final_polygon.extend(vertices[int(f)-1])
            polygons.append(tuple(final_polygon))
    return polygons
