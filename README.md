# ipynb-py-convert-databricks

Function for un- and re- doing the conversion from .ipynb ipython notebook to .py python file which Databricks performs every time it exports a notebook. Building on code from [kiwi0fruit/ipynb-py-convert](https://github.com/kiwi0fruit/ipynb-py-convert)

## Why?

Databricks exports `.ipynb` files (e.g. when version controlling) as `.py`, which is pretty handy as it's easier to deal with a straight up python script file than a JSON formatted IPython notebook. However, it would be nice to perform the reverse operation, e.g. when we download a databricks notebook and want to run it in a local anaconda notebook.

## How?

Conversion is possible both ways; from the `.py` version made by databricks to an IPython notebook:

`convert_databricks_nb('databricks_nb.py', 'databricks_nb.ipynb')`

And from an IPython notebook to a `.py` file (i.e. a function presumably similar to the one Databricks itself runs before exporting notebooks):

`convert_databricks_nb('databricks_nb.ipynb','databricks_nb.py')`

## Example

Let's say we write the following notebook in databricks:
<p align="center">
  <img width="460" src="example_databricks_notebook.png">
</p>
