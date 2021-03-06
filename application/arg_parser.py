from argparse import ArgumentParser
from application import database_operations, config_writer
from application.my_namespace import MyNamespace

'''
Setup Command Line interface.
'''

parser = ArgumentParser(add_help=True)
sub_parser = parser.add_subparsers(dest='command', required=True)

### Global Flags:
#     # These aren't global...........
# parser.add_argument('-q', '--quiet', 
#                     action='store_true',        # The value that is stored. # Store_true --> Flag (No value expected.)
#                     dest='quiet')               # The Namespace attribute that the above value is stored in

### Commands
refresh_database = sub_parser.add_parser('refresh-database', help='Refresh the database')
refresh_database.add_argument('-s', '--sample', action='store_true', help='Generate sample data', dest='sample')

delete_database = sub_parser.add_parser('delete-database', help='Delete the database')
delete_database.add_argument('-f', '--force', action='store_true', help='Force delete (without warning)')

update_config = sub_parser.add_parser('update-config', help='Edit global configurations')
update_config.add_argument('--setting', help='The Config Setting to update', dest='setting', nargs='?')
update_config.add_argument('--value', help='The new value for the specified setting', dest='value', nargs='?')

update_config = sub_parser.add_parser('describe', help='prints')

# Main script
user_input = parser.parse_args(namespace=MyNamespace())
command = user_input.command
args = user_input.getAuxilliaryInputDict()

directory = {
    'refresh-database': database_operations.refreshDatabase,
    'delete-database': database_operations.deleteDatabase,
    'update-config': config_writer.updateConfig,
    'describe': database_operations.describe
}

print(directory[command](args))
# print(command)
# print(user_input.getAuxilliaryInputDict())
# print(user_input)
