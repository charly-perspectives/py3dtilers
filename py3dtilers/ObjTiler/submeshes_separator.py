'''
             ___________________________   
            |____SUBMESHES_SEPARATOR____|
                
'''
#https://web.cse.ohio-state.edu/~shen.94/581/Site/Lab3_files/Labhelp_Obj_parser.htm
# Class definitions


class Scene:
    def __init__(self, src_file):
        self.vertex_format = 'N3F_V3F'
        file = open(src_file, 'r')
        line = file.readline()
        gi = gInfo(['',''], 0)
        start = 0
        vertex_index = 0
        while line:
            subline = line.split(' ')
            token = subline[0]
            if(token=='g' and start==1):
                self.groups.append(gi.createGroup())
                gi = gInfo(subline, vertex_index)
            if(token=='g' and start==0):
                start = 1
                gi = gInfo(subline, vertex_index)
            if(token=='v'):
                gi.addVertex(subline)
                vertex_index += 1
            if(token=='vn'):
                gi.addNormal(subline)
            if(token=='f'):
                gi.addFace(subline)
            if(token=='usemtl'):
                gi.addMaterial(subline)
            line = file.readline()
        self.groups.append(gi.createGroup())
        file.close()


class Group:
    def __init__(self, id, vertices, normals, faces, material):
        self.id = id
        self.vertices = []
        for f in faces:
            i0 = f[0]
            i1 = f[1]
            i2 = f[2]
            self.vertices += (vertices[i0] + normals[i0])
            self.vertices += (vertices[i1] + normals[i1])
            self.vertices += (vertices[i2] + normals[i2])
        self.material = material
            
    def print(self):
        print('id', self.id)
        print('vertices', self.vertices)
        print('material', self.material)

class gInfo:

    def createGroup(self):
        return Group(self.id, self.vertices, self.normals, self.faces, self.material)

    def __init__(self, sline, vi):
        self.id = sline[1]
        self.vertices = list()
        self.normals = list()
        self.faces = list()
        self.material = ''
        self.vi = vi
    
    def addVertex(self, sline):
        vertex = [ float(sline[1]), float(sline[2]), float(sline[3])]
        self.vertices.append(vertex)
    
    def addNormal(self, sline):
        normal = [ float(sline[1]), float(sline[2]), float(sline[3])]
        self.normals.append(normal)
    
    def addFace(self, sline):
        face_vertices = []
        for strv in sline[1:]:
            subarray = strv.split('//')
            v = int(subarray[0])
            v -= self.vertex_index
            face_vertices.append(v)
        self.faces.append(face_vertices)
    
    def addMaterial(self, sline):
        self.material = sline[1]

    def print(self):
        print(self.id)
        print(self.vertices)
        print(self.normals)
        print(self.faces)
        print(self.material)

src_file = 'data//normal.obj'
# file = open(src_file, 'r')

# line = file.readline()
# scene = Scene()
# gi = gInfo(['',''], 0)
# start = 0
# vertex_index = 0
# while line:
#     subline = line.split(' ')
#     token = subline[0]
#     if(token=='g' and start==1):
#         scene.groups.append(gi.createGroup())
#         gi = gInfo(subline, vertex_index)
#     if(token=='g' and start==0):
#         start = 1
#         gi = gInfo(subline, vertex_index)
#     if(token=='v'):
#         gi.addVertex(subline)
#         vertex_index += 1
#     if(token=='vn'):
#         gi.addNormal(subline)
#     if(token=='f'):
#         gi.addFace(subline)
#     if(token=='usemtl'):
#         gi.addMaterial(subline)

#     line = file.readline()
# scene.groups.append(gi.createGroup())
# file.close()

# for g in scene:
#     print(g.vertices)

scene = Scene(src_file)

print(scene.vertex_format)