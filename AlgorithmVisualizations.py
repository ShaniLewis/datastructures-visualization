#! /usr/bin/env python3
__doc__ = """
Program to show algorithm visualizations in a tabbed Tk notebook presentation
form.
This progam loads all the visualization modules in a give set of directories.
It searches the modules for classes that are subclasses of VisualizationApp 
and instantiates each one in a separate tab.  When the user clicks on a
tab, it calls the class's runVisualization method.
"""

import argparse, sys
from tkinter import *
from tkinter import ttk
from PythonVisualizations import VisualizationApp
import PythonVisualizations

def findVisualizations(module, verbose=0):
    classes = []
    for name in dir(module):
        this = getattr(module, name)
        if isinstance(this, type(VisualizationApp)) and (
                hasattr(this, 'runVisualization') and
                isinstance(getattr(this, 'runVisualization'),
                           type(VisualizationApp.runVisualization)) and
                this is not VisualizationApp):
            classes.append(this)
        elif verbose > 1:
            print('Ignoring {}.{} of type {}'.format(
                module.__name__, name, type(this)), file=sys.stderr)
    return classes

TAB_FONT = ('Calibri', 16)
INTRO_FONT = ('Helvetica', 16)

intro_msg = """
Welcome to the algorithm visualizations for the book:
Data Structures and Algorithms in Python

Please use these visualization tools along with the
book to improve your understanding of how computers
organize and manipulate data efficiently.

Select tabs at the top to see the different data structures.


The students of the Computer Science Department of
Stern College at Yeshiva University
developed these visualizations.
https://www.yu.edu/stern/ug/computer-science
"""

def showVisualizations(   # Display a set of VisualizationApps in a ttk.Notebook
        classes, start=None, title="Algorithm Visualizations", verbose=0):
    top = Tk()
    top.title(title)
    ttk.Style().configure("TNotebook.Tab", font=TAB_FONT,
                          padding=[12, TAB_FONT[1] * 5 // 8, 12, 2])
    notebook = ttk.Notebook(top)
    intro = ttk.Frame(notebook)
    for line in intro_msg.split('\n'):
        ttk.Label(intro, text=line, font=INTRO_FONT).pack()
    notebook.add(intro, state=NORMAL, text='Introduction', padding=8)
    for app in classes:
        if verbose > 1:
            print('Found app {} and instantiating'.format(app.__name__),
                  file=sys.stderr)
        pane = ttk.Frame(notebook)
        vizApp = app(window=pane)
        name = getattr(vizApp, 'title', app.__name__)
        notebook.add(pane, text=name)
        if start and start.lower() in (app.__name__.lower(), name.lower()):
            notebook.select(pane)
    notebook.pack(expand=True, fill=BOTH)
    top.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-s', '--start', 
        help='Starting tab.  '
        'Should match one of the visualization module titles or class name.')
    parser.add_argument(
        '-t', '--title',  default='Algorithm Visualizations',
        help='Title for top level window')
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='Add verbose comments')
    args = parser.parse_args()

    showVisualizations(findVisualizations(PythonVisualizations, args.verbose),
                       start=args.start, title=args.title)
