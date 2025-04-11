#!/usr/bin/env python3
import argparse
import sys
import os
from  helper.target import *

parser = argparse.ArgumentParser(
    description='Magpie',
    prog='magpie'
)

main_subparsers = parser.add_subparsers(
    dest='command',
    required=True,
    title='Available commands',
    metavar='<command>',
    help='Use "<command> --help" for command-specific help.'
)

parser_target = main_subparsers.add_parser(
    'target',
    help='Manage targets (people, organizations).',
    description='Commands for managing targets databases.'
)

parser_data = main_subparsers.add_parser(
    'data',
    help='Manage data for the targets.',
    description='Commands for managing data in targets.'
)

parser_open_file = main_subparsers.add_parser(
    'open',
    help='Open the file in tartget database',
    description='Open the file in tartget database'
)

target_subparsers = parser_target.add_subparsers(
    dest='action',
    required=True,
    title='Target actions',
    metavar='<action>'
)

data_subparsers = parser_data.add_subparsers(
    dest='action',
    required=True,
    title='data actions',
    metavar='<action>'
)

open_subparsers = parser_open_file.add_subparsers(
    dest='action',
    required=True,
    title='open file or image',
    metavar='<action>'
)

targetHelper = Target()

p_target_add = target_subparsers.add_parser('add', help='Add a new target.')
p_target_add.add_argument('--name',  required=True, help='Target name.')
p_target_add.set_defaults(func=targetHelper.handle_target_add)

p_target_count = target_subparsers.add_parser('count', help='count the total number of targets in the databases.')
p_target_count.set_defaults(func=targetHelper.handle_data_count)

p_target_list = target_subparsers.add_parser('list', help='list all targets.')
p_target_list.set_defaults(func=targetHelper.handle_target_list)

p_target_dump = target_subparsers.add_parser('dump', help='dump all data of a target.')
p_target_dump.add_argument('--target',  required=True, help='Target name.')
p_target_dump.set_defaults(func=targetHelper.handle_target_dump)

p_target_search = target_subparsers.add_parser('search',  help='search for specific entries within the database.')
p_target_search.add_argument('--query',   required=True,  help='the query text.')
p_target_search.add_argument('--target',  required=False, help='Target name, if you want to search only in a specific target.')
p_target_search.add_argument('--dump',    required=False, help='Dump all target contain the query.')
p_target_search.set_defaults(func=targetHelper.handle_target_search)


p_target_delete = target_subparsers.add_parser('remove', help='remove target from database.')
p_target_delete.add_argument('--target',  required=True, help='Target name.')
p_target_delete.set_defaults(func=targetHelper.handle_target_delete)

target_add_data = data_subparsers.add_parser('add', help='add data to the target, valid data types are text, file and image.')
target_add_data.add_argument('--target',   required=True, help='Target name.')
target_add_data.add_argument('--label',  required=True, help='data label.')
target_add_data.add_argument('--type',   required=False, help='data type, text if empty. Valid data types are text, file and image.')
target_add_data.add_argument('--value',  required=True, help='data value, filepath if type is file or image.')
target_add_data.set_defaults(func=targetHelper.handle_data_add)

target_remove_data = data_subparsers.add_parser('remove', help='remove data from the target.')
target_remove_data.add_argument('--target',   required=True, help='Target name.')
target_remove_data.add_argument('--label',  required=True, help='data label.')
target_remove_data.set_defaults(func=targetHelper.handle_data_remove)

target_open = open_subparsers.add_parser('image', help='open image.')
target_open.add_argument('--path',  required=True, help='image path in target database: /targetname/imagelabel')
target_open.set_defaults(func=targetHelper.handle_open_image)

target_open_file = open_subparsers.add_parser('file', help='open file.')
target_open_file.add_argument('--path',  required=True, help='file path in target database: /targetname/filelabel')
target_open_file.set_defaults(func=targetHelper.handle_open_file)



if __name__ == '__main__':
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.command == 'file' and args.action == 'add':
        if not os.path.exists(args.value) or not os.path.isfile(args.value):
            parser.error(f"File not found or is not a file: {args.path}")

    args.func(args)