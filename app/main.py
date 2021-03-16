import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from packages import pdf_reader


def open_file():
    path = os.getcwd()

    # dont open Tk's mainframe
    Tk().withdraw()

    # open file dialog
    filedata = askopenfilename(initialdir=path,
                               filetypes=(("PDF", "*.pdf"),
                                          ("All files", "*.*")),
                               title="Select a PDF file."
                               )

    print(f'Loaded file: {filedata}')

    try:
        if filedata.endswith('.pdf'):
            pdf_reader.get_data(filedata)
    except:
        print('Something went wrong.')


open_file()
