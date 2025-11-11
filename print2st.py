import uuid
from typing import Any

import pandas as pd
import streamlit as st

def print_one(arg:Any = ""):
    key = str(uuid.uuid4())
    if isinstance(arg, list):
        data = []
        lst = arg
        for item in lst:
            if hasattr(item, '__dict__'):
                # For objects, use their dictionary of attributes
                data.append(item.__dict__)
            else:
                # For simple data types, create a dictionary with a default key
                data.append({'value': item})

        df = pd.DataFrame(data)
        # df = pd.DataFrame([obj.__dict__ for obj in arg])
        df.columns = [column.capitalize() for column in df.columns]
        st.data_editor(df, #num_rows="dynamic",
                       key=key,
                       hide_index=True,
                       disabled=True,
                       use_container_width=True)
    else:
        st.write(arg)


def print(*args):
    for arg in args:
        print_one(arg)

# input("Press Enter to continue...")