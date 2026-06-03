import numpy as np
from dataclasses import dataclass, field
from ctypes import c_uint32, byref

from OpenGL.GL import *  # type: ignore
from pyglm import glm  # type: ignore

from shader import Shader

MAX_BONE_INFLUENCE: int = 4


@dataclass
class Vertex:
    Position: glm.vec3 = field(default_factory=lambda: glm.vec3(0))
    Normal: glm.vec3 = field(default_factory=lambda: glm.vec3(0))
    TexCoords: glm.vec2 = field(default_factory=lambda: glm.vec2(0))
    Tangent: glm.vec3 = field(default_factory=lambda: glm.vec3(0))
    Bitangent: glm.vec3 = field(default_factory=lambda: glm.vec3(0))
    m_BoneIDs: list[int] = field(default_factory=lambda: [0] * MAX_BONE_INFLUENCE)
    m_Weights: list[float] = field(default_factory=lambda: [0.0] * MAX_BONE_INFLUENCE)


@dataclass
class Texture:
    id: int
    type_: str
    path: str


class Mesh:
    # mesh Data
    vertices: list[Vertex]
    indices: list[int]
    textures: list[Texture]
    VAO: int

    # constructor
    def __init__(self, vertices: list[Vertex], indices: list[int], textures: list[Texture]):
        self.vertices = vertices
        self.indices = indices
        self.textures = textures

        self.VAO = 0
        self._VBO = 0
        self._EBO = 0

        # now that we have all the required data, set the vertex buffers and its attribute pointers.
        self.setupMesh()

    # render the mesh
    def draw(self, shader: Shader):
        diffuseNr: int = 1
        specularNr: int = 1
        normalNr: int = 1
        heightNr: int = 1

        for i, texture in enumerate(self.textures):
            number: str = ""
            name = texture.type_

            if name == "texture_diffuse":
                number = f"{diffuseNr}"
                diffuseNr += 1
            elif name == "texture_specular":
                number = f"{specularNr}"
                specularNr += 1
            elif name == "texture_normal":
                number = f"{normalNr}"
                normalNr += 1
            elif name == "texture_height":
                number = f"{heightNr}"
                heightNr += 1

            glUniform1i(glGetUniformLocation(shader.id, name + number), i)
            # Use DSA texture binding
            glBindTextureUnit(i, texture.id)

        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    def setupMesh(self):
        # Convert vertex data to a flat numpy array for OpenGL
        # Each vertex has: Pos(3), Normal(3), Tex(2), Tangent(3), Bitangent(3) = 14 floats
        vertex_data = []
        for v in self.vertices:
            vertex_data.extend([v.Position.x, v.Position.y, v.Position.z])
            vertex_data.extend([v.Normal.x, v.Normal.y, v.Normal.z])
            vertex_data.extend([v.TexCoords.x, v.TexCoords.y])
            vertex_data.extend([v.Tangent.x, v.Tangent.y, v.Tangent.z])
            vertex_data.extend([v.Bitangent.x, v.Bitangent.y, v.Bitangent.z])

        v_array = np.array(vertex_data, dtype=np.float32)
        i_array = np.array(self.indices, dtype=np.uint32)

        self.VAO = c_uint32(0)
        self._VBO = c_uint32(0)
        self._EBO = c_uint32(0)

        glCreateVertexArrays(1, byref(self.VAO))
        glCreateBuffers(1, byref(self._VBO))
        glCreateBuffers(1, byref(self._EBO))

        # Use glNamedBufferStorage for DSA buffer allocation
        glNamedBufferStorage(self._VBO, v_array.nbytes, v_array, GL_DYNAMIC_STORAGE_BIT)
        glNamedBufferStorage(self._EBO, i_array.nbytes, i_array, GL_DYNAMIC_STORAGE_BIT)

        # Bind VBO to binding point 0
        stride = 14 * v_array.itemsize
        glVertexArrayVertexBuffer(self.VAO, 0, self._VBO, 0, stride)
        # Bind EBO to VAO
        glVertexArrayElementBuffer(self.VAO, self._EBO)

        # Attribute definitions using DSA
        # vertex Positions
        glEnableVertexArrayAttrib(self.VAO, 0)
        glVertexArrayAttribFormat(self.VAO, 0, 3, GL_FLOAT, GL_FALSE, 0)
        glVertexArrayAttribBinding(self.VAO, 0, 0)

        # vertex normals
        glEnableVertexArrayAttrib(self.VAO, 1)
        glVertexArrayAttribFormat(self.VAO, 1, 3, GL_FLOAT, GL_FALSE, 3 * v_array.itemsize)
        glVertexArrayAttribBinding(self.VAO, 1, 0)

        # vertex texture coords
        glEnableVertexArrayAttrib(self.VAO, 2)
        glVertexArrayAttribFormat(self.VAO, 2, 2, GL_FLOAT, GL_FALSE, 6 * v_array.itemsize)
        glVertexArrayAttribBinding(self.VAO, 2, 0)

        # vertex tangent
        glEnableVertexArrayAttrib(self.VAO, 3)
        glVertexArrayAttribFormat(self.VAO, 3, 3, GL_FLOAT, GL_FALSE, 8 * v_array.itemsize)
        glVertexArrayAttribBinding(self.VAO, 3, 0)

        # vertex bitangent
        glEnableVertexArrayAttrib(self.VAO, 4)
        glVertexArrayAttribFormat(self.VAO, 4, 3, GL_FLOAT, GL_FALSE, 11 * v_array.itemsize)
        glVertexArrayAttribBinding(self.VAO, 4, 0)
        glVertexArrayAttribFormat(self.VAO, 4, 3, GL_FLOAT, GL_FALSE, 11 * v_array.itemsize)
        glVertexArrayAttribBinding(self.VAO, 4, 0)
