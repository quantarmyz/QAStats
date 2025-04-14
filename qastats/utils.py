####
# QUANTARMY 2022 - PRIVATE CODE - ALL RIGTHS RESERVED
# QUANTARMY 2023 - PRIVATE CODE - ALL RIGTHS RESERVED
# QUANTARMY 2024 - GNU PUBLIC LICENSE (ALL SOURCE RELEASED)
# QUANTARMY 2025 - GNU PUBLIC LICENSE - OPEN SOURCE
# by jcx - jcx@quantarmy.com | https://quantarmy.com
####
# Noviembre 2022
# Enero 2023 - 
# Feb 2024 - Update 2.0
# Abril 2025 - Update 2.1
##### armystats v2
#
#### 
#To-Do
# -> Tests
import pandas as pd 
from scipy.stats import norm
from IPython.display import display, HTML


APPROX_BDAYS_PER_MONTH = 21
APPROX_BDAYS_PER_YEAR = 252
MONTHS_PER_YEAR = 12
WEEKS_PER_YEAR = 52
MM_DISPLAY_UNIT = 1000000.0
DAILY = "daily"
WEEKLY = "weekly"
MONTHLY = "monthly"
YEARLY = "yearly"

ANNUALIZATION_FACTORS = {
    DAILY: APPROX_BDAYS_PER_YEAR,
    WEEKLY: WEEKS_PER_YEAR,
    MONTHLY: MONTHS_PER_YEAR,
}


def two_dec_places(x, pos):
    """
    Adds 1/100th decimal to plot ticks.
    """
    return "%.2f" % x

def percentage(x, pos):
    """
    Adds percentage sign to plot ticks.
    """

    return "%.0f%%" % x

def print_table(table, name=None, float_format=None, formatters=None, header_rows=None):
    """
    Pretty print a pandas DataFrame.
    Uses HTML output if running inside Jupyter Notebook, otherwise
    formatted text output.
    Parameters
    ----------
    table : pandas.Series or pandas.DataFrame
        Table to pretty-print.
    name : str, optional
        Table name to display in upper left corner.
    float_format : function, optional
        Formatter to use for displaying table elements, passed as the
        `float_format` arg to pd.Dataframe.to_html.
        E.g. `'{0:.2%}'.format` for displaying 100 as '100.00%'.
    formatters : list or dict, optional
        Formatters to use by column, passed as the `formatters` arg to
        pd.Dataframe.to_html.
    header_rows : dict, optional
        Extra rows to display at the top of the table.
    """

    if isinstance(table, pd.Series):
        table = pd.DataFrame(table)

    if name is not None:
        table.columns.name = name

    html = table.to_html(float_format=float_format, formatters=formatters)

    if header_rows is not None:
        # Count the number of columns for the text to span
        n_cols = html.split("<thead>")[1].split("</thead>")[0].count("<th>")

        # Generate the HTML for the extra rows
        rows = ""
        for name, value in header_rows.items():
            rows += (
                '\n    <tr style="text-align: right;"><th>%s</th>'
                + "<td colspan=%d>%s</td></tr>"
            ) % (name, n_cols, value)

        # Inject the new HTML
        html = html.replace("<thead>", "<thead>" + rows)

    display(HTML(html))

def to_utc(df):
    """
    For use in tests; applied UTC timestamp to DataFrame.
    """

    try:
        df.index = df.index.tz_localize("UTC")
    except TypeError:
        df.index = df.index.tz_convert("UTC")

    return df
