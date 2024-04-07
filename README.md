# termmodrinth
A console utility that works with the modrinth api and downloads projects from there

All settings are in `termmodrinth.json`. The corresponding slugs should be added to the mods, resourcepacks, shaders lists. Slug can be found in the address bar. For example, in the address `https://modrinth.com/mod/fabric-api` the slug is `fabric-api`.

Directories for storing project files will be created in the directory specified in the `storage` option. The `storage` directories store project files and their change history. The `active` directories contain projects ready to be connected. It is enough to create a symbolic link of the `active` directories to the appropriate locations. For example, like this: `ln -s ~/modrinth/resourcepacks/active ~/.minecraft/resourcepacks`

The `minecraft_versions` option should specify a list of compatible versions of minecraft. The script will try to download projects following this list in order.

The `#` symbol at the beginning of the project slug is preventing the loading of this project (mod, resource pack...)

`primaries_only` - download only primary files

`try_not_download_sources` - try not to download source code files when allowed downloading not only primary files (there is no obvious sign, i can only focus on the file name)

`request_dependencies` - which type of dependencies should be downloaded

# TODO
Wait for the opportunity to work with custom lists on morinth and synchronize the project lists with them
