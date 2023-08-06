from functools import reduce
import numpy as np
from hestia_earth.schema import UNIQUENESS_FIELDS, Term, NodeType
from hestia_earth.schema.utils.sort import get_sort_key

# __package__ = "hestia_earth.utils" # required to run interactively in vscode

from .tools import flatten
from .api import find_term_ids_by_names


PANDAS_IMPORT_ERROR_MSG = "Run `pip install pandas>=1.2` to use this functionality"
try:
    import pandas as pd
    version = [int(x) for x in pd.__version__.split('.')]
    if version[0] < 1 or (version[0] == 1 and version[1] < 2):
        raise ImportError(PANDAS_IMPORT_ERROR_MSG)
except ImportError:
    raise ImportError(PANDAS_IMPORT_ERROR_MSG)


# assuming column labels always camelCase
def _get_node_type_label(node_type):
    return node_type[0].lower() + node_type[1:]


def _get_name_id_dict(df):
    names = []
    for node_type, array_fields in UNIQUENESS_FIELDS.items():
        nt_label = _get_node_type_label(node_type)
        for array_field, uniqueness_fields in array_fields.items():
            for field in [f for f in uniqueness_fields if ".@id" in f]:
                name_field = field.replace(".@id", ".name")
                regex = rf"^{nt_label}\.{array_field}\.\d+\.{name_field}$"
                names_for_field = df.filter(regex=regex).to_numpy().flatten()
                names.extend(names_for_field)
    valid_names = [name for name in set(names) if pd.notna(name)]
    return find_term_ids_by_names(sorted(valid_names))


def _sort_keys(index):
    return [get_sort_key(col) for col in index]


def _sort_inplace(df):
    df.sort_index(axis=1, inplace=True, key=_sort_keys)


def _get_term_field(col_header):
    return ".".join(col_header.split(".")[3:])


def _get_term_index(col_header):
    return f"term.{col_header.split('.')[2]}"


def _group_by_term(term, name_id_dict, uniqueness_fields):
    term.columns = map(_get_term_field, term.columns)
    # fill in any missing ids prior to grouping by id
    replace_fields = {
        f: f.replace(".@id", ".name") for f in uniqueness_fields if ".@id" in f
    }
    for idField, nameField in replace_fields.items():
        term[idField] = term.apply(
            lambda row: row.get(
                idField,
                name_id_dict.get(row.get(nameField, "default_id_value"), np.nan),
            ),
            axis=1,
        )
        term.drop(nameField, axis=1, inplace=True, errors="ignore")
    return term


def _pivot_by_term(row, fields_to_include):
    value_col_fields = []
    series = {}
    for col, append_to_value_col in fields_to_include.items():
        if pd.notna(row[col]):
            if append_to_value_col:
                value_col_fields.append(col)
            else:
                series[f"{row['term.@id']}.{col}"] = row[col]
    value_col_fields.sort()
    value_col_prefix = f"{row['term.@id']}{'+' if len(value_col_fields) else ''}"
    value_col = f"{value_col_prefix}{'+'.join([f'{col}[{row[col]}]' for col in value_col_fields]) }.value"
    series[value_col] = row.get("value", default=np.nan)
    return pd.Series(series)


def _is_not_term_field(col):
    deepest_field = col.split(".")[-1]
    is_name = (
        deepest_field == "name"
    )  # workaround to keep name while we do not do 'deep' pivoting
    return is_name or deepest_field not in Term().fields


def _pivot_by_term_id_group(terms, uniqueness_fields):
    fields_to_include = {}
    for col in terms.columns:
        if col in uniqueness_fields:
            single_value = (
                terms[col].eq(terms[col].iloc[0]).all() or terms[col].isna().all()
            )
            append_to_value_col = (
                # depthUpper and depthLower are exceptions which go into value col no matter what
                col == "depthUpper"
                or col == "depthLower"
                or not single_value
            )
            fields_to_include[col] = append_to_value_col
        elif col != "value" and _is_not_term_field(col):
            fields_to_include[col] = False
    del fields_to_include["term.@id"]
    pivoted = terms.apply(_pivot_by_term, axis=1, fields_to_include=fields_to_include)
    return pivoted


def _pivot_row(row, uniqueness_fields):
    # unstack to group sets of values for each id, then stack to restore row
    # unstacking looks like this:
    #          term.@id dates	            startDate	value
    # term.0	gwp100	01-02-22;02-02-22	01-01-22	10;12
    # term.1	gwp100	01-02-22;02-02-22	02-01-22	20;30
    # term.2	someId	bla                 bla         1.0

    pivoted = (
        row.unstack()
        .groupby("term.@id", group_keys=False)
        .apply(_pivot_by_term_id_group, uniqueness_fields=uniqueness_fields)
    )
    return pivoted.stack(dropna=False)


def pivot_csv(filepath):
    """
    Pivot terms belonging to array fields of nodes, indexing their value directly with
    the term ID and any distinguishing uniqueness fields in the following format:
    node.arrayField.termId+uniquenessField1[value]+uniquenessField2etc[value]

    Parameters
    ----------
    filepath : str
        Path to the CSV to be formatted.

    Returns
    -------
    pandas.DataFrame
        Pandas dataframe with pivoted array terms
    """
    df_in = pd.read_csv(filepath, index_col=None, dtype=object)
    df_in.replace("-", np.nan, inplace=True)
    df_in.dropna(how="all", axis=1, inplace=True)
    df_in.drop(columns="-", errors="ignore", inplace=True)
    df_out = df_in.copy()
    name_id_dict = _get_name_id_dict(df_out)

    for node_type, array_fields in UNIQUENESS_FIELDS.items():
        nt_label = _get_node_type_label(node_type)
        for field in array_fields:
            regex = rf"^{nt_label}\.{field}\.\d+"
            uniqueness_fields = array_fields[field]
            field_cols = df_in.filter(regex=regex)

            with_grouped_cols = field_cols.groupby(
                _get_term_index, axis=1, group_keys=True
            ).apply(
                _group_by_term,
                name_id_dict=name_id_dict,
                uniqueness_fields=uniqueness_fields,
            )

            pivoted_terms = with_grouped_cols.apply(
                _pivot_row, axis=1, uniqueness_fields=uniqueness_fields
            )

            # merge any duplicated columns caused by shuffled term positions
            # this operation coincidentally sorts the columns alphabetically
            pivoted_terms = pivoted_terms.groupby(
                level=pivoted_terms.columns.nlevels - 1, axis=1, group_keys=False
            ).apply(lambda term: term.fillna(method="bfill", axis=1).iloc[:, 0])

            pivoted_terms.columns = map(
                lambda col: f"{nt_label}.{field}.{col}", pivoted_terms.columns
            )

            df_out.drop(df_out.filter(regex=regex).columns, axis=1, inplace=True)
            df_out = df_out.merge(
                pivoted_terms, left_index=True, right_index=True, how="outer"
            )
    _sort_inplace(df_out)
    df_out.fillna("-", inplace=True)
    return df_out


def _replace_ids(df):
    # in columns, first letter is always lower case
    node_types = [e.value[0].lower() + e.value[1:] for e in NodeType]
    # add extra subvalues
    subvalues = ["source", "defaultSource", "site", "organisation", "cycle"]
    node_types = node_types + flatten(
        [v + "." + value for v in node_types] for value in subvalues
    )
    columns = reduce(
        lambda prev, curr: {**prev, curr + ".@id": curr + ".id"}, node_types, {}
    )
    return df.rename(columns=columns)


def _clean_term_columns(df):
    columns = ["name", "termType", "units"]
    cols = [c for c in df.columns if all([not c.endswith("." + v) for v in columns])]
    return df[cols]


def _replace_nan_values(df, col: str, columns: list):
    for index, row in df.iterrows():
        try:
            value = row[col]
            if np.isnan(value):
                for empty_col in columns:
                    df.loc[index, empty_col] = np.nan
        except TypeError:
            continue
    return df


def _empty_impact_na_values(df):
    impacts_columns = [c for c in df.columns if ".impacts."]
    impacts_values_columns = [c for c in impacts_columns if c.endswith(".value")]
    for col in impacts_values_columns:
        col_prefix = col.replace(".value", "")
        same_col = [c for c in impacts_columns if c.startswith(col_prefix) and c != col]
        _replace_nan_values(df, col, same_col)
    return df


def format_for_upload(filepath: str):
    """
    Format downloaded file for upload on Hestia platform.
    Will replace all instances of `@id` to `id`, and drop the columns ending by `name`, `termType` or `units`.

    Parameters
    ----------
    filepath : str
        Path to the CSV to be formatted.

    Returns
    -------
    pandas.DataFrame
        Formatted pandas dataframe
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("Run `pip install pandas~=1.2.0` to use this functionality")

    df = pd.read_csv(filepath, index_col=None, na_values="")

    # replace @id with id for top-level Node
    df = _replace_ids(df)

    # drop all term columns that are not needed
    df = _clean_term_columns(df)

    # empty values for impacts which value are empty
    df = _empty_impact_na_values(df)

    return df
