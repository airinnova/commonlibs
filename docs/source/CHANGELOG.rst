Changelog
=========

Changelog for CommonLibs. Version numbers try to follow `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

[0.6.3] -- 2021-02-22
---------------------

Changed
~~~~~~~

* Change logger methods `enable()` and `disable()` to properties `on` and `off`

[0.5.2] -- 2020-05-29
---------------------

Added
~~~~~

* Added new module `commonlibs.log` module to replace `commonlibs.logger.logger` in the future

[0.5.1] -- 2020-05-01
---------------------

Removed
~~~~~~~

* Removed module `model` since moved to separate repo (https://github.com/airinnova/model-framework)

[0.5.0] -- 2020-04-15
---------------------

Removed
~~~~~~~

* Removed `dicts.schemadicts` since the module has moved to its own repo (https://github.com/airinnova/schemadict)

[0.4.2] -- 2020-03-26
---------------------

Added
~~~~~

* Add package `strings` with string manipulation tools

[0.4.1] -- 2020-03-22
---------------------

Added
~~~~~

* Added module `dicts.special` with `rangedict` class (subclass from `dict`)

[0.4.0] -- 2020-03-21
---------------------

Added
~~~~~

* Added module `models` with a prototype `PropertyHandler()` meta class for model APIs

[0.3.4] -- 2019-09-23
---------------------

Added
~~~~~

* Added support for serialising Numpy arrays in `dump_pretty_json()`

[0.3.3] -- 2019-09-19
---------------------

Changed
~~~~~~~

* Level argument in `logger.logger.init()` is determined by attribute rather than string

[0.3.2] -- 2019-09-18
---------------------

Added
~~~~~

* Added module `fileio.json` wrapper `dump_pretty_json()`

[0.3.1] -- 2019-09-18
---------------------

Added
~~~~~

* Added `get_default_value_dict()` which returns a default value dictionary from a schema dictionary

[0.3.0] -- 2019-09-17
---------------------

Added
~~~~~

* Added new module `dicts.schemadicts` for methods to check if a dictionary is conform with a schema

[0.2.2] -- 2019-09-05
---------------------

Changed
~~~~~~~

* Moved staticmethod `ProjectPaths.join_paths()` into separate function


[0.2.1] -- 2019-09-03
---------------------

Added
~~~~~

* Added methods to `ProjectPaths()`
    - `remove_path()`
    - `add_suffix()`
    - `change_suffix()`

[0.2.0] -- 2019-08-21
---------------------

Added
~~~~~

* Added `ProjectPaths()` in new module `fileio.paths` class for simpler path handling

[0.1.1] -- 2019-08-15
---------------------

Changed
~~~~~~~

* Renamed module `mathtools` to `math`

Removed
~~~~~~~

* Removed module `mathtool.rank_nullspace`

[0.1.0] -- 2019-08-13
---------------------

* First public release of `CommonLibs`

Fixed
~~~~~
