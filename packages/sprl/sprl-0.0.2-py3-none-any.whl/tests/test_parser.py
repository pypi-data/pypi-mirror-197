import os
import tempfile
from sprl.parser import parse_sprl_file, make_prompt


def test_parse_sprl_file_valid():
    valid_sprl_content = '''
title = "Example Prompt"

[context]

header = "Choose an animal and its sound."

body = """
Imagine you have a {animal} that makes the sound {animal_noise}.

What would you name your {animal}? Maybe {name}?
"""

footer = "Have fun choosing a name!"

[parameters]

animal = "dog"
animal_noise = "woof"
name = "*"
'''
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        temp.write(valid_sprl_content)
        temp.seek(0)

        result = parse_sprl_file(temp.name)
        os.unlink(temp.name)

        assert result['title'] == 'Example Prompt'
        assert result['context']['header'] == 'Choose an animal and its sound.'
        assert 'Imagine you have a {animal}' in result['context']['body']
        assert result['context']['footer'] == 'Have fun choosing a name!'
        assert result['parameters']['animal'] == 'dog'
        assert result['parameters']['animal_noise'] == 'woof'
        assert result['custom_parameters']['name'] == '*'


def test_parse_sprl_file_invalid():
    invalid_sprl_content = '''
This is an invalid file.
'''
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        temp.write(invalid_sprl_content)
        temp.seek(0)

        result = parse_sprl_file(temp.name)
        os.unlink(temp.name)

        assert result is None


def test_make_prompt():
    parsed_sprl_data = {
        'title': 'Example Prompt',
        'context': {
            'header': 'Choose an animal and its sound.',
            'body': '''
Imagine you have a {animal} that makes the sound {animal_noise}.

What would you name your {animal}? Maybe {name}?
            ''',
            'footer': 'Have fun choosing a name!'
        },
        'parameters': {
            'animal': 'dog',
            'animal_noise': 'woof',
            'name': '*'
        },
        'custom_parameters': {
            'name': '*'
        }
    }

    custom_params = {'name': 'Fluffy'}
    prompt = make_prompt(parsed_sprl_data, custom_params)

    assert 'Choose an animal and its sound.' in prompt
    assert 'Imagine you have a dog' in prompt
    assert 'sound woof' in prompt
    assert 'Maybe Fluffy?' in prompt
    assert 'Have fun choosing a name!' in prompt
