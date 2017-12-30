# ida-namer
Automatically rename structures, and hopefully more later.

This plugin reserves for itself a small namespace in non-repeatable comments on structures, structure elements, and data.  All such comments that contain a line beginning "ida-namer:" belong to this plugin.  Please, modify them only in accordance to this documentation, and don't expect any that don't match this documentation to be retained.

On a structure, "ida-namer: foo", where foo is any valid python code, will cause the value of that code (as a string) to be used as the name of the structure.  Elements of the structure may be accessed as s["foo"].  (Currently, if ida knows that a member is an offset, and there is a string literal at that offset, it will get the value of the string.  Everything else will be interpreted as an integer of the relevant size.)  For convience of slightly strange hacks, attempts to rename things to false values or ```True``` will be ignored.

An example, for (hopefully) a bit more clarity:

    00000000 ; ida-namer: "idcfunc_t_"+s["name"]
    00000000 ; ida-namer: set_name(s["fptr"], "idcfunc_"+s["name"])
    00000000 ext_idcfunc_t   struc ; (sizeof=0x28, mappedto_78)
    00000000                                         ; XREF:  .text:idcfunc_t_SetOstype/r
    00000000                                         ; .text:idcfunc_t_SetApptype/r ...
    00000000 name            dq ?                    ; offset
    00000008 fptr            dq ?                    ; offset
    00000028 ext_idcfunc_t   ends

This shows a couple of non-obvious features:

1. You can have more than one ida-namer: line on the same thing.  They will execute in the order given.  (More explicitly: the first line will run first, for all instances of the struct.  After that, the second line will run for each instance.)

1. You can use arbitrary expressions to do things like add a prefix or suffix.

1. You can call ```set_name(ea, string)``` explicitly to give a name to (the thing pointed to by) an element of the struct.  This works without having to explicitly make a null-operation because set_name() returns ```True``` on success.

Eventually: On a structure element, "ida-namer: name: foo" will allow naming something pointed to by this structure to be named, similarly to "ida-namer: foo" allowing this instance of a structure itself to be named.

Eventually: Use on data is currently "ida-namer: autonamed", which will allow ida-namer to change the name of that thing again.  If you want to keep the names of auto-named things, even if the naming convention would make it change, then delete this comment, and ida-namer will leave the data element alone.

