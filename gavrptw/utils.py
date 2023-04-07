
'''gavrptw/uitls.py'''

import os
import io
import fnmatch
from json import load, dump
from . import BASE_DIR


def make_dirs_for_file(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass


def guess_path_type(path):
    if os.path.isfile(path):
        return 'Файл'
    if os.path.isdir(path):
        return 'Директория'
    if os.path.islink(path):
        return 'Ссылка'
    if os.path.ismount(path):
        return 'Точка отсчёта'
    return 'Путь'


def exist(path, overwrite=False, display_info=True):
    if os.path.exists(path):
        if overwrite:
            if display_info:
                print(f'{guess_path_type(path)}: {path} существует. Перезаписано.')
            os.remove(path)
            return False
        if display_info:
            print(f'{guess_path_type(path)}: {path} существует.')
        return True
    if display_info:
        print(f'{guess_path_type(path)}: {path} не существует.')
    return False


def load_instance(json_file):
    if exist(path=json_file, overwrite=False, display_info=True):
        with io.open(json_file, 'rt', encoding='utf-8', newline='') as file_object:
            return load(file_object)
    return None


def merge_rules(rules):
    is_fully_merged = True
    for round1 in rules:
        if round1[0] == round1[1]:
            rules.remove(round1)
            is_fully_merged = False
        else:
            for round2 in rules:
                if round2[0] == round1[1]:
                    rules.append((round1[0], round2[1]))
                    rules.remove(round1)
                    rules.remove(round2)
                    is_fully_merged = False
    return rules, is_fully_merged


def calculate_distance(customer1, customer2):
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + \
        (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5


def text2json(customize=False):
    text_data_dir = os.path.join(BASE_DIR, 'data', 'text_customize' if customize else 'text')
    json_data_dir = os.path.join(BASE_DIR, 'data', 'json_customize' if customize else 'json')
    for text_file in map(lambda text_filename: os.path.join(text_data_dir, text_filename), \
        fnmatch.filter(os.listdir(text_data_dir), '*.txt')):
        json_data = {}
        with io.open(text_file, 'rt', encoding='utf-8', newline='') as file_object:
            for line_count, line in enumerate(file_object, start=1):
                if line_count in [2, 3, 4, 6, 7, 8, 9]:
                    pass
                elif line_count == 1:
                    # <Instance name>
                    json_data['instance_name'] = line.strip()
                elif line_count == 5:
                    # <Maximum vehicle number>, <Vehicle capacity>
                    values = line.strip().split()
                    json_data['max_vehicle_number'] = int(values[0])
                    json_data['vehicle_capacity'] = float(values[1])
                elif line_count == 10:
                    # Custom number = 0, depart
                    # <Custom number>, <X coordinate>, <Y coordinate>,
                    # ... <Demand>, <Ready time>, <Due date>, <Service time>
                    values = line.strip().split()
                    json_data['depart'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }
                else:
                    # <Custom number>, <X coordinate>, <Y coordinate>,
                    # ... <Demand>, <Ready time>, <Due date>, <Service time>
                    values = line.strip().split()
                    json_data[f'customer_{values[0]}'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }
        customers = ['depart'] + [f'customer_{x}' for x in range(1, 39)]
        json_data['distance_matrix'] = [[calculate_distance(json_data[customer1], \
            json_data[customer2]) for customer1 in customers] for customer2 in customers]
        json_file_name = f"{json_data['instance_name']}.json"
        json_file = os.path.join(json_data_dir, json_file_name)
        print(f'Write to file: {json_file}')
        make_dirs_for_file(path=json_file)
        with io.open(json_file, 'wt', encoding='utf-8', newline='') as file_object:
            dump(json_data, file_object, sort_keys=True, indent=4, separators=(',', ': '))
