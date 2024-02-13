class data_prep:
    def __init__(self):
        pass

    @staticmethod
    def dict_exclude_keys(dict: dict, *fields_to_exclude):
        clean_dict = dict.copy()
        for field in fields_to_exclude:
            if not isinstance(field, str):
                raise TypeError('All keys must be strings')
            clean_dict.pop(field, None)
        return clean_dict
    
    @staticmethod
    def dict_include_keys(dict: dict, *fields_to_include):
        clean_dict = dict.copy()
        for key in list(dict.keys()):
            if not isinstance(key, str):
                raise TypeError('All keys must be strings')
            if key not in fields_to_include:
                clean_dict.pop(key)
        return clean_dict