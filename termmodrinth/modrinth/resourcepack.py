from termmodrinth.modrinth.project import ModrinthProject

class ModrinthResourcePack(ModrinthProject):
  def __init__(self, slug):
    super().__init__(slug, "resourcepack")
