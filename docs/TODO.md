# TODO

## fileio.paths
* `ProjectPaths()`
    * Make `join_path()` function more general (any number of paths)
    * Separate `join_path()` function outside of `ProjectPaths()`

## math.interpolation
* `lin_interpol()`
    * Change order: x12, y12

## dicts.schemadicts
* Add function `check_schema_dict()` --> Make sure that schema itself has a correct format

## strings.strings
* Improve string manipulation functions
* Functions which modify file content could be placed in `fileio` instead (!?)

## model.model
* Let `PropertyHandler()` subclass from `dict` for more consistent storage of dictionary data and overwrite set/get methods?
* Add option to attach "actions" when data is set/added using `set()` or `add()`
    * Separate method like `_add_action(key, action, *args, **kwargs)` where `action` is callable OR
    * Set during `_add_prop_spec(..., action=..., ...)`

## Documentation
* Add documentation

## Testing
* Add test cases
