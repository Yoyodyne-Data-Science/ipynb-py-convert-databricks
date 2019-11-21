import json
import sys
from os import path

header_comment = '# COMMAND ----------'
markdown_comment = "# MAGIC %md"
magic_code = "# MAGIC "
databricks_nb_start = "# Databricks notebook source\n"

def nb2py(notebook):
    """ Function for converting from notebook to py file
    """
    result = []
    cells = notebook['cells']
    
    for idx, cell in enumerate(cells):
        cell_type = cell['cell_type']

        if cell_type == 'markdown':
            cell_content = markdown_comment + "\n" + magic_code + \
                            ''.join(cell['source']).replace("\n", "\n"+magic_code)
            if idx == 0:
                cell_content = databricks_nb_start + cell_content 
            else:
                cell_content = cell_content
            result.append(cell_content)
    
        if cell_type == 'code':
            cell_content = ''.join(cell['source'])
            if idx == 0:
                cell_content = databricks_nb_start + cell_content
            else:
                cell_content = cell_content
            result.append(cell_content)
        
    return ("\n\n" + header_comment + "\n\n").join(result)


def py2nb(py_str):
    """ Function for converting from py file to notebook
    """
    # remove leading header comment
    if py_str.startswith(header_comment):
        py_str = py_str[len(header_comment):]
        
    # remove leading Databricks notebook start
    if py_str.startswith(databricks_nb_start):
        py_str = py_str[len(databricks_nb_start):]

    cells = []
    chunks = py_str.split('\n\n%s\n\n' % header_comment)
    #chunks = py_str.split('%s' % header_comment)

    for chunk in chunks:
        cell_type = 'code'
        if chunk.startswith(markdown_comment):
            chunk = chunk[len(markdown_comment):]
            chunk = chunk.strip("'\n")
            chunk = chunk.replace(magic_code, '')
            cell_type = 'markdown'

        cell = {
            'cell_type': cell_type,
            'metadata': {},
            'source': chunk.splitlines(True),
        }

        if cell_type == 'code':
            cell.update({'outputs': [], 'execution_count': None})

        cells.append(cell)

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

    return notebook


def convert_databricks_nb(in_file, out_file):
    """ This is the main funciton, figures out which 
        way the conversion is going (i.e. py -> ipynb or
        ipynb -> py) or throws an error message
    """
    _, in_ext = path.splitext(in_file)
    _, out_ext = path.splitext(out_file)

    if in_ext == '.ipynb' and out_ext == '.py':
        with open(in_file, 'r') as f:
            notebook = json.load(f)
        py_str = nb2py(notebook)
        with open(out_file, 'w') as f:
            f.write(py_str)

    elif in_ext == '.py' and out_ext == '.ipynb':
        with open(in_file, 'r') as f:
            py_str = f.read()
        notebook = py2nb(py_str)
        with open(out_file, 'w') as f:
            json.dump(notebook, f, indent=2)

    else:
        raise(Exception('Extensions must be .ipynb and .py or vice versa'))