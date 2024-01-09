# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.1] - 2023-12-07
### Changed
 - optional shapely dependency moved to main dependency group

## [0.6.0] - 2023-04-19
### Removed
 - geopandas dependency

 ### Changed
 - function get_backarc_polygon() renamed to backarc_polygon()
## [0.5.1] - 2023-04-18
### Removed
 - BACKARC_POLYGON no longer declared in geometry.py see https://github.com/GNS-Science/nzshm-common-py/issues/29
 - updated project dependency group geometry

## [0.5.0] - 2023-04-17
### Changed
 - update optional geopandas version
 - location_by_id() retuns None if code doesn't exist
 - LOCATIONS and LOCATION_LISTS
 - included support for python 3.10

### Added
 - add Hawkes Bay locatons with vs30s
 - add SRWG214 locations
 - function to create backarc polygon
 - backarc polygon
 - add BACKARC_POLYGON constant (note requires optional geopandas dependency)

## [0.4.0] - 2022-09-27
### Changed
 - updated temporary codes (xxN) used for some locations to use Z prefix
### Added
 - added Whangarei to locations list

## [0.3.2] - 2022-08-18
### Added
 - extras [geometry] to provide geometry helper

### Changed
 - github actions config
 - tox setup
 - project metadata

### Removed
  - python 3.7 support (pandas)

## [0.2] - 2022-08-10

### Added
 - util.compression module
 - tox setup

## [0.1.2] - 2022-08-10

### Added
 - ROT Rotorua to LOCATIONS
 - Added ROT to NZ main cities

## [0.1.1] - 2022-08-01

### Changed
 - fix lat-lon order for grid enums
 - move to semantic versioning
   next logical version was 1.1.0, but this is not appropriate, as the public API is still fluid (see https://devhints.io/semver)

## [1.1.0] - 2022-08-01

### Added
 - NZ_0_1_NB_1_0 0.1 grid ENUM matching the CSV data used before this release
 - NZ_0_1_NB_1_1 0.1 grid ENUM matching the new latest generation data.
 - added this changelog file.
