# -*- coding: utf-8 -*-

import argparse
import sys
import os
import json


class JsonLambda:
    def __init__(self, root, directory, file):
        self.root = root
        self.dir = directory
        self.file = file

    def __str__(self):
        return f'[root : {self.root}, dir : {self.dir}, file : {self.file}'


def get_lambdas(lambda_path):
    lambda_list = []
    if '.json' in lambda_path:
        if os.path.isfile(lambda_path):
            lambda_list.append(lambda_path)
        else:
            print('file not exist')
            sys.exit()
    else:
        for file in os.listdir(lambda_path):
            if file.endswith('.json'):
                lambda_list.append(JsonLambda(os.path.dirname(lambda_path), os.path.basename(lambda_path), file))
        for r, d, _ in os.walk(lambda_path):
            for folder in d:
                for file in os.listdir(os.path.join(r, folder)):
                    if file.endswith('.json'):
                        lambda_list.append(JsonLambda(r, folder, file))
    return lambda_list


def create_meta(info):
    template = '.. meta::\n'
    template += '\t:keywords:'

    for keyword in info['keywords']:
        template += ' ' + keyword.upper()

    template += '\n\n'
    template += '.. role:: raw-html(raw)\n\t:format: html\n\n'
    return template


def create_desc(info):
    template = ''
    template += info['name'] + '\n'
    template += '=============================\n\n'
    template += info['descriptions']['ko'] + '\n\n'
    return template


def create_slot(controls):
    template = ''

    if controls.get('input'):
        template += '입력 슬롯\n'
        template += '---------\n\n'
        if type(controls['input']) == str:
            template += '* **' + controls['input'].strip() + '**\n\n'
        else:
            for param in controls['input']:
                if type(param) == str:
                    template += '* **' + param.strip() + '**\n\n'
                else:
                    template += '* **' + param['name'].strip() + '**\n\n'

    if controls.get('output'):
        template += '출력 슬롯\n'
        template += '---------\n\n'
        if type(controls['output']) == str:
            template += '* **' + controls['output'].strip() + '**\n\n'
        else:
            for param in controls['output']:
                if type(param) == str:
                    template += '* **' + param.strip() + '**\n\n'
                else:
                    template += '* **' + param['name'].strip() + '**\n\n'
    return template


def create_blank(standard, length):
    blank = ''
    for _ in range(standard - length - 1):
        blank += ' '
    return blank


def create_lines(num, char):
    line = ''
    for _ in range(num):
        line += char
    return line


def create_prop_table(param):
    standard_len = 15

    template = ''
    template += '+-----------------+-------+----------+'
    if len(param) > standard_len:
        template += create_lines(len(param) + 1, '-') + '+\n'
        template += '| Rule            + Type  + Required + Default value'
        template += create_blank(len(param), standard_len - 2) + ' |\n'
        template += '+=================+=======+==========+'
        template += create_lines(len(param) + 1, '=') + '+\n'
    else:
        template += create_lines(standard_len, '-') + '+\n'
        template += '| Rule            + Type  + Required + Default value |\n'
        template += '+=================+=======+==========+'
        template += create_lines(standard_len, '=') + '+\n'
    return template


def create_prop_box(prop):
    standard_len = 15

    template = ''
    template += create_prop_table(str(prop['default_value']))
    template += '|'
    template += ' ' + str(prop['rule']) + create_blank(17, len(str(prop['rule']))) + '+'
    template += ' ' + str(prop['type']) + create_blank(7, len(str(prop['type']))) + '+'
    template += ' ' + str(prop['required']) + create_blank(10, len(str(prop['required']))) + '+'
    template += ' ' + str(prop['default_value']) + create_blank(standard_len, len(str(prop['default_value']))) + '|\n'
    template += '+-----------------+-------+----------+'
    if len(str(prop['default_value'])) > standard_len:
        template += create_lines(len(str(prop['default_value'])) + 1, '-') + '+\n\n'
    else:
        template += create_lines(standard_len, '-') + '+\n\n'

    return template


def create_props(props):
    template = ''
    template += '속성 목록\n'
    template += '---------\n\n'
    for prop in props:
        template += '* **' + prop['title']['ko'].strip() + '**\n\n'
        template += create_prop_box(prop)
        if prop.get('help'):
            template += prop['help']['ko'] + '\n\n'
    return template


def make_sphinx_structure(out_path, json_obj):
    dir_path = os.path.join(out_path, json_obj.dir)
    os.makedirs(dir_path, exist_ok=True)

    template = ''
    template += json_obj.dir + '\n'
    template += create_lines(len(json_obj.dir) + 5, '=') + '\n\n'

    template += '.. toctree::\n'
    template += '    :maxdepth: 1\n'
    template += '    :name: toc-lambda-' + json_obj.dir + '\n\n'

    # for title in json_obj.file:
    #     template += '\t' + title.replace('.app.json', '')

    index_file = open(dir_path + '/index.rst', 'w')
    index_file.write(template)
    index_file.close()


def fill_sphinx_index(lambda_list):
    # make index.rst body
    for lambda_obj in lambda_list:
        file = open(os.path.join(args.opath, lambda_obj.dir, 'index.rst'), 'a')
        file.write('    ' + lambda_obj.file.replace('.app.json', '') + '\n')
        file.close()


def make_sphinx(lambda_list):
    # Make Sphinx Structure
    for lambda_obj in lambda_list:
        make_sphinx_structure(args.opath, lambda_obj)
    fill_sphinx_index(lambda_list)


def create_rst(lambda_list, output_path):
    for lambda_obj in lambda_list:
        lambda_path = output_path
        if type(lambda_obj) == JsonLambda:
            json_path = os.path.join(lambda_obj.root, lambda_obj.dir, lambda_obj.file)
            file_name = lambda_obj.file
            lambda_path = os.path.join(output_path, lambda_obj.dir)
        elif '.json' in lambda_obj:
            json_path = lambda_obj
            file_name = lambda_obj
        else:
            continue
        with open(json_path) as json_file:
            lambda_body = json.load(json_file)
            output = create_meta(lambda_body['info'])
            output += create_desc(lambda_body['info'])
            if lambda_body.get('controls'):
                output += create_slot(lambda_body['controls'])
            if lambda_body.get('props'):
                output += create_props(lambda_body['props'])
            out_file = file_name.replace('.app.json', '.rst')
            f = open(os.path.join(lambda_path, out_file), 'w')
            f.write(output)
            f.close()


# Get Argument
parser = argparse.ArgumentParser()
parser.add_argument('lpath', help='Lambda Directory or Lambda File')
parser.add_argument('opath', help='Output Directory')
args = parser.parse_args()

# json lambda path & files
lambdas = get_lambdas(args.lpath)

# make output dir
os.makedirs(args.opath, exist_ok=True)

if '.json' not in args.lpath:
    make_sphinx(lambdas)

create_rst(lambdas, args.opath)

