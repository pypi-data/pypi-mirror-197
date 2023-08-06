from functools import partial
from tkinter import Tk, Button, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview, Entry, Frame


# see https://www.youtube.com/watch?v=n5gItcGgIkk
# rowheight:https://stackoverflow.com/questions/26957845/ttk-treeview-cant-change-row-height/26962663#26962663

class mtkEditTable(Treeview):
    """
    Editable table based on a TreeView => all Treeview features can be used

    * set self.debug to True for debugging
    * kwargs["columns"]: ex = ("A", "B", "C")
    * kwargs["column_titles"]: ex = ("col A", "col B", "col C")
    * kwargs["cells"]: ex = {"0": ["ZER", "TYU", "IOP"],
            "1": ["QSD", "FGH", "JKL"]
            }
    """

    def __init__(self, master, **kwargs):
        self.frame = master
        self.debug = False
        self.edit_frame = None
        self.horscrlbar = None
        self.edit_entry = None

        self.columns = kwargs["columns"]
        self.column_titles = None
        self.cells = None
        # handling extra params
        if "column_titles" in kwargs.keys():
            self.column_titles = kwargs["column_titles"]
            del kwargs["column_titles"]
        if "cells" in kwargs.keys():
            self.cells = kwargs["cells"]
            del kwargs["cells"]
        #
        super().__init__(master, **kwargs)
        # events
        print("<Double-1>")
        self.bind("<Double-1>", self._on_double_click)
        # set layout
        if self.column_titles:
            self.column("#0", width=0, stretch=NO)
            for (col_id, t) in zip(kwargs["columns"], self.column_titles):
                self.column(col_id, anchor=W, width=30)
                self.heading(col_id, text=t, anchor=CENTER)
        # set data
        if self.cells:
            self.set_data(self.cells)
        else:
            self.clear_data()

    def clear_data(self):
        self.cells = None
        for row in self.get_children():
            self.delete(row)

    def set_data(self, json=None):
        self.clear_data()
        if json is not None:
            self.cells = json
        for row in self.cells.keys():
            self.insert(parent="", index='end', iid=row, text="", values=tuple(self.cells[row]))
        Tk.update(self.master)

    def get_data(self) -> dict:
        """
        :return: a dict from the content
        """
        res = {}
        for i in self.get_children():
            data = self.item(i)['values']
            row = []
            res[i] = data
        return res

    def _on_double_click(self, event):
        """
        displays an entry field on top of the double-clicked cell
        :param event:
        :return:
        """
        print("_on_double_click")
        region_clicked = self.identify_region(event.x, event.y)
        if self.debug:
            print("region double clicked", region_clicked, event)
        if region_clicked == "cell":
            col_index = self.identify_column(event.x)
            selected_row_iid = self.focus()
            selected_values = self.item(selected_row_iid)
            values = selected_values.get("values")
            col_number = int(col_index[1:]) - 1
            cell_value = values[col_number]
            cell_box = self.bbox(selected_row_iid, col_number)
            if self.debug:
                print("cell_box", cell_box)
            self.edit_frame = Frame(self.master)
            self.edit_entry = Entry(self.edit_frame, width=cell_box[2])
            self.edit_entry.pack()
            self.horscrlbar = Scrollbar(self.edit_frame, orient="horizontal", width=20, command=self.edit_entry.xview)
            self.horscrlbar.pack(fill=BOTH, expand=1)
            self.edit_entry.configure(xscrollcommand=self.horscrlbar.set)
            # values recorded for _on_return_pressed
            self.edit_entry.editing_column_index = col_number
            self.edit_entry.editing_item_iid = selected_row_iid
            # only cells are editable / not the tree part
            if col_number > -1:
                self.edit_frame.place(x=cell_box[0], y=cell_box[1], w=cell_box[2], h=cell_box[3] * 2)
                print("winfo_rooty", self.winfo_rooty())
                self.edit_entry.insert(0, cell_value)
                self.edit_entry.select_range(0, END)
                self.edit_entry.focus()
                self.edit_entry.bind("<FocusOut>", self._on_focus_out)
                self.edit_entry.bind("<Return>", self._on_return_pressed)
                self.edit_entry.bind("<Escape>", self._on_focus_out)

    def _on_focus_out(self, event):
        """
        when focus is lost, the entry box is discarded
        :param event:
        :return:
        """
        self.edit_frame.destroy()
        # self.horscrlbar = None
        # self.edit_entry = None
        # event.widget.destroy()

    def _on_return_pressed(self, event):
        """
        when RETURN the cell is replaced by the entry
        :param event:
        :return:
        """
        new_text = event.widget.get()
        col_index = event.widget.editing_column_index
        selected_row_iid = event.widget.editing_item_iid
        selected_values = self.item(selected_row_iid)
        if col_index > -1:
            values = selected_values.get("values")
            values[col_index] = new_text
            self.item(selected_row_iid, values=values)
        else:
            self.item(selected_row_iid, text=new_text)
        event.widget.destroy()
        self.cells = self.get_data()


def __do_test_extract(a_met: mtkEditTable):
    """
    only for test purpose on met.get_data()
    :param a_met:
    :return:
    """
    j = a_met.get_data()
    print(j)


if __name__ == "__main__":
    print("mtkEditTable demo")
    root = Tk()
    col_ids = ("A", "B", "C")
    col_titles = ("col A", "col B", "col C")
    data = {"0": ["ZER", "TYU", "IOP"],
            "1": ["QSD", "FGH", "JKL"]
            }
    met = mtkEditTable(root, columns=col_ids, column_titles=col_titles, cells=data)
    met.debug = True
    met.pack(fill=BOTH, expand=True)
    extract = Button(root, text='Extract to file', command=partial(__do_test_extract, met))
    extract.pack()
    root.mainloop()
