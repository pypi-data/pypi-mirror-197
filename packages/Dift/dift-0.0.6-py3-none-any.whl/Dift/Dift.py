import json

def readData(file_path, ctype=True, separator=":", ignore=True) -> dict:
    """
    Read the data from a file and convert it into a dictionary
    :param file_path: The file path to read data from
    :type file_path: str
    :param ctype: Enable or disable the option to store int as int in dictionary
    :type ctype: bool
    :param separator: The sign to separate the key from the value
    :type separator: string
    :param ignore: Ignore the error due to incorrect separator or no value
    :type ignore: bool
    """


    data = dict()

    if file_path.endswith(('.json', '.Json')):
        with open(file_path, 'r') as f:
            return json.load(f)

 
    with open(file_path, 'r') as f:
        for line in f:
            
            if not line.strip():
                continue

            
            if line.strip().startswith('#'):
                continue

            key, value = map(str.strip, line.strip().split(separator, maxsplit=1))

            
            if ctype:
                try:
                    value = int(value)
                except ValueError:
                    pass

            
            data[key] = value

    return data