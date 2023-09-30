
def load_config(file_path: str, values: [str]):

    config = {}

    with open(file_path, 'r') as file:

        for val in values:
            file.seek(0)

            section_name = val
            print('test')

            for line in file:

                line = line.strip()
                line_name = line.split('=')[0]

                if line_name == val:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()

    return config
