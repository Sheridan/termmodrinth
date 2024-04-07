from termmodrinth.modrinth.project import ModrinthProject

class ModrinthMod(ModrinthProject):
  def __init__(self, slug):
    super().__init__(slug, "mod")
