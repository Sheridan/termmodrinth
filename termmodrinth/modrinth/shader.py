from termmodrinth.modrinth.project import ModrinthProject

class ModrinthShader(ModrinthProject):
  def __init__(self, slug):
    super().__init__(slug, "shader")
