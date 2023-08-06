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