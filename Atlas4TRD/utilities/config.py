def read_config(filepath):
    import json

    with open(filepath) as json_file:
        config = json.load(json_file)

    return config


