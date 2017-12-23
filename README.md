# ida-namer
Automatically rename structures, and hopefully more later.

Note: this is currently documenting code that is not yet actually written!

This plugin reserves for itself a small namespace in non-repeatable comments on structures, structure elements, and data.  All such comments that contain a line beginning "ida-namer:" belong to this plugin.  Please, modify them only in accordance to this documentation, and don't expect any that don't match this documentation to be retained.

On a structure, "ida-namer: foo", where foo is any valid python code, will cause the value of that code (as a string) to be used as the name of the structure.  Elements of the structure may be accessed as s.foo.

On a structure element, "ida-namer: name: foo" will allow naming something pointed to by this structure to be named, similarly to "ida-namer: foo" allowing this instance of a structure itself to be named.

Use on data is currently "ida-namer: autonamed", which will allow ida-namer to change the name of that thing again.  If you want to keep the names of auto-named things, even if the naming convention would make it change, then delete this comment, and ida-namer will leave the data element alone.
