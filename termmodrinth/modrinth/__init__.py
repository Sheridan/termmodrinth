from termmodrinth.modrinth.mod import ModrinthMod
from termmodrinth.modrinth.resourcepack import ModrinthResourcePack
from termmodrinth.modrinth.shader import ModrinthShader

project_types = {
  'mod': {
    'class': ModrinthMod
  },
  'resourcepack': {
    'class': ModrinthResourcePack
  },
  'shader': {
    'class': ModrinthShader
  }
}
