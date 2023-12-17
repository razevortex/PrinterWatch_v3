from functools import wraps

from Packages.SubPkg.const.ConstantParameter import data_dict_template


def DataValidation(func):
    @wraps(func)
    def data_validation(data):
        reference = data_dict_template()
        if data is None:
            print('non')
            return data_validation
        elif type(data).__name__ is type(reference).__name__:
            print('typ')
            return data_validation
        elif len(data.items()) < len(reference.items()):
            print('len')
            return data_validation
        for key, val in data.items():
            if key not in list(reference.keys()):
                print('key')
            elif val is None or val == '':
                data[key] = 'NaN'
        data_handle = func(data)
        return data_handle
    return data_validation


@DataValidation
def test(data):
    return data