# Contributing and Extending arcpy_metadata

## Extending the library to new metadata properties
Extending arcpy metadata to support additional metadata properties can vary in complexity, but is often an
easy way to get started contributing. If you need it to support additional attributes feel free to fork
the code, extend it, and submit a pull request with the changes. Please be aware that by submitting a
pull request, you are agreeing to allow submitted work to be licensed under our existing MIT license.

### Adding string fields
String fields can be added by updating `elements.py` with the correct information. In most cases, adding a key to the
dictionary `elements` with the name to be used on the metadata object (so an item accessed via `metadata.abstract` 
would be just `"abstract"`). That key should then have another dictionary as its value with at least two keys of its own.
The following is the full definition for the `abstract` attribute:

```python
    "abstract": {
        "path": "dataIdInfo/idAbs",
        "type": "string"},
```

Note that it includes a path and a data type. The data type in this case is simple, just "string" indicating it takes a string
or text value, but in other cases, such as nested lists, it can be a reference to an object (which is a subject that will need
to be covered in more detail later). The path refers not to how to access the data in ArcCatalog, but to where the value is stored
in XML exported by the ArcGIS Export Metadata tool. If you're not sure of the path of metadata you're interested in extending
arcpy_metadata to include, try setting a unique value for that field on a dataset, export the metadata Export Metadata,
and then open the exported XML and find the value you set. The nested set of XML tags will be the path (each element separated by /).

Ideally, new elements will have unit tests associated with them, though we haven't established any formal requirements yet. It's
possible a reviewer will ask for tests before merging a pull, but if you're uncertain on how to write tests, but have extended the
library, feel free to submit a pull request and one of us will try to help with creating tests. However, we do require that you
update the main README document to include the newly added element before your pull request will be accepted.

More to come later on adding more complex elements, such as those with multiple values.
