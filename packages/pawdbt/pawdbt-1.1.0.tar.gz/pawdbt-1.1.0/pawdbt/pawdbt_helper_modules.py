# automated version with user prompt
import argparse
import yaml
import subprocess
import os
from tqdm import tqdm
from prettytable import PrettyTable
from halo import Halo
import sys
import inspect

# Define global attributes

VERSION = '1.1.0'
AUTHOR = 'Dan Wilson'
NAME = 'pawdbt'

DRY_FILE_NAME = 'dry'
DRY_FILE_EXT = 'md'
DRY_FILE_IN_DIR = '_docs'
DRY_DOC_BLOCK_PREFIX = DRY_FILE_NAME + '_'
DOC_BLOCK_START_PATTERN = '{% docs'
DOC_BLOCK_END_PATTERN = '%}'

DBT_DEBUG_CMD = ['dbt', 'debug']

# Create list of flags available during module call

flag_list = [('-s', '--select', str), ('-d', '--save-doc-blocks-in', str), ('-o', '--always-overwrite', bool),
             ('-r', '--run-models', bool)]

# Custom loading icon for use by Halo

loader = {
		"interval": 60,
		"frames": [
			"▰ ▱ ▱ ▱ ▱ ▱ ▱ ",
			"▰ ▰ ▱ ▱ ▱ ▱ ▱ ",
			"▰ ▰ ▰ ▱ ▱ ▱ ▱ ",
			"▰ ▰ ▰ ▰ ▱ ▱ ▱ ",
			"▰ ▰ ▰ ▰ ▰ ▱ ▱ ",
			"▰ ▰ ▰ ▰ ▰ ▰ ▱ ",
			"▰ ▰ ▰ ▰ ▰ ▰ ▰ ",
            "▱ ▰ ▰ ▰ ▰ ▰ ▰ ",
            "▱ ▱ ▰ ▰ ▰ ▰ ▰ ",
            "▱ ▱ ▱ ▰ ▰ ▰ ▰ ",
            "▱ ▱ ▱ ▱ ▰ ▰ ▰ ",
            "▱ ▱ ▱ ▱ ▱ ▰ ▰ ",
            "▱ ▱ ▱ ▱ ▱ ▱ ▰ ",
            "▱ ▱ ▱ ▱ ▱ ▱ ▱ ",
            "▱ ▱ ▱ ▱ ▱ ▱ ▱ ",
            "▱ ▱ ▱ ▱ ▱ ▱ ▱ "
		]
}

def raise_error(msg):
    """
    Get name of caller function for debugging & raise a stderr with custom message
    """

    frame = inspect.currentframe().f_back  # get the frame of the calling function
    function_name = frame.f_code.co_name  # get the name of the calling function
    print('\033[31m' + f"\nError raised within subroutine `{function_name}`: {msg}" + '\033[0m', file=sys.stderr)  # raise as stderr
    sys.exit(1)

def clear_terminal():
    """
    Clear terminal before running script, OS agnostic
    """

    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_dir():
    """
    Returns absolute path of current users current working directory
    """

    try:
        directory = os.getcwd()
        return directory
    except OSError as error_str:
        raise_error(error_str)
        return None

def get_file_path(path, name, type, required_folder_name=None):
    """
    Takes a path as a parameter, and then looks within this path to find a file of name.type.
    An optional argument required_folder_name can be provided to ensure that one of the directories in the files path is equal to it.
    This can be useful when there may be multiple files of the same name, but only one path you would like to search.
    """

    try:
        for root, dirs, files in os.walk(path):
            if required_folder_name is None or required_folder_name in root.split(os.path.sep):
                for file in files:
                    file_name, file_type = file.split('.')
                    if file_name == name and file_type == type:
                        return os.path.join(root, file)
    except(ValueError, OSError) as error_str:
        raise_error(error_str)

    return None

def get_file_contents_by_line(path):
    """
    Reads the contents of a file and returns the contents as a list of lines.

    Args:
        path (str): The path to the file to read.

    Returns:
        list: A list of lines from the file, or None if an error occurred.

    Raises:
        OSError: If there was an error opening or reading the file.
    """

    try:
        with open(path, encoding='utf-8') as file:
            return file.readlines()
    except OSError as error_str:
        raise_error(error_str)

    return None

def find_text_between_delimiters(line, start_delim, end_delim):
    """
    Finds the text between two delimiters in a given string.

    Args:
        line (str): The string to search for the delimiters and the text.
        start_delim (str): The starting delimiter to search for in the line.
        end_delim (str): The ending delimiter to search for in the line.

    Returns:
        str: The text found between the start and end delimiters, or None if either delimiter is not found.

    Raises:
        ValueError: If the start or end delimiter is not found in the line.
        ValueError: If both start and end delimiters are contained within the found text.
    """

    start_index = line.find(start_delim)
    end_index = line.find(end_delim)

    if start_index == -1 or end_index == -1:
        return None

    found_text = line[start_index + len(start_delim):end_index].strip()

    if start_delim in found_text and end_delim in found_text:
        raise_error(f'Start and end delimiters cannot be contained in line: {line}')

    return found_text

def get_all_dry_doc_blocks(cd):
    """
    Finds all the 'dry' blocks in a DRY markdown file.

    A 'dry' block is a block of documentation that can be reused in
    multiple places.

    Args:
        cd (str): The path to the directory to search for the DRY markdown file.

    Returns:
        list: A list of 'dry' block names found in the DRY markdown file.
    """

    # Get the path to the DRY markdown file.
    dry_md_path = get_file_path(cd, DRY_FILE_NAME, DRY_FILE_EXT, DRY_FILE_IN_DIR)

    # Read the contents of the DRY markdown file into a list of lines.
    dry_file_lines = get_file_contents_by_line(dry_md_path)

    # Find all 'dry' blocks in the DRY markdown file.
    dry_blocks = []

    for line in dry_file_lines:
        stripped_of_jinja = find_text_between_delimiters(line, DOC_BLOCK_START_PATTERN, DOC_BLOCK_END_PATTERN)
        if stripped_of_jinja and stripped_of_jinja.startswith(DRY_DOC_BLOCK_PREFIX):
            dry_blocks.append(stripped_of_jinja)

    return dry_blocks

def run_command_get_output(command):
    """
    Runs a shell command and returns its output.

    Args:
        command (str): the command to run

    Returns:
        str: the output of the command
    """
    try:
        # Run the command and capture its output and errors
        completed_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                           check=True)
        # If the command ran successfully, return its output as a string
        return completed_process.stdout
    except (subprocess.CalledProcessError, OSError) as error_msg:
        # If the command failed, raise an exception with the error message
        raise_error(error_msg)

def is_dbt_project_healthy():
    """
    Checks if the current directory contains a healthy dbt project.

    Returns:
        bool: True if the project is healthy, False otherwise.
    """

    output = run_command_get_output(DBT_DEBUG_CMD)
    if output:
        if 'All checks passed!' in output:
            return True
        elif 'Could not load dbt_project.yml' in output:
            raise_error('Current working directory is not a dbt project')
        elif 'Encountered an error' in output:
            raise_error('Profiles.yml entry for this project not found')
        else:
            raise_error('Unknown error occurred')
    else:
        raise_error('Unknown error occurred')
    return False

def return_flag_values(flag_list):
    """
    Parse command-line arguments based on the given flag list and return a dictionary of parsed values.

    Args:
        flag_list (list): A list of tuples representing the command-line flags to be parsed. Each tuple should have
        three elements: the short flag (single character), the long flag (string), and the data type of the argument.

    Returns:
        dict: A dictionary with the long flag names as keys and the parsed values as values. Flags that were not
        present on the command line are excluded from the dictionary.

    Raises:
        RuntimeError: If an error occurs during argument parsing.
    """

    try:
        parser = argparse.ArgumentParser()
        for short_flag, long_flag, data_type in flag_list:
            if data_type == bool:
                parser.add_argument(short_flag, long_flag, dest=long_flag.lstrip('-'), action='store_true')
            else:
                parser.add_argument(short_flag, long_flag, dest=long_flag.lstrip('-'), type=data_type, nargs='+')
        args = parser.parse_args()

        return {long_flag.lstrip('-'): value for long_flag, value in vars(args).items() if value is not None}
    except Exception as error_str:
        raise_error(error_str)

def get_models_by_identifier_type(type, selector):
    """
    Function that retrieves the names of dbt models that match a specific identifier type and selector.

    Input:

    - type: a string representing the type of output.
    - selector: a string representing the selector used to identify models.

    Output:

    - A list of strings representing the names of the models that match the selector.

    Behavior:

    - The function builds a command to execute a dbt command with the provided selector and output type.
    - The command is executed using the run_command_get_output() function.
    - The output is split into separate lines.
    - If the output is empty, the function raises an error stating that the provided selector does not match any nodes.
    """

    cmd = ['dbt', '--quiet', 'ls', '--resource-type', f"model", '--output', f"{type}", '--select', f"{selector}"]
    lines = run_command_get_output(cmd).splitlines()

    if not lines:
        raise_error('Selector provided does not match any nodes')

    return lines

def get_domain_name(path):
    """
    Function that extracts the domain name from a file path.

    Input:

    - path: a string representing the file path from which to extract the domain name.

    Output:

    - A string representing the domain name.

    Behavior:

    - The function splits the file path by the OS path separator to obtain the second directory in the path.
    - The second directory is returned as the domain name.
    - If an IndexError or TypeError occurs during the operation, the function prints an error message and returns None.
    """

    try:
        second_dir = path.split(os.sep)[1]
        return second_dir
    except (IndexError, TypeError) as error_str:
        raise_error(error_str)
        return None

def get_relation_columns_and_datatype(relation):
    """
    Returns a tuple containing two lists - column names and their data types - for a given relation.

    Args:
        relation (str): The name of the relation for which to get column names and data types.

    Returns:
        tuple: A tuple containing two lists - column names and their data types - extracted from the output of the
            `get_relation_columns_and_datatype` dbt operation.
    """

    cmd = ['dbt', 'run-operation', 'get_relation_columns_and_datatype', '--args', f'relation: "{relation}"']
    lines = run_command_get_output(cmd).splitlines()

    cols = []
    types = []

    for line in lines:
        clean_line = find_text_between_delimiters(line, '{', '}')
        if clean_line:
            column_name, data_type = clean_line.split(':')
            cols.append(column_name)
            types.append(data_type)

    return cols, types

class MyDumper(yaml.Dumper):
    """
    A custom YAML dumper that overrides the increase_indent and write_line_break methods of the parent class.

    Methods:
    --------
    increase_indent(flow=False, indentless=False):
        Increase the current indentation level of the YAML document.

    write_line_break(data=None):
        Write a line break to the YAML document and add an extra one after the first level of indentation.
    """

    def increase_indent(self, flow=False, indentless=False):
        """
        Override the parent method to always set 'indentless' to False.

        Parameters:
        -----------
        flow : bool, optional
            Whether to use the flow style of YAML or not. Default is False.

        indentless : bool, optional
            Whether the current node should not have indentation. Default is False.
        """
        return super(MyDumper, self).increase_indent(flow, False)

    def write_line_break(self, data=None):
        """
        Override the parent method to add an extra line break after the first level of indentation.

        Parameters:
        -----------
        data : any, optional
            The data to write to the YAML document. Default is None.
        """
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

def create_relation_yml(relation, relation_path, columns, dry_columns, data_types):
    """
    This function creates a YAML string that represents a dbt model for a given database table. It takes in the relation name,
    path to the relation, list of column names, list of dry columns, and list of data types for each column.

    The function loops through each column and creates a dictionary with the column name, description that includes the doc block for the
    column, and a test to check the data type of the column. It then appends this dictionary to a list.

    The function then creates another dictionary with the relation name, description that includes the doc block for the relation, and
    a test to check the number of columns in the relation. This dictionary contains a list of the column dictionaries created earlier.

    Finally, the function dumps this dictionary into a YAML string using MyDumper class that has customized indent and line break functions.

    The function returns the YAML string representing the dbt model for the relation.
    """

    col_list = []
    for i in range(len(columns)):

        col_doc_block = get_domain_name(relation_path) + '_' + columns[i]

        for dry_col in dry_columns:
            if 'dry_' + columns[i] == dry_col:
                col_doc_block = dry_col

        col_dict = {
            'name': columns[i],
            'description': f'{{{{ doc("{col_doc_block}") }}}}',
            'tests': [
                {
                    'dbt_expectations.expect_column_values_to_be_of_type': {
                        'column_type': data_types[i]
                    }
                }
            ]
        }
        col_list.append(col_dict)

    data = {
        'version': 2,
        'models': [
            {
                'name': relation,
                'description': f'{{{{ doc("{relation}") }}}}',
                'tests': [
                    {
                        'dbt_expectations.expect_table_column_count_to_equal': {
                            'value': len(columns)
                        }
                    }
                ],
                'columns': col_list
            }
        ]
    }

    yaml_str = yaml.dump(data, Dumper=MyDumper, sort_keys=False)

    return yaml_str

def generate_column_md(column_name):
    """
    Function: generate_column_md(column_name)

    Description:
    This function takes a column name as input and generates markdown for that column. The markdown contains a tag for
    the column name which can be used to link to documentation related to that column.

    Arguments:
    - column_name: a string representing the name of the column for which markdown needs to be generated.

    Returns:
    - A string containing markdown for the specified column. The markdown contains a tag for the column name.
    """

    lines = ['{{% docs {} %}}'.format(column_name),
             '{% enddocs %}']

    return '\n\n'.join(lines)

def create_relation_md(relation_name, relation_path, selected_models, selected_paths, dry_arr, doc_blocks_in_relation):
    """
    Function: create_relation_md(relation_name, relation_path, selected_models, selected_paths, dry_arr, doc_blocks_in_relation)

    Description:
    This function generates markdown for a specified relation by concatenating a header and a list of documentation
    blocks for columns in the relation. The function can also fetch documentation blocks from other models in the same
    domain as the relation.

    Arguments:
    - relation_name: a string representing the name of the relation for which markdown needs to be generated.
    - relation_path: a string representing the path to the relation.
    - selected_models: a list of strings representing the names of the models in the relation.
    - selected_paths: a list of strings representing the paths of the models in the relation.
    - dry_arr: a list of strings representing columns to be excluded from documentation.
    - doc_blocks_in_relation: a string representing the name of a model in the same domain from which documentation
    blocks should be fetched.

    Returns:
    - A string containing markdown for the specified relation.
    """

    full_md = ''
    header_lines = [
        '{{% docs {} %}}'.format(relation_name),
        '## Overview',
        '### Unique Key:',
        '### Partitioned by:',
        '### Contains PII:',
        '### Granularity:',
        '### Update Frequency:',
        '### Example Queries:',
        '{% enddocs %}'
    ]

    full_md += '\n\n'.join(header_lines)

    doc_columns = []
    doc_blocks = []

    if doc_blocks_in_relation:
        if relation_name == doc_blocks_in_relation:
            relation_domain = get_domain_name(relation_path)

            with tqdm(total=len(selected_models), colour='green') as pbar:

                for i in range(len(selected_models)):
                    if relation_domain == get_domain_name(selected_paths[i]):
                        pbar.set_description(f'Fetching Shared Column Doc Blocks ({selected_models[i]})')
                        columns, types = get_relation_columns_and_datatype(selected_models[i])
                        for column in columns:
                            add_doc = True
                            for dry_column in dry_arr:
                                if 'dry_' + column == dry_column:
                                    add_doc = False
                            if add_doc:
                                if column not in doc_columns:
                                    doc_columns.append(column)

                    pbar.update()

            for column in doc_columns:
                doc_blocks.append(generate_column_md(relation_domain + '_' + column))

            full_md += '\n\n' + '\n\n'.join(doc_blocks)

    return full_md

def header_and_info(selector, doc_blocks_in_relation, always_overwrite, run_models):
    """
    Function: header_and_info(selector, doc_blocks_in_relation, always_overwrite, run_models)

    Description:
    This function generates and prints a pretty table with information on the current package, its version, the selector
    used, whether documentation blocks will be saved, whether force overwrite is enabled, and whether models will be run.

    Arguments:
    - selector: a string representing the selector used to filter models.
    - doc_blocks_in_relation: a string representing the name of the model in the same domain from which documentation
      blocks should be fetched.
    - always_overwrite: a boolean indicating whether to overwrite existing documentation blocks.
    - run_models: a boolean indicating whether to run the models to fetch documentation blocks.
    """

    table = PrettyTable()
    table.field_names = ['Package', 'Maintained By', 'Version', 'Selector', 'Doc Blocks Saved To', 'Force Overwrite?',
                         'Run Models?']
    table.add_row([NAME, AUTHOR, VERSION, selector, doc_blocks_in_relation, str(always_overwrite), str(run_models)])
    print(table)

def create_file(relation_path, extension, str, always_overwrite):
    """
    Function: create_file(relation_path, extension, str, always_overwrite)

    Description:
    This function creates a file with a given extension and writes a given string to it. If the file already exists
    and always_overwrite is False, the function asks the user whether to overwrite, append to, or ignore the file.

    Arguments:
    - relation_path: a string representing the path to the original file.
    - extension: a string representing the extension of the new file to be created.
    - str: a string to be written to the new file.
    - always_overwrite: a boolean indicating whether to always overwrite existing files.
    """
    try:
        dir_path, file_name = os.path.split(relation_path)
        file_name_no_ext = os.path.splitext(file_name)[0]
        new_file_name = file_name_no_ext + "." + extension
        file_path = os.path.join(dir_path, new_file_name)
        mode = 'w'
        while os.path.exists(file_path) and not always_overwrite:
            print(f"\n\nThe file {file_path} already exists. Do you want to:")
            print("1. Overwrite the file")
            print("2. Append to the file")
            print("3. Ignore the file")
            action = input("Choice (1,2,3): ")
            if action.lower() == "1":
                mode = "w"
                break
            elif action.lower() == "2":
                mode = "a"
                break
            elif action.lower() == "3":
                return
            else:
                print("Invalid choice. Please choose 1, 2, or 3.")
        with open(file_path, mode) as f:
            f.write(str)
    except Exception as error_str:
        raise_error(error_str)

def run_selector(selector):
    """
    This function runs a dbt run command with a specified selector. It takes a single argument selector, which is
    a string specifying the selector to use when running dbt.

    Inside the function, a command list cmd is created with dbt, run, and --select as its elements. Then,
    run_command_get_output function is called with cmd as an argument. If the function is executed successfully,
    the function returns True. Otherwise, it raises an error with the error message passed to the function.
    """

    cmd = ['dbt', 'run', '--select', selector]
    try:
        run_command_get_output(cmd)
        return True
    except Exception as error_str:
        raise_error(error_str)
