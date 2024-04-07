from termmodrinth.modrinth.mod import ModrinthMod
from termmodrinth.modrinth.resourcepack import ModrinthResourcePack
from termmodrinth.modrinth.shader import ModrinthShader

project_types = {
  'mod': {
    'class': ModrinthMod,
    'extention': '.jar'
  },
  'resourcepack': {
    'class': ModrinthResourcePack,
    'extention': '.zip'
  },
  'shader': {
    'class': ModrinthShader,
    'extention': '.zip'
  }
}
