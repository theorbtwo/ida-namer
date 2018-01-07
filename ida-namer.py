from ida_struct import *
import idautils
from ida_bytes import *
from ida_name import *
# import ida_struct

def handle_struct_comment(struct_id, comment):
    our_line_re = re.compile(r'^ida-namer:\s*(.*)$', re.IGNORECASE | re.MULTILINE)
    s_obj = get_struc(struct_id)
    s_name = get_struc_name(struct_id)

    for line in our_line_re.findall(comment):
        print "Our comment: {}".format(line)
        code = compile(line, "ida-namer struct comment "+s_name, 'eval')

        for xref in idautils.XrefsTo(struct_id):
            s_ea = xref.frm
            #print "{} at {:#x}".format(s_name, s_ea)
            #print "xref: t#{} t {} {:#x} -> {:#x}".format(xref.type, idautils.XrefTypeName(xref.type), xref.frm, xref.to)

            s = {}
            offset = get_struc_first_offset(s_obj)
            while not is_bad(offset):
                #print "Member offset {:#x}".format(offset)
                m = get_member(s_obj, offset)
                if not m:
                    break

                m_ea = s_ea + offset

                #print " member id: {:#x}".format(m.id)

                mname = get_member_name(m.id)
                #print " member name: {}".format(mname)

                flags = m.flag
                #print " member flags: {:#x}".format(flags)

                size = ida_bytes.get_data_elsize(m_ea, flags)
                #print " size: {}".format(size)

                # FIXME: There is a get_data_value, but I cannot figure out the right way to call it from python!
                value = -1
                if size == 8:
                    value = get_64bit(m_ea)
                elif size == 4:
                    value = get_32bit(m_ea)
                elif size == 2:
                    value = get_16bit(m_ea)
                elif size == 1:
                    value = get_byte(m_ea)

                #print " value: {} = {:#x}".format(value, value)

                s[mname] = value

                if is_off0(flags):
                    #print " is_off0"
                    off_flags = get_flags(value)
                    if is_strlit(off_flags):
                        strlen = get_max_strlit_length(value, 0)
                        if strlen > 0:
                            str = get_bytes(value, strlen-1)
                            s[mname] = str
                
                
                if is_strlit(flags):
                    print " is_strlit"

                offset = get_struc_next_offset(s_obj, offset)

            print "{:#x} s: {}".format(s_ea, s)
            inst_name = eval(code)
            print "Instance Name for {:#x}: {}".format(s_ea, inst_name)
            if inst_name and inst_name != True:
                inst_name = re.sub(r'[ ]', '_', inst_name, 0)
                inst_name = re.sub(r'!', '_excl_', inst_name, 0)
                set_name(xref.frm, inst_name)
            


def is_bad(ea):
    if ea == -1:
        return true
    if ea == 0xFFFFFFFF:
        return True
    if ea == 0xffffffffffffffff:
        return True
    return False

# FIXME: Genericify more?
lookfor_pairs = [[0x14154A230, "SettingT_int"], # const SettingT<class INISettingCollection>::`vftable'
                 [0x14154EC48, "SettingT_int"], # const SettingT<class INIPrefSettingCollection>::`vftable'
                 [0x141539C88, "SettingT_int"], # const SettingT<class GameSettingCollection>::`vftable
                 [0x14172E0D0, "hkDescription"], # aHkDescription
                 [0x14172E0B8, "hkbRoleattribute"], # db 'hkb.RoleAttribute
]

for lookfor_pair in lookfor_pairs:
    lookfor = lookfor_pair[0]
    makeinto = lookfor_pair[1]
    makeinto_tid = get_struc_id(makeinto)
    makeinto_size = ida_struct.get_struc_size(makeinto_tid)

    print "Checking for {:#x} -> {}".format(lookfor, makeinto)
    for xref in idautils.XrefsTo(lookfor):
        s_ea = xref.frm
        if not is_code(get_flags(s_ea)):
            print "Changing {:#x} into struct {:#x} ({})".format(s_ea, makeinto_tid, makeinto)
            ida_bytes.del_items(s_ea, 0, makeinto_size)
            ida_bytes.create_struct(s_ea, makeinto_size, makeinto_tid)
        else:
            print "Skipping {:#x} into struct {:#x} ({}) (is code)".format(s_ea, makeinto_tid, makeinto)
            


this_struct_idx = ida_struct.get_first_struc_idx()
while not is_bad(this_struct_idx):
    #print "this_struct_idx = {}".format(this_struct_idx)

    this_struct_id = get_struc_by_idx(this_struct_idx)
    #print "this_struct_id = {:#x}".format(this_struct_id)

    #this_struct_name = get_struc_name(this_struct_id)
    #print "this_struct_name = {}".format(this_struct_name)

    this_struct_comment = get_struc_cmt(this_struct_id, 0)
    if this_struct_comment:
        #print "this_struct_comment = {}".format(this_struct_comment)
        handle_struct_comment(this_struct_id, this_struct_comment)

    else:
        #print "no comment"
        pass

    this_struct_idx = ida_struct.get_next_struc_idx(this_struct_idx)

