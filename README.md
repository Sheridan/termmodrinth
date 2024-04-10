# termmodrinth
A terminal utility that works with the modrinth api and downloads projects from there



Directories for storing project files will be created in the directory specified in the `storage` option. The `storage` directories store project files and their change history. The `active` directories contain projects ready to be connected. It is enough to create a symbolic link of the `active` directories to the appropriate locations. For example, like this: `ln -s ~/modrinth/resourcepacks/active ~/.minecraft/resourcepacks`


# configuration
All settings are in `termmodrinth.json`. The corresponding slugs should be added to the mods, resourcepacks, shaders lists. Slug can be found in the address bar. For example, in the address `https://modrinth.com/mod/fabric-api` the slug is `fabric-api`.

Example configuration in `termmodrinth.json.example`

Add the `#` symbol at the beginning of the lists item to ignore it

## explain
### root section
* Projects slugs lists. Slug - project tag, used on modrinth. For example, in the address `https://modrinth.com/mod/fabric-api` the slug is `fabric-api`
```json
  "mods":
  [
    "accurate-block-placement-reborn",
    "#inventorio",
    "#iris",
    "world-play-time"
  ],
  "resourcepacks":
  [
    "3d-crops",
    "3d-items-mintynoura",
    "better-enchanted-book",
    "#xalis-potion",
  ],
  "shaders":
  [
    "bsl-shaders",
    "#noble",
    "shrimple",
    "soft-voxels-lite"
  ]
```
* `"storage"`: storage path. The `active` directories contain projects ready to be connected. It is enough to create a symbolic link of the `active` directories to the appropriate locations. For example, like this: `ln -s /tmp/modrinth/resourcepacks/active ~/.minecraft/resourcepacks`
* `"threads"`: update threads. Speeds up the download

### `"modrinth"` section

* `"max_queries_per_minute"`: Maxinum API queries per minute. Modrinth limit: 300
* Supported minecraft versions per project type. Order matters, script will try to download a newer one
```json
    "minecraft_versions":
    {
      "mods":
      [
        "1.20.4"
      ],
      "resourcepacks":
      [
        "1.20.4",
        "1.20.3",
        "1.20.2",
        "1.20.1",
        "1.20",
        "1.19.2"
      ],
      "shaders":
      [
        "1.20.4",
        "1.20.3"
      ]
    }
```
* Supported loader per project type:
```json
    "loader":
    {
      "mods": "fabric",
      "resourcepacks": "minecraft",
      "shaders": "iris"
    }
```
* Project dependencies types for downloading:
```json
    "request_dependencies":
    [
      "required",
      "#optional"
    ]
```
* Download only primary files. Some projects have several files included in the release. One of them is the primary.
```json
    "primaries_only":
    {
      "mods": true,
      "resourcepacks": false,
      "shaders": true
    }
```
* When not only primaries files downloading try not download source code archives
```json
    "try_not_download_sources":
    {
      "mods": true,
      "resourcepacks": true,
      "shaders": true
    }
```
* Unused modrinth auth
```json
    "user":
    {
      "login": "",
      "password": ""
    }
```
# TODO
Wait for the opportunity to work with custom lists on morinth and synchronize the project lists with them
