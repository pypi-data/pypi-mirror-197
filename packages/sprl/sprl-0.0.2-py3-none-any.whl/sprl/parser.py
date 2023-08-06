import toml


def parse_sprl_file(file_path):
    try:
        with open(file_path, 'r') as file:
            sprl_data = toml.load(file)

            title = sprl_data.get('title')
            context = sprl_data.get('context', {})
            parameters = sprl_data.get('parameters', {})
            custom_parameters = {key: value for key,
                                 value in parameters.items() if value == '*'}

            return {
                'title': title,
                'context': context,
                'parameters': parameters,
                'custom_parameters': custom_parameters,
            }

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error while parsing the file: {e}")

    return None


def make_prompt(parsed_sprl_data, custom_params):
    parameters = parsed_sprl_data['parameters']
    parameters.update(custom_params)

    header = parsed_sprl_data['context'].get('header', '')
    body = parsed_sprl_data['context'].get('body', '').format(**parameters)
    footer = parsed_sprl_data['context'].get('footer', '')

    return f"{header}\n\n{body}\n\n{footer}".strip()
