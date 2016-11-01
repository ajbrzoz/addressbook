"""This module contains functions for serializing AddressBook objects to JSON or saving them as Excel files"""

import addressbook.ab_abook
import addressbook.ab_person
import datetime
import json
import pickle
import xlwt


def from_json(obj):
    """JSON decoder"""
    
    if "__class__" in obj:

        if obj["__class__"] == "ab_person.Person":
            obligatory = [obj["__value__"][key] for key in ["name", "surname", "email", "phone"]]
            new_object = addressbook.ab_person.Person(*obligatory)
            for key, val in obj["__value__"].items():
               if val not in obligatory:
                    new_object.__setattr__(key, val, conversion=True)
            return new_object

        if obj["__class__"] == "datetime.date":
            string_value = obj["__value__"]
            date_values = (int(n) for n in string_value.split("-"))
            year, month, day = date_values
            return datetime.date(year, month, day)

    return obj


def open_base(fformat, filename):
    """Main function for opening files that contain AddressBook (.pkl, .pickle, .json)"""

    if fformat == ".json":
        abook = open_json(filename)
    else:
        with open(filename, "rb") as abook_file:
            abook = pickle.load(abook_file)

    return abook


def open_json(filename):
    """Open JSON file as AddressBook"""

    with open(filename, "r", encoding="utf-8") as abook_file:
        json_object = json.load(abook_file, object_hook=from_json)
        
    abook = addressbook.ab_abook.AddressBook()

    for item in json_object:
        abook.append(item)

    return abook


def to_excel(gui, filename):
    """Save AddressBook to Excel file (.xls)"""

    wk = xlwt.Workbook()
    ws = wk.add_sheet("AddressBook")

    col_names = ["name", "surname", "email", "phone", "city", "streetname", "streetnumber", "birthday"]

    heading_style = xlwt.Style.easyxf("""
        font: bold on;
        borders: bottom thick, right thin;
        pattern: pattern solid, fore_colour gold;
        align: wrap on, vert centre, horiz center;
        """)

    for ix, col in enumerate(col_names):
        name = col.replace("n", " n") if col in ("streetname", "streetnumber") else col
        ws.write(0, ix, name.title(), heading_style)

    cell_style = xlwt.Style.easyxf("""
        borders: bottom thin, right thin;
        align: wrap on, vert centre, horiz center;
        """, num_format_str="yyyy-mm-dd")
        
    row = 1
    for item in gui.dashboard.data_list:    
        for n in range(0, 8):
            value = item[n]            
            col_width = ws.col(n).width
            if (len(str(value)) * 367) > col_width:
                ws.col(n).width = (len(str(value)) * 367)
            ws.write(row, n, value, cell_style)
        row += 1

    if not filename.endswith(".xls"):
        filename += ".xls"

    wk.save(filename)


def to_json(obj):
    """JSON encoder"""

    if str(type(obj)) == "<class 'ab_person.Person'>" or str(type(obj)) == "<class 'addressbook.ab_person.Person'>":
    
        return {"__class__": "ab_person.Person", "__value__": obj.__dict__}

    if isinstance(obj, datetime.date):
        return {"__class__": "datetime.date", "__value__": str(obj)}

    raise TypeError(repr(obj) + "is not JSON serializable")
