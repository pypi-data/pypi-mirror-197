from functools import partial
from tkinter import Tk, Button, Scrollbar, Menu
from tkinter.constants import *
from tkinter.ttk import Treeview, Entry, Frame


# see https://www.youtube.com/watch?v=n5gItcGgIkk
# rowheight:https://stackoverflow.com/questions/26957845/ttk-treeview-cant-change-row-height/26962663#26962663

class mtkEditTableListener:
    def right_click_fired(self, event):
        pass

    def double_click_fired(self, event):
        pass


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
        self.listeners = []
        self.columns = kwargs["columns"]
        self.column_titles = None
        self.cells = None
        self.rowID = None
        self.current_cell_value = None
        # handling extra params
        if "column_titles" in kwargs.keys():
            self.column_titles = kwargs["column_titles"]
            del kwargs["column_titles"]
        if "cells" in kwargs.keys():
            self.cells = kwargs["cells"]
            del kwargs["cells"]
        #
        super().__init__(master, **kwargs)
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
        # events
        self.bind("<Double-1>", self._on_double_click)
        self.bind("<Button-3>", self._on_right_click)
        # right click menu - https://tkdocs.com/tutorial/menus.html
        self.menu = Menu(self.frame, tearoff=0)
        self.menu.add_command(label="Copy under", command=self.clone_after_current_row)
        self.menu.add_command(label="New empty line under", command=self.new_after_current_row)
        self.menu.add_separator()
        self.menu.add_command(label="Remove current", command=self.remove_current)
        # text & image : menu.add_command(label=txt, image=self._img4, compound='left', command=cmd)

    def add_listener(self, listener: mtkEditTableListener):
        found = False
        for l in self.listeners:
            if l == listener:
                found = True
        if not found:
            self.listeners.append(listener)

    def _on_right_click(self, event):
        self.rowID = self.identify('item', event.x, event.y)
        for listener in self.listeners:
            listener.right_click_fired(event)

        if self.rowID:
            self.selection_set(self.rowID)
            self.focus_set()
            self.focus(self.rowID)
            # self.menu.tk_popup(event.x_root, event.y_root)
            self.menu.post(event.x_root, event.y_root)
            self.current_cell_value = self.get_cell_value(event)

    def remove_current(self):
        """
        must be prepared with _on_right_click()
        """
        self.delete(self.rowID)

    def clone_after_current_row(self):
        """
        must be prepared with _on_right_click()
        """
        self.insert(parent="", index=int(self.rowID) + 1, iid=str(int(self.rowID) + 10000), text="",
                    values=("", self.current_cell_value))

    def new_after_current_row(self):
        """
        must be prepared with _on_right_click()
        """
        self.insert(parent="", index=int(self.rowID) + 1, iid=str(int(self.rowID) + 10000), text="",
                    values=("", self.current_cell_value))

    def clear_data(self):
        self.cells = None
        for row in self.get_children():
            self.delete(row)

    def set_data(self, json=None):
        self.clear_data()
        if json is not None:
            self.cells = json
        for key in self.cells.keys():
            print("-", key, "/", self.cells[key])
            if type(self.cells[key]) is dict:
                child_id = 0
                for child_key in self.cells[key].keys():
                    print("--", key, "/", child_key, "/", self.cells[key][child_key])
                    if child_id == 0:
                        parent = child_key
                        self.insert(parent="", index='end', iid=child_key, text=key, values=tuple(self.cells[key][child_key]))
                    else:
                        self.insert(parent=parent, index='end', iid=child_key, text="", values=tuple(self.cells[key][child_key]))
                    child_id += 1
            else:
                self.insert(parent="", index='end', iid=key, text="", values=tuple(self.cells[key]))
        Tk.update(self.master)

    def get_data(self) -> dict:
        """
        :return: a dict from the content
        """
        res = {}
        for i in self.get_children():
            print("--", self.item(i))
            text = self.item(i)['text']
            if text:
                res[text] = {}
                res[text][i] = self.item(i)['values']
                for j in self.get_children(i):
                    print("----", self.item(j))
                    res[text][j] = self.item(j)['values']
            else:
                data = self.item(i)['values']
                res[i] = data
        print(res)
        return res

    def get_cell_value(self, event):
        col_index = self.identify_column(event.x)
        selected_row_iid = self.focus()
        selected_values = self.item(selected_row_iid)
        values = selected_values.get("values")
        col_number = int(col_index[1:]) - 1
        return values[col_number]

    def get_cell_dimensions(self, event) -> ():
        col_index = self.identify_column(event.x)
        print("col_index", col_index)
        selected_row_iid = self.focus()
        if int(col_index[1:]) > 0:
            col_number = int(col_index[1:]) - 1
            return self.bbox(selected_row_iid, col_number)
        else:
            return self.bbox(selected_row_iid, col_index)

    def _on_double_click(self, event):
        """
        displays an entry field on top of the double-clicked cell
        :param event:
        :return:
        """
        print("_on_double_click")
        for listener in self.listeners:
            listener.double_click_fired(event)

        region_clicked = self.identify_region(event.x, event.y)
        if self.debug:
            print("region double clicked", region_clicked, event)
        col_index = self.identify_column(event.x)
        selected_row_iid = self.focus()
        selected_values = self.item(selected_row_iid)
        cell_box = self.get_cell_dimensions(event)
        print("cell_box", cell_box)
        col_number = 0
        if region_clicked == "cell":
            values = selected_values.get("values")
            col_number = int(col_index[1:]) - 1
            cell_value = self.get_cell_value(event)
            if self.debug:
                print("cell_value", cell_value)
        elif region_clicked == "tree":
            col_number = -1
            cell_value = selected_values.get("text")
            if self.debug:
                print("tree_value", cell_value)
        else:
            print("Header clicked")
        #
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
            self.edit_entry.insert(0, cell_value)
        else:
            self.edit_entry.insert(0, cell_value)
        self.edit_frame.place(x=cell_box[0], y=cell_box[1], w=cell_box[2], h=cell_box[3] * 2)
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
        self.edit_frame.destroy()
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
