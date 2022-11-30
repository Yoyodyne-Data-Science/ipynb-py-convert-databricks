import json
import sys
from os import path
from typing import Dict, List, NoReturn

# Set variables per file extension
py_comment = '#'
sql_comment = '--'

py_extension = '.py'
sql_extension = '.sql'
nb_extension = '.ipynb'

command_block = ' COMMAND ----------'
py_command_comment = py_comment + command_block
sql_command_comment = sql_comment + command_block

markdown_cell = "%md"
markdown_sandbox_cell = "%md-sandbox"
magic = " MAGIC "
py_markdown_comment = py_comment + magic + markdown_cell
sql_markdown_comment = sql_comment + magic + markdown_cell
py_markdown_sandbox_comment = py_comment + magic + markdown_sandbox_cell
sql_markdown_sandbox_comment = sql_comment + magic + markdown_sandbox_cell
py_magic_code = py_comment + magic
sql_magic_code = sql_comment + magic

databricks_nb_start_block = " Databricks notebook source\n"
py_databricks_nb_start = py_comment + databricks_nb_start_block
sql_databricks_nb_start = sql_comment + databricks_nb_start_block

def nb2py(notebook):
    """ Function for converting from notebook to py file
    """
    result = []
    cells = notebook['cells']
    
    for idx, cell in enumerate(cells):
        cell_type = cell['cell_type']

        if cell_type == 'markdown':
            cell_content = py_markdown_comment + "\n" + py_magic_code + \
                            ''.join(cell['source']).replace("\n", "\n" + py_magic_code)
            if idx == 0:
                cell_content = py_databricks_nb_start + cell_content 
            else:
                cell_content = cell_content
            result.append(cell_content)
    
        if cell_type == 'code':
            cell_content = ''.join(cell['source'])
            if idx == 0:
                cell_content = py_databricks_nb_start + cell_content
            else:
                cell_content = cell_content
            result.append(cell_content)
        
    return ("\n\n" + py_command_comment + "\n\n").join(result)

def _get_notebook(cells:List[str], format:str) -> Dict:
    """
    Creates a notebook JSON format
    """
    if format == '.py':
        notebook = {
        'cells': cells,
        'metadata': {
            'anaconda-cloud': {},
            'kernelspec': {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3'},
            'language_info': {
                'codemirror_mode': {'name': 'ipython', 'version': 3},
                'file_extension': '.py',
                'mimetype': 'text/x-python',
                'name': 'python',
                'nbconvert_exporter': 'python',
                'pygments_lexer': 'ipython3',
                'version': '3.6.1'}},
        'nbformat': 4,
        'nbformat_minor': 1
    }
    elif format == '.sql':
        notebook = {
        'cells': cells,
        'metadata': {
            'anaconda-cloud': {},
            'kernelspec': {
                'display_name': 'sql',
                'language': 'sql',
                'name': 'sql'},
            'language_info': {
                'file_extension': '.sql',
                'mimetype': 'text/x-sql',
                'name': 'sql',
                'nbconvert_exporter': 'sql'}},
        'nbformat': 4,
        'nbformat_minor': 1
    }
    else:
        raise(Exception(f'File extension not allowed. Allowed extensions are: {py_extension} or {sql_extension}'))
    return notebook
   
def any2nb(input_str: str, format:str) -> Dict:
    if format == py_extension:
        header_command = py_command_comment
        databricks_nb_start = py_databricks_nb_start
        markdown_comment = py_markdown_comment
        markdown_sandbox_comment = py_markdown_sandbox_comment
        magic_code = py_magic_code
    elif format == sql_extension:
        header_command = sql_command_comment
        databricks_nb_start = sql_databricks_nb_start
        markdown_comment = sql_markdown_comment
        markdown_sandbox_comment = sql_markdown_sandbox_comment
        magic_code = sql_magic_code
    else:
        raise(Exception(f'File extension not allowed. Allowed extensions are: {py_extension} or {sql_extension}'))
    
    # remove leading header comment
    if input_str.startswith(header_command):
        input_str = input_str[len(header_command):]

    # remove leading Databricks notebook start
    if input_str.startswith(databricks_nb_start):
        input_str = input_str[len(databricks_nb_start):]

    cells = []
    chunks = input_str.split('\n\n%s\n\n' % header_command)

    for chunk in chunks:
        
        cell_type = 'code'
        # remove markdown sandbox block comment
        if chunk.startswith(markdown_sandbox_comment):
            chunk = chunk[len(markdown_sandbox_comment):]
            chunk = chunk.strip("\n")
            chunk = chunk.replace(magic_code, '')
            cell_type = 'markdown'
        # remove markdown block comment
        elif chunk.startswith(markdown_comment) and not chunk.startswith(markdown_sandbox_comment):
            chunk = chunk[len(markdown_comment):]
            chunk = chunk.strip("\n")
            chunk = chunk.replace(magic_code, '')
            cell_type = 'markdown'

        elif chunk.startswith(magic_code):
            chunk = chunk.replace(magic_code, '')

        cell = {
            'cell_type': cell_type,
            'metadata': {},
            'source': chunk.splitlines(True),
        }

        if cell_type == 'code':
            cell.update({'outputs': [], 'execution_count': None})

        cells.append(cell)

    notebook = _get_notebook(cells=cells, format=format)

    return notebook

def convert_databricks_nb(in_file:str, out_file:str) -> NoReturn:
    """ This is the main funciton, figures out which 
        way the conversion is going (i.e. py -> ipynb, sql -> ipynb
        ipynb -> py) or throws an error message
    """
    _, in_ext = path.splitext(in_file)
    _, out_ext = path.splitext(out_file)

    if in_ext == nb_extension and out_ext == py_extension:
        with open(in_file, 'r') as f:
            notebook = json.load(f)
        py_str = nb2py(notebook)
        with open(out_file, 'w') as f:
            f.write(py_str)

    elif (in_ext == py_extension or in_ext == sql_extension) and out_ext == nb_extension:
        with open(in_file, 'r') as f:
            input_str = f.read()
        notebook = any2nb(format=in_ext, input_str=input_str)
        with open(out_file, 'w') as f:
            json.dump(notebook, f, indent=2)

    else:
        raise(Exception(f'File extension not allowed. Allowed extensions are: {nb_extension}, {py_extension} or {sql_extension}'))