from IPython import get_ipython


def invoke_ipython_sql_magic() -> None:
    ipython = get_ipython()

    already_invoked = ipython.find_magic("sql")
    if already_invoked is None:
        ipython.magic("load_ext sql")
        return print("ipython magic sql made available.")
    else:
        return


def connect_to_db(conn_str: str):
    get_ipython().magic(f"sql {conn_str}")
    return

