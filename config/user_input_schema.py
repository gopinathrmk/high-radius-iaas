import json
import os
import re
import click
from config_schema import GLOBAL_SCHEMA
import cerberus
from general_utils import validate_schema, validate_ip, validate_subnet

CALM_ENVIRONMENT = os.environ['CALM_ENVIRONMENT']

def highlight_text(text, fg=None, **kwargs):
    """Highlight text"""
    return click.style("{}".format(text), fg=fg, bold=True, **kwargs)

def validate_ip_click(value):
    """
    Function to check if the value from click.prompt is a valid ip or not, if not it'll raise an error and ask to re-enter the value.
    Eg: validate_ip("1.1.1.1")
    """
    pattern = re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$")
    if not pattern.match(value, ):
        print('{} must be a valid IP address'.format(value))
        raise click.UsageError(highlight_text('The input value {} is not a valid IP address string in format x.x.x.x - Please enter a valid IP string.'.format(value), "red"))
    return value

def read_ssh_key():
    return os.system('make init-ssh-keys SSH_KEY_TYPE=private')

def validate_subnet_click(value):
    """
    Function to check if "value" is a valid subnet or not, if not it'll raise error("field")
    Eg: validate_subnet("1.1.1.0/24")
    """
    pattern = re.compile\
        (r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?/\d{1,2})')
    if not pattern.match(value, ):
        print('"{}" must be a valid Subnet'.format(value))
        raise click.UsageError(highlight_text('The input value {} is not a valid Subnet address string in format x.x.x.x/x - Please enter a valid Subnet string.'.format(value), "red"))
    return value

def read_user_input(question, data_type=None, value_proc=None, prompt=True, hide_input=False, default=None):
    if data_type == "integer":
        data_type = int
    elif data_type == "string":
        data_type = str
    elif data_type == "float":
        data_type = float
    if default is not None:
        show_default = True
    else:
        show_default = False
    return click.prompt(highlight_text(question), show_default=show_default, type=data_type, hide_input=hide_input, value_proc=value_proc, default=default)

#print(GLOBAL_SCHEMA.keys())

# print(GLOBAL_SCHEMA.items())
# print(GLOBAL_SCHEMA.keys())

# for k, v in GLOBAL_SCHEMA.items():
#     print('Key is {}'.format(k))
#     print('Vales for {} are {}'.format(k, v))
"""
output_data = {}
for k, v in GLOBAL_SCHEMA.items():
    output_data[k] = {}
    print(highlight_text('These questions concern {}'.format(k), "cyan"))
    click.echo(highlight_text('If a default value is present at the end of the question, press "Enter" to select it.  Otherwise, enter a value.', "magenta"))
    for line in v:
        #print('schema line is {}'.format(line))
        datatype = v[line]['type']
        if "default" in v[line]:
            click_default = v[line]['default']
        else:
            click_default = None
        if 'IP'.lower() in line:
            value_proc = validate_ip_click
        else:
            value_proc = None
        user_input = read_user_input(highlight_text("What is the {} to be used with the repo?".format(line), "green"), data_type=datatype, value_proc=value_proc, default=click_default)
        output_data[k][line] = user_input

    validate_schema(v, output_data[k])
"""

def collect_input(schema):
    while True:
        output = {}
        for k,v in schema.items():
            if v['type'] == 'dict':
                print(highlight_text('These questions concern the {} section of the repository schema.'.format(k.upper()), "magenta"))
                output[k] = collect_input(v['schema'])
            elif v.get('type') == 'list' :
                print(highlight_text('\n'+'  '*level+'These questions concern the {} section of the repository schema'.format(k), "magenta"))
                num_of_items = read_user_input(highlight_text('  '*level+"How many {} are in the list ".format(k), "green"), data_type='integer')
                list = []
                level=level+1
                for itr in range(num_of_items):
                    print(highlight_text('\n'+'  '*level+'Please input for  {}.{}'.format(itr+1,k), "magenta"))
                    if (v.get('schema').get('type') == 'dict'):
                        resp = collect_input(v.get('schema').get('schema'),level=level)
                        list.append(resp)
                    else:
                        resp = collect_input({k:v.get('schema')},level=level)
                        list.append(resp.get(k))
                        #print(resp,"..........")
                level=0
                print("\n")
                output[k] = list
                #print(list,"...")
            else:
                if v.get('validator') == validate_ip:
                    value_proc = validate_ip_click
                elif v.get('validator') == validate_subnet:
                    value_proc = validate_subnet_click
                else:
                    value_proc = None
                click_default =  v.get('default')
                metadata = v.get('meta')
                if metadata is not None:
                    description = metadata.get('description', k)
                    hide_input = metadata.get('secret', False)
                else:
                    description = k
                    hide_input = False

                user_input = read_user_input(highlight_text("What is the {} to be used within the repository?".format(description), "green"), data_type=v['type'], value_proc=value_proc, hide_input=hide_input, default=click_default)

                output[k] = user_input

        if validate_schema(schema, output):
            break

    return output

click.echo(highlight_text('\nStarting to configure the repository schema.  Please answer the following questions:', "blue"))
click.echo(highlight_text('NOTE - If a default value is present at the end of the question, press "Enter" to select it.  Otherwise, enter a value.', "blue"))
output_data = {}
for key in GLOBAL_SCHEMA.keys():
    output_data.update(collect_input(GLOBAL_SCHEMA[key]))

with open('../.local/{}/{}-config.json'.format(CALM_ENVIRONMENT, CALM_ENVIRONMENT), 'w') as json_file:
    json.dump(output_data, json_file, indent=4)