import logging
from pathlib import Path
from ctypes import c_uint32, byref

import pyassimp as pyassimp
from PIL import Image
from OpenGL.GL import *  # type: ignore
from pyglm import glm  # type: ignore

from pyassimp.structs import Scene, Node, Mesh as AssimpMesh, Material
from pyassimp.errors import AssimpError
from pyassimp.material import (
    aiTextureType_DIFFUSE,
    aiTextureType_SPECULAR,
    aiTextureType_NORMALS,
    aiTextureType_HEIGHT,
    aiTextureType_AMBIENT,
    aiTextureType_EMISSIVE,
)
from pyassimp.postprocess import (
    aiProcess_Triangulate,
    aiProcess_GenSmoothNormals,
    aiProcess_FlipUVs,
    aiProcess_CalcTangentSpace,
)

from mesh import Mesh, Vertex, Texture


class Model:
    def __init__(self, path: str, gamma: bool = False):
        self.meshes: list[Mesh] = []
        self.directory: str = ""
        self.textures_loaded: list[Texture] = []
        self.gamma_correction = gamma
        self._load_model(path)

    def draw(self, shader):
        for mesh in self.meshes:
            mesh.draw(shader)

    def _load_model(self, path: str):
        processing = aiProcess_Triangulate | aiProcess_GenSmoothNormals | aiProcess_FlipUVs | aiProcess_CalcTangentSpace
        try:
            with pyassimp.load(path, processing=processing) as scene:
                self.directory = str(Path(path).parent)
                self._process_node(scene.rootnode, scene)
        except AssimpError as e:
            logging.error(f"ERROR::ASSIMP:: {e}")

    def _process_node(self, node: Node, scene: Scene):
        for mesh in node.meshes:
            self.meshes.append(self._process_mesh(mesh, scene))

        for child in node.children:
            self._process_node(child, scene)

    def _process_mesh(self, mesh: AssimpMesh, scene: Scene):
        vertices: list[Vertex] = []
        indices: list[int] = []
        textures: list[Texture] = []

        for i, v in enumerate(mesh.vertices):
            vertex = Vertex()
            vertex.Position = glm.vec3(*v)

            if mesh.normals is not None and len(mesh.normals) > i:
                vertex.Normal = glm.vec3(*mesh.normals[i])

            if mesh.texturecoords is not None and len(mesh.texturecoords) > 0:
                vertex.TexCoords = glm.vec2(mesh.texturecoords[0][i][0], mesh.texturecoords[0][i][1])
                
                if mesh.tangents is not None and len(mesh.tangents) > i:
                    vertex.Tangent = glm.vec3(*mesh.tangents[i])
                if mesh.bitangents is not None and len(mesh.bitangents) > i:
                    vertex.Bitangent = glm.vec3(*mesh.bitangents[i])
            else:
                vertex.TexCoords = glm.vec2(0.0)

            vertices.append(vertex)

        for face in mesh.faces:
            for index in face:
                indices.append(index)

        material = scene.materials[mesh.materialindex]

        # 1. diffuse maps
        diffuse_maps = self._load_material_textures(material, aiTextureType_DIFFUSE, "texture_diffuse")
        textures.extend(diffuse_maps)
        # 2. specular maps
        specular_maps = self._load_material_textures(material, aiTextureType_SPECULAR, "texture_specular")
        textures.extend(specular_maps)
        # 3. normal maps
        normal_maps = self._load_material_textures(material, aiTextureType_HEIGHT, "texture_normal")
        textures.extend(normal_maps)
        # 4. height maps
        height_maps = self._load_material_textures(material, aiTextureType_AMBIENT, "texture_height")
        textures.extend(height_maps)

        return Mesh(vertices, indices, textures)

    def _load_material_textures(self, mat: Material, type_: int, type_name: str) -> list[Texture]:
        textures: list[Texture] = []
        
        # Pyassimp material properties is a dict. 
        # For textures, keys are often like ('file', <semantic_index>)
        # Since we import constants like aiTextureType_DIFFUSE (which is 1), 
        # we can use type_ directly as the semantic index.
        
        file_path = mat.properties.get(('file', type_))
        
        if file_path:
            # Check if already loaded
            skip = False
            for loaded in self.textures_loaded:
                if loaded.path == file_path:
                    textures.append(loaded)
                    skip = True
                    break
            
            if not skip:
                texture_id = load_texture(f"{self.directory}/{file_path}")
                texture = Texture(texture_id, type_name, file_path)
                textures.append(texture)
                self.textures_loaded.append(texture)
                    
        return textures


def load_texture(path: str) -> int:
    texture_id = c_uint32(0)
    glCreateTextures(GL_TEXTURE_2D, 1, byref(texture_id))
    
    try:
        img = Image.open(path).convert("RGBA").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
        glTextureParameteri(texture_id, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTextureParameteri(texture_id, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTextureParameteri(texture_id, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTextureParameteri(texture_id, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glTextureStorage2D(texture_id, 1, GL_RGBA8, img.width, img.height)
        glTextureSubImage2D(texture_id, 0, 0, 0, img.width, img.height, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())
        glGenerateTextureMipmap(texture_id)
        
        return int(texture_id.value)
    except Exception as e:
        logging.error(f"Texture failed to load at path: {path} - {e}")
        return 0
