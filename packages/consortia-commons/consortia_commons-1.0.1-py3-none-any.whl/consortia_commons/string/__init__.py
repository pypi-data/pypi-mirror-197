def trim_dict_or_list(item):
    if type(item) is list:
        for i, v in enumerate(item):
            if type(v) is str:
                item[i] = v.strip()
            else:
                trim_dict_or_list(v)
    elif type(item) is dict:
        for k, v in item.items():
            if type(v) is str:
                item[k] = v.strip()
            else:
                trim_dict_or_list(v)

    return item


def is_blank(val):
    if val is None:
        return True
    if val.strip() == "":
        return True
    return False


def is_yes(val):
    if is_blank(val): return False
    c_val = val.upper().strip()
    return (c_val == "Y" or c_val == "YES" or c_val == "TRUE")


def get_yes_no(msg):
    ans = None
    while ans not in ("y", "n"):
        ans = input(msg)
        ans = ans.lower().strip()
        if ans == "y":
            return True
        elif ans == "n":
            return False


def pad_leading_zeros(int_val, n_chars_with_padding):
    for n in range(1, n_chars_with_padding):
        chk_val = int_val / 10 ** n
        if chk_val < 1:
            return str(str('0') * (n_chars_with_padding - n)) + str(int_val)
    return str(int_val)


def list_to_delimited(lst, delimit_char=", ", quote_char=None, trim_and_upper_case=False):
    delimiter = ""
    r_val = ""
    first = True
    if quote_char is None:
        quote_char = ""
    for val in lst:
        if isinstance(val, tuple):
            p_val = val[0]
        else:
            p_val = val
        if trim_and_upper_case:
            p_val = p_val.strip().upper()
        r_val = r_val + delimiter + quote_char + p_val + quote_char
        if first:
            first = False
            delimiter = delimit_char

    return r_val


def list_to_tab_separated(lst, quote_char=None, trim_and_upper_case=False):
    return list_to_delimited(lst, '\t', quote_char, trim_and_upper_case)


def list_to_comma_separated(lst, quote_char=None, trim_and_upper_case=False):
    return list_to_delimited(lst, ", ", quote_char, trim_and_upper_case)


def all_indexes(value, character):
    return [i for i, ltr in enumerate(value) if ltr == character]
