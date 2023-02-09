
def convert_into_dict(entity):
    entity.param_dict = {}
    for name in dir(entity):
        value = getattr(entity, name)
        if name in entity.param_list:
            if isinstance(value, str) is False:
                entity.param_dict[name] = str(value)
            else:
                entity.param_dict[name] = value

def convert_dict2obj(entity):
    for name in dir(entity):
        value = getattr(entity, name)
        if name in entity.param_list:
            setattr(entity, name, entity.param_dict[name])