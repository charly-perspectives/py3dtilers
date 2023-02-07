'''
             _________________________   
            |_______OBJ-READER________|
                
'''
#https://web.cse.ohio-state.edu/~shen.94/581/Site/Lab3_files/Labhelp_Obj_parser.htm
import numpy as np

class Scene:
    def __init__(self, src_file):
        #read .obj
        self.vertex_format = 'N3F_V3F'
        self.groups = list()
        self.materials = list()
        file = open(src_file, 'r')
        line = file.readline()
        gi = gInfo(['',''], 0)
        start = 0
        vertex_index = 0
        material_index = - 1
        while line:
            subline = line.split(' ')
            token = subline[0]
            if(token=='g' and start==1):
                self.groups.append(gi.createGroup())
                material_index = -1
                gi = gInfo(subline, vertex_index)
                gi.newChunkOfFaces()
            if(token=='g' and start==0):
                start = 1
                gi = gInfo(subline, vertex_index)
                gi.newChunkOfFaces()
            if(token=='v'):
                gi.addVertex(subline)
                vertex_index += 1
            if(token=='vn'):
                gi.addNormal(subline)
            if(token=='f'):
                gi.addFace(subline, material_index)
            if(token=='usemtl'):
                gi.addMaterial(subline)
                gi.newChunkOfFaces()
                material_index += 1
            line = file.readline()
        self.groups.append(gi.createGroup())
        file.close()

        #read .mtl
        mtl_file = src_file[:-3] + 'mtl'
        file = open(mtl_file, 'r')
        line = file.readline()
        mat = Material('init')
        start = 0
        while line:
            subline = line.split(' ')
            token = subline[0]
            if(token=='newmtl' and start==1):
                self.materials.append(mat)
                mat = Material(subline[1])
            if(token=='newmtl' and start==0):
                start = 1
                mat = Material(subline[1])
            if(token=='Kd'):
                mat.r = float(subline[1])
                mat.g = float(subline[2])
                mat.b = float(subline[3])
            if(token=='d'):
                mat.a = 1 - float(subline[1])
            line = file.readline()
        self.materials.append(mat)
        file.close()

class Material:
    def __init__(self, name):
        self.name = name
        self.r = 0
        self.g = 0
        self.b = 0
        self.a = 1

class Group:
    def __init__(self, id, vertices, normals, faces, materials):
        self.id = id
        self.materials = materials
        nb_materials = len(materials)
        self.vertices= list()

        for i in range(nb_materials):
            verts = list()
            for f in faces[i]:
                i0 = f[0] - 1
                i1 = f[1] - 1
                i2 = f[2] - 1
                verts += vertices[i0]
                verts += vertices[i1]
                verts += vertices[i2]
            self.vertices.append(verts)
            

        

class gInfo:
    def createGroup(self):
        return Group(self.id, self.vertices, self.normals, self.faces, self.materials)

    def __init__(self, sline, vi):
        self.id = sline[1]
        self.vertices = list()
        self.normals = list()
        self.faces = list()
        self.materials = list()
        self.vi = vi
    
    def addVertex(self, sline):
        vertex = [np.double(sline[1]), np.double(sline[2]), np.double(sline[3])]
        self.vertices.append(vertex)
    
    def addNormal(self, sline):
        normal = [ float(sline[1]), float(sline[2]), float(sline[3])]
        self.normals.append(normal)
    
    def addFace(self, sline, material_index):
        face_vertices = []
        for strv in sline[1:]:
            subarray = strv.split('//')
            v = int(subarray[0])
            v -= self.vi
            face_vertices.append(v)
        self.faces[material_index].append(face_vertices)

    def newChunkOfFaces(self):
        face_vertices = []
        self.faces.append(face_vertices)
    
    def addMaterial(self, sline):
        self.materials.append(sline[1])
