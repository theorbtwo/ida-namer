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

... and a bit of what it did from that:

    .data:00000000618DF4A8 idcfunc_t_set_enum_idx ext_idcfunc_t <offset aSetEnumIdx_0, offset idcfunc_set_enum_idx, \ ; "set_enum_idx"
    .data:00000000618DF4A8                                offset dword_615562B4, 0, 0, EXTFUN_BASE>; 0
    .data:00000000618DF4D0 idcfunc_t_set_enum_name ext_idcfunc_t <offset aSetEnumName_0, offset idcfunc_set_enum_name, \ ; "set_enum_name"
    .data:00000000618DF4D0                                offset qword_61556310, 0, 0, EXTFUN_BASE>; 0
    .data:00000000618DF4F8 idcfunc_t_set_enum_cmt ext_idcfunc_t <offset aSetEnumCmt_0, offset idcfunc_set_enum_cmt, \ ; "set_enum_cmt"
    .data:00000000618DF4F8                                offset qword_61556370, 0, 0, EXTFUN_BASE>; 0
    .data:00000000618DF520 idcfunc_t_set_enum_flag ext_idcfunc_t <offset aSetEnumFlag_0, offset idcfunc_set_enum_flag, \ ; "set_enum_flag"
    .data:00000000618DF520                                offset qword_615563E0, 0, 0, EXTFUN_BASE>; 0

    .text:000000006131B380 ; [00000025 BYTES: COLLAPSED FUNCTION idcfunc_set_enum_idx. PRESS CTRL-NUMPAD+ TO EXPAND]
    .text:000000006131B3A5 algn_6131B3A5:                          ; DATA XREF: .text:00000000618C1190↓o
    .text:000000006131B3A5                 align 10h
    .text:000000006131B3B0 ; [00000096 BYTES: COLLAPSED FUNCTION idcfunc_get_event_exc_info. PRESS CTRL-NUMPAD+ TO EXPAND]
    .text:000000006131B446 algn_6131B446:                          ; DATA XREF: .text:00000000618C119C↓o
    .text:000000006131B446                 align 10h
    .text:000000006131B450 ; [00000025 BYTES: COLLAPSED FUNCTION idcfunc_add_func. PRESS CTRL-NUMPAD+ TO EXPAND]
    .text:000000006131B475 algn_6131B475:                          ; DATA XREF: .text:00000000618C11A8↓o
    .text:000000006131B475                 align 20h
    .text:000000006131B480 ; [0000005F BYTES: COLLAPSED FUNCTION idcfunc_trim. PRESS CTRL-NUMPAD+ TO EXPAND]
    .text:000000006131B4DF algn_6131B4DF:                          ; DATA XREF: .text:00000000618C11B4↓o
    .text:000000006131B4DF                 align 20h
    .text:000000006131B4E0 ; [00000033 BYTES: COLLAPSED FUNCTION idcfunc_set_enum_name. PRESS CTRL-NUMPAD+ TO EXPAND]
    .text:000000006131B513 algn_6131B513:                          ; DATA XREF: .text:00000000618C11C0↓o
    .text:000000006131B513                 align 20h


TODO: On a structure element, "ida-namer: name: foo" will allow naming something pointed to by this structure to be named, similarly to "ida-namer: foo" allowing this instance of a structure itself to be named.

TODO: Use on data is currently "ida-namer: autonamed", which will allow ida-namer to change the name of that thing again.  If you want to keep the names of auto-named things, even if the naming convention would make it change, then delete this comment, and ida-namer will leave the data element alone.
