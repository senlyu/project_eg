
def add_into_dict_as_list_item(d, key, item):
    if key in d:
        if isinstance(item, list):
            d[key] = d[key] + item
        else:
            d[key].append(item)
    else:
        if isinstance(item, list):
            d[key] = item
        else:
            d[key] = [ item ]

    return d