from typing import Final

aiProcess_CalcTangentSpace: Final[int] = 0x1
aiProcess_JoinIdenticalVertices: Final[int] = 0x2
aiProcess_MakeLeftHanded: Final[int] = 0x4
aiProcess_Triangulate: Final[int] = 0x8
aiProcess_RemoveComponent: Final[int] = 0x10
aiProcess_GenNormals: Final[int] = 0x20
aiProcess_GenSmoothNormals: Final[int] = 0x40
aiProcess_SplitLargeMeshes: Final[int] = 0x80
aiProcess_PreTransformVertices: Final[int] = 0x100
aiProcess_LimitBoneWeights: Final[int] = 0x200
aiProcess_ValidateDataStructure: Final[int] = 0x400
aiProcess_ImproveCacheLocality: Final[int] = 0x800
aiProcess_RemoveRedundantMaterials: Final[int] = 0x1000
aiProcess_FixInfacingNormals: Final[int] = 0x2000
aiProcess_SortByPType: Final[int] = 0x8000
aiProcess_FindDegenerates: Final[int] = 0x10000
aiProcess_FindInvalidData: Final[int] = 0x20000
aiProcess_GenUVCoords: Final[int] = 0x40000
aiProcess_TransformUVCoords: Final[int] = 0x80000
aiProcess_FindInstances: Final[int] = 0x100000
aiProcess_OptimizeMeshes: Final[int] = 0x200000
aiProcess_OptimizeGraph: Final[int] = 0x400000
aiProcess_FlipUVs: Final[int] = 0x800000
aiProcess_FlipWindingOrder: Final[int] = 0x1000000
aiProcess_SplitByBoneCount: Final[int] = 0x2000000
aiProcess_Debone: Final[int] = 0x4000000

aiProcess_GenEntityMeshes: Final[int] = 0x100000
aiProcess_OptimizeAnimations: Final[int] = 0x200000
aiProcess_FixTexturePaths: Final[int] = 0x200000
aiProcess_EmbedTextures: Final[int] = 0x10000000

aiProcess_ConvertToLeftHanded: Final[int] = (
    aiProcess_MakeLeftHanded | aiProcess_FlipUVs | aiProcess_FlipWindingOrder | 0
)

aiProcessPreset_TargetRealtime_Fast: Final[int] = (
    aiProcess_CalcTangentSpace
    | aiProcess_GenNormals
    | aiProcess_JoinIdenticalVertices
    | aiProcess_Triangulate
    | aiProcess_GenUVCoords
    | aiProcess_SortByPType
    | 0
)

aiProcessPreset_TargetRealtime_Quality: Final[int] = (
    aiProcess_CalcTangentSpace
    | aiProcess_GenSmoothNormals
    | aiProcess_JoinIdenticalVertices
    | aiProcess_ImproveCacheLocality
    | aiProcess_LimitBoneWeights
    | aiProcess_RemoveRedundantMaterials
    | aiProcess_SplitLargeMeshes
    | aiProcess_Triangulate
    | aiProcess_GenUVCoords
    | aiProcess_SortByPType
    | aiProcess_FindDegenerates
    | aiProcess_FindInvalidData
    | 0
)

aiProcessPreset_TargetRealtime_MaxQuality: Final[int] = (
    aiProcessPreset_TargetRealtime_Quality
    | aiProcess_FindInstances
    | aiProcess_ValidateDataStructure
    | aiProcess_OptimizeMeshes
    | 0
)
