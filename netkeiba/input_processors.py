import re


def parse_horse_sex(text):
    text = re.split('[戦勝]', text)[:2]

    possible_inputs = {
        '牡': 'male',
        '牝': 'female',
        'セ': 'castrated'
    }

    return possible_inputs.get(text[0])


def parse_horse_age(text):
    text = re.split('[戦勝]', text)[:2]

    return int(text[1])
