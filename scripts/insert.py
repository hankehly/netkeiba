import argparse
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def parse_trainer_item(item: dict):
    print(f"[parse_trainer_item] {item['id']}")


def parse_jockey_item(item: dict):
    print(f"[parse_jockey_item] {item['id']}")


def parse_horse_item(item: dict):
    print(f"[parse_horse_item] {item['id']}")


def parse_race_item(item: dict):
    print(f"[parse_race_item] {item['id']}")


def noop(_):
    pass


def parse_item(item: dict):
    handlers = {'race': parse_race_item, 'horse': parse_horse_item, 'jockey': parse_jockey_item,
                'trainer': parse_trainer_item}

    handlers.get(item['item_type'], noop)(item)


def main(opts):
    if not os.path.isfile(opts.input):
        raise FileNotFoundError(f'input file does not exist: {opts.input}')

    with open(opts.input, 'r') as f:
        for obj in f:
            parse_item(json.loads(obj))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='file containing scraped data')
    args = parser.parse_args()
    main(args)
