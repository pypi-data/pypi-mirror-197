# Changelog

## [Unreleased]

## [0.7.3] 2023-03-17

### Fixed
- Fixed some attribute errors breaking package generation.

## [0.7.1] 2023-03-04

### Fixed
- Re-merged importmod_core into importmod setup.py. For the moment, importmod_core can optionally
  be installed by itself when installing manually, but otherwise is just part of importmod.

## [0.7.0] 2023-03-03

### Dependencies
- core: Depends on prompt_toolkit and tomlkit

### Added
- install subcommand (core). This lets you interactively install mods into a portmod prefix and set them up to
  work with configtool.
- `--interactive` argument has been added to the `importmod import` subcommand.
  This will prompt for unknown information, and let you change metadata which
  has been auto-detected.
- Added internal function for updating all packages in a repository.

### Fixed
- Fixed NEXUS_SRC_URI formatting during package generation

### Changed
- Split into importmod and importmod_core. The former has fewer dependencies and exposes a new install subcommand.

## [0.6.0] 2022-07-18

### Dependencies
- Updated to work with portmod 2.4

### Added
- `ruamel.yaml` and `pypi-simple` have been added as dependencies.
- `importmod import` can now take package atoms as an argument, for generating updates to existing packages.
- `importmod import` can now generate packages from Gitlab, Github and pypi releases.
- Updates from specific NexusMods files can now be detected for packages using `NEXUS_SRC_URI`.
  If this is used without NEXUS_URL, the updater will ignore other files from the project page.
- A new `importmod update` subcommand can be used for generating pybuilds for out of date packages in a
  repository, in addition to explicit update information (currently required for the update subcommand)
  which can be specified in the package's `metadata.yaml` to indicate where to pull updates from.

### Changed
- Generation of `metadata.yaml` will no longer overwrite existing data. This requires `ruamel.yaml` as a
  dependency.

### Fixed
- When importing from Nexusmods files marked as archived will no longer be considered

## [0.5.0] 2021-09-27

### Added
- Added `longdescription`, `bugs_to` and `doc` to `create_metadata`
- Added support for `NEXUS_SRC_URI` to generator

### Changed
- [DeltaPlugin](https://gitlab.com/bmwinger/delta-plugin) is now a requirement when determining
  plugin masters. Importmod now supports all ESP versions.
- `get_updates` now can be filtered to a specific repository using the `repository` argument.

### Bugfixes
- Fixed invalid commas in lists of InstallDirs when generating packages
- Fixed version comparison of packages from NexusMods when the remote version is equivalent
  but not exactly the same string.
- Fixed GitHub update checker raising an exception if there are no releases
- File changes on NexusMod files will now be ignored if they are older than the last time the
  package was modified.
- Generated longdescription in `metadata.yaml` will now be quoted so that descriptions with colons
  do not produce invalid yaml.

## [0.4.0] 2021-05-31

### Dependencies
- Removed dependency on outdated omwcmd by re-implemented the function it was needed for in python.
- Updated to work with portmod 2.0_rc10

### New
- Added update checking for packages hosted on GitLab and GitHub.
  This only works when checking for updates of all packages, not for checking packages
  updated within a period.
- Added detection of file changes on Nexus even without version bumps

### Changed
- InstallDirs in the package generator output will be sorted by source file name and path.

### Bugfixes
- Made the update checker report the newest version of a package in the database,
  rather than the first version encountered

## [0.3.0] 2020-06-25

### Dependencies
- Requires RedBaron

### New Features
- Made pybuild generation use old version as a starting point.
- Refactored interface to use `importmod` as main command, with subcommands for importing mods and update detection.
- Added subcommand to validate NexusMods files (i.e. check that the files in the portmod repo match the files on NexusMods).
- Added subcommand to scan textures to determine a texture size that can be used in Portmod.

### Bugfixes
- Fixed bug in parsing updates from mw.modhistory.com
- Fixed parsing of version numbers and atoms from NexusMods
- Fixed handling of exceptions when parsing NexusMods mods
- Fixed incorrect separator in update output
- Use source name (minus extension) in InstallDir.S when generating pybuilds
- Parse numeric components of atoms as integers to remove leading zeroes.
- Fixed suffix parsing so that "_alpha" suffixes aresn't considered corruptions of "_p"
- Ignore old versions of Nexus files when detecting the latest version numbers
  (Oddly, some mods have old versions with larger version numbers).
- Fixed omwcmd dds command syntax to match newest version.
