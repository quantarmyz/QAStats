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

import calendar
import datetime
import os
from collections import OrderedDict
from functools import wraps
from .randomizer import *
import empyrical as ep
import matplotlib
import matplotlib as mpl
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
import scipy as sp
import seaborn as sns
from .stats import *
from .timeseries import *
from .utils import *
from matplotlib import figure, font_manager
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.ticker import FuncFormatter
from .utils import APPROX_BDAYS_PER_MONTH, APPROX_BDAYS_PER_YEAR

def customize(func):
    """
    Con esta funcion llamamos a todas las plantillas de estilo que utilizamos.
    """
    @wraps(func)
    def call_w_context(*args, **kwargs):
        set_context = kwargs.pop("set_context", True)
        if set_context:
            with plotting_context(), axes_style():
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return call_w_context

def plotting_context(context="notebook", font_scale=1.75, rc=None):
    """
    Create pyfolio default plotting style context.
    Under the hood, calls and returns seaborn.plotting_context() with
    some custom settings. Usually you would use in a with-context.
    Parameters
    ----------
    context : str, optional
        Name of seaborn context.
    font_scale : float, optional
        Scale font by factor font_scale.
    rc : dict, optional
        Config flags.
        By default, {'lines.linewidth': 1.5}
        is being used and will be added to any
        rc passed in, unless explicitly overriden.
    Returns
    -------
    seaborn plotting context
    Example
    -------
    >>> with pyfolio.plotting.plotting_context(font_scale=2):
    >>>    pyfolio.create_full_tear_sheet(..., set_context=False)
    See also
    --------
    For more information, see seaborn.plotting_context().
    """
    if rc is None:
        rc = {}

    rc_default = {"lines.linewidth": 1.25}

    # Add defaults if they do not exist
    for name, val in rc_default.items():
        rc.setdefault(name, val)

    return sns.plotting_context(context=context, font_scale=font_scale, rc=rc)

def axes_style(style="darkgrid", rc=None):
    """
    Create pyfolio default axes style context.
    Under the hood, calls and returns seaborn.axes_style() with
    some custom settings. Usually you would use in a with-context.
    Parameters
    ----------
    style : str, optional
        Name of seaborn style.
    rc : dict, optional
        Config flags.
    Returns
    -------
    seaborn plotting context
    Example
    -------
    >>> with pyfolio.plotting.axes_style(style='whitegrid'):
    >>>    pyfolio.create_full_tear_sheet(..., set_context=False)
    See also
    --------
    For more information, see seaborn.plotting_context().
    """
    if rc is None:
        rc = {}

    rc_default = {}

    # Add defaults if they do not exist
    for name, val in rc_default.items():
        rc.setdefault(name, val)
    return sns.axes_style(style=style, rc=rc)

def plot_ref(ax, dark, **kwargs):
    if ax is None:
        fig, ax = plt.subplots(figsize=(0.7,0.7))

    if dark == True:
        color1 = 'grey'
        color2 = 'red'
        color3 = 'white'
    else:
        color1 = 'black'
        color2 = 'black'
        color3 = 'black'

    ax.set_ylim(0,1)
    ax.set_xlim(0,1)
    ax.text(0.5, 0.9, 'QUANTARMY', fontname='Source Code Pro', weight='bold', ha='center', size=46, color='blue')
    ax.text(0.5, 0.8, 'QAMGF: QuantArmy Module for Generate Factsheets - version:0.1-beta', weight='bold', ha='center', size=12, color=color1)
    ax.text(0.5, 0.70, 'ALL RIGHTS RESERVED - CLASSIFICATED INFORMATION : UNDER NDA AGREEGEMENT', ha='center', size=8, color=color2)
    ax.text(0.5, 0.75, 'This report has disclaimer and disclosures, for more information contact with jcx@quantarmy.com', ha='center', size=8, color=color3)
    ax.axis('off')
    return ax

def plot_rolling_returns(
    returns,
    factor_returns=None,
    live_start_date=None,
    logy=True,
    cone_std=[0.25,0.5,1.25,2],
    legend_loc="best",
    volatility_match=False,
    cone_function=forecast_cone_bootstrap,
    ax=None,
    vami=None,
    marca_blanca=False,
    **kwargs,
):
    """
    Plotea los retornos acumulados rolantes contra un factor(benchmark)
    Los resultados del modelo dentro de muestra, salen en verde, los periodos fuera de muestra, en rojo.
    Ademas de unas bandas no parametricas de expectativas, añadidas a la zona fuera de muestra.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series, optional
        Daily noncumulative returns of the benchmark factor to which betas are
        computed. Usually a benchmark such as market returns.
         - This is in the same style as returns.
    live_start_date : datetime, optional
        The date when the strategy began live trading, after
        its backtest period. This date should be normalized.
    logy : bool, optional
        Whether to log-scale the y-axis.
    cone_std : float, or tuple, optional
        If float, The standard deviation to use for the cone plots.
        If tuple, Tuple of standard deviation values to use for the cone plots
         - See forecast_cone_bounds for more details.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
    volatility_match : bool, optional
        Whether to normalize the volatility of the returns to those of the
        benchmark returns. This helps compare strategies with different
        volatilities. Requires passing of benchmark_rets.
    cone_function : function, optional
        Function to use when generating forecast probability cone.
        The function signiture must follow the form:
        def cone(in_sample_returns (pd.Series),
                 days_to_project_forward (int),
                 cone_std= (float, or tuple),
                 starting_value= (int, or float))
        See forecast_cone_bootstrap for an example.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=(5,12))
    sns.set(font='Bloomberg')
    ax.set_xlabel("")
    ax.set_ylabel("Retornos (%)" if not logy else "Retornos Logaritmicos Log(%)",font='Bloomberg')
    ax.set_yscale("log" if logy else "linear")

    if volatility_match and factor_returns is None:
        raise ValueError("Para ajustar a volatilidad, se necesita un factor de ajuste (bench)")
    elif volatility_match and factor_returns is not None:
        bmark_vol = factor_returns.loc[returns.index].std()
        returns = (returns / returns.std()) * bmark_vol

    returns = returns
    cum_rets = ep.cum_returns(returns, 1.0)

    y_axis_formatter = FuncFormatter(two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    if factor_returns is not None:
        cum_factor_returns = ep.cum_returns(factor_returns[cum_rets.index], 1.0)
        cum_factor_returns.plot(
            lw=2.22,
            color="#0068ff",
            label="Factor",
            alpha=0.60,
            ax=ax,
            **kwargs,
        )

    if live_start_date is not None:
        is_cum_returns = cum_rets.loc[cum_rets.index < live_start_date]
        oos_cum_returns = cum_rets.loc[cum_rets.index >= live_start_date]
    else:
        is_cum_returns = cum_rets
        oos_cum_returns = pd.Series([], dtype="float64")

    is_cum_returns.plot(
        lw=2.29, color="#fb8b1e", alpha=0.6, label="Model", ax=ax, **kwargs
    )

    if len(oos_cum_returns) > 0:
        oos_cum_returns.plot(
            lw=4, color="blue", alpha=0.6, label="OOS", ax=ax, **kwargs
        )

        if cone_std is not None:
            if isinstance(cone_std, (float, int)):
                cone_std = [cone_std]

            is_returns = returns.loc[returns.index < live_start_date]
            cone_bounds = cone_function(
                is_returns,
                len(oos_cum_returns),
                cone_std=cone_std,
                starting_value=is_cum_returns[-1],
            )

            cone_bounds = cone_bounds.set_index(oos_cum_returns.index)
            for std in cone_std:
                ax.fill_between(
                    cone_bounds.index,
                    cone_bounds[float(std)],
                    cone_bounds[float(-std)],
                    color="royalblue",
                    alpha=0.5,
                )

    if legend_loc is not None:
        ax.legend(loc=legend_loc, frameon=True, framealpha=0.5)
    ax.axhline(0.0, linestyle="--", color="black", lw=1)

    font_files = font_manager.findSystemFonts(fontpaths=os.getcwd())
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    if marca_blanca==False:
        ax.annotate('QA',#0.85 .20
                    xy=(0.85, .25), xycoords='figure fraction',
                    horizontalalignment='right', verticalalignment='top',
                    fontsize=45, color='blue',
                    fontname='Source Code Pro',
                    weight='bold',
                    alpha=0.4)
    ax.set_title("Retornos Acumulados en (%)")

    return ax

    def plot_drawdown_underwater(returns, ax=None, **kwargs):
        """
    Plots how far underwaterr returns are over time, or plots current
    drawdown vs. date.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
            - See full explanation in tears.create_full_tear_sheet.
        ax : matplotlib.Axes, optional
            Axes upon which to plot.
        **kwargs, optional
            Passed to plotting function.
        Returns
        -------
        ax : matplotlib.Axes
            The axes that were plotted on.
        """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(percentage)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    df_cum_rets = ep.cum_returns(returns, starting_value=1.0)
    running_max = np.maximum.accumulate(df_cum_rets)
    underwater = -100 * ((running_max - df_cum_rets) / running_max)
    underwater.plot(ax=ax, kind="area", color="blue", alpha=0.7, **kwargs)
    ax.set_ylabel("Drawdown")
    ax.set_title("Underwater")
    ax.set_xlabel("QA - 2023")
    return ax

def plot_monthly_returns_heatmap(returns, ax=None,marca_blanca=False, **kwargs):
    """
    Plots a heatmap of returns by month.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to seaborn plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    monthly_ret_table = ep.aggregate_returns(returns, "monthly")
    monthly_ret_table = monthly_ret_table.unstack().round(3)

    monthly_ret_table.rename(
        columns={i: m for i, m in enumerate(calendar.month_abbr)}, inplace=True
    )

    sns.heatmap(
        monthly_ret_table.fillna(0) * 100.0,
        annot=True,
        annot_kws={"size": 9},
        alpha=1.0,
        center=0.0,
        cbar=False,
        cmap=matplotlib.cm.seismic.reversed(),
        ax=ax,
        **kwargs,
    )
    ax.set_ylabel("Año")
    ax.set_xlabel("Mes")
    ax.set_title("Retorno Mensual (%)")

def plot_annual_returns(returns, ax=None,marca_blanca=False, **kwargs):
    """
    Plots a bar graph of returns by year.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    x_axis_formatter = FuncFormatter(percentage)
    ax.xaxis.set_major_formatter(FuncFormatter(x_axis_formatter))
    ax.tick_params(axis="x", which="major")

    ann_ret_df = pd.DataFrame(ep.aggregate_returns(returns, "yearly"))

    ax.axvline(
        100 * ann_ret_df.values.mean(),
        color='blue',
        linestyle="--",
        lw=1,
        alpha=0.7,
    )
    (100 * ann_ret_df.sort_index(ascending=False)).plot(
        ax=ax, kind="barh", alpha=0.70,color='royalblue',**kwargs
    )
    ax.axvline(0.0, color="black", linestyle="-", lw=2)
    ax.set_ylabel("Año")
    ax.set_xlabel("Retornos")
    ax.set_title("Return por Año")
    ax.legend(["Mean"], frameon=True, framealpha=0.5)

    if marca_blanca==False:
        ax.annotate('QA',#0.85 .20
                    xy=(0.85, .25), xycoords='figure fraction',
                    horizontalalignment='right', verticalalignment='top',
                    fontsize=74, color='blue',
                    fontname='Source Code Pro',
                    weight='bold',
                    alpha=0.4)
    ax.set_title("Retornos Acumulados en (%)")
    return ax

def plot_monthly_returns_dist(returns, marca_blanca=False,ax=None, **kwargs):
    """
    Plots a distribution of monthly returns.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    x_axis_formatter = FuncFormatter(percentage)
    ax.xaxis.set_major_formatter(FuncFormatter(x_axis_formatter))
    ax.tick_params(axis="x", which="major")

    monthly_ret_table = ep.aggregate_returns(returns, "monthly")

    ax.hist(
        100 * monthly_ret_table,
        color="royalblue",
        alpha=0.95,
        bins=30,
        **kwargs,
    )

    ax.axvline(
        100 * monthly_ret_table.mean(),
        color="red",
        linestyle="--",
        lw=2,
        alpha=1.0,
    )

    ax.axvline(0.0, color="black", linestyle="-", lw=1, alpha=0.75)
    ax.legend(["Media de los retornos mensuales"], frameon=True, framealpha=0.5)
    ax.set_ylabel("Numero de meses")
    ax.set_xlabel("Retornos")
    ax.set_title("Distribucion de los retornos mensuales")
    if marca_blanca==False:
        ax.annotate('QA',#0.85 .20
                    xy=(0.5, .50), xycoords='figure fraction',
                    horizontalalignment='center', verticalalignment='center',
                    fontsize=300, color='blue',
                    fontname='Source Code Pro',
                    weight='bold',
                    alpha=0.05)
    return ax

def plot_monthly_returns_timeseries(returns,ax=None, **kwargs):
    """
    Plots monthly returns as a 
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to seaborn plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    def cumulate_returns(x):
        return ep.cum_returns(x)[-1]

    if ax is None:
        ax = plt.gca()

    monthly_rets = returns.resample("M").apply(lambda x: cumulate_returns(x))
    monthly_rets = monthly_rets.to_period()
    monthly_rets = monthly_rets * 100

    sns.barplot(x=monthly_rets.index, y=monthly_rets.values, color="royalblue",**kwargs,ax=ax)

    _, labels = plt.xticks()
    plt.setp(labels, rotation=90)

    # only show x-labels on year boundary
    xticks_coord = []
    xticks_label = []
    count = 0
    for i in monthly_rets.index:
        if i.month == 1 and i.year % 3 == 0:
            xticks_label.append(i)
            xticks_coord.append(count)
            # plot yearly boundary line
            ax.axvline(count, color="black", ls="--", alpha=0.4)

        count += 1

    ax.axhline(0.0, color="darkgray", ls="-")
    ax.set_xlabel("")
    ax.set_ylabel("Retornos Mensuales en porcentaje (%)")
    ax.set_yscale("linear")
    ax.set_xticks(xticks_coord)
    ax.set_xticklabels(xticks_label)
    ax.set_title("Retornos Acumulados en (%)", fontsize=14)

    return ax

def plot_drawdown_underwater(returns,marca_blanca=False, ax=None, **kwargs):    
    """
    Plots how far underwaterr returns are over time, or plots current
    drawdown vs. date.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(percentage)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    df_cum_rets = ep.cum_returns(returns, starting_value=1.0)
    running_max = np.maximum.accumulate(df_cum_rets)
    underwater = -100 * ((running_max - df_cum_rets) / running_max)
    underwater.plot(ax=ax, kind="area", color='darkred',lw=3, alpha=0.7, **kwargs)
    ax.set_ylabel("Drawdown (%)")
    ax.set_title("Underwater Mark", fontsize=14)
    ax.set_xlabel("Time")

    if marca_blanca==False:
        ax.annotate('QA',#0.85 .20
                    xy=(0.5, 0.5), xycoords='figure fraction',
                    horizontalalignment='right', verticalalignment='top',
                    fontsize=74, color='blue',
                    fontname='Source Code Pro',
                    weight='bold',
                    alpha=0.3)
    return ax

def plot_drawdown_periods(returns, marca_blanca=False, top=10, ax=None, **kwargs):
    """
    Plots cumulative returns highlighting top drawdown periods.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    top : int, optional
        Amount of top drawdowns periods to plot (default 10).
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if not ax:
        fig, ax = plt.subplots(figsize=(4,10))

    y_axis_formatter = FuncFormatter(two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    df_cum_rets = ep.cum_returns(returns, starting_value=1.0)
    df_drawdowns = gen_drawdown_table(returns, top=top)

    df_cum_rets.plot(ax=ax,lw=3, **kwargs)

    lim = ax.get_ylim()
    colors = sns.cubehelix_palette(len(df_drawdowns),start=44,dark=0.5,light=0.9,hue=0.6)[::-1]
    for i, (peak, recovery) in df_drawdowns[["Peak date", "Recovery date"]].iterrows():
        if pd.isnull(recovery):
            recovery = returns.index[-1]
        ax.fill_between((peak, recovery), lim[0], lim[1], alpha=0.4, color=colors[i])
    ax.set_ylim(lim)
    ax.set_title("Top %i drawdown periods" % top, fontsize=14)
    ax.set_ylabel("Cumulative returns")
    ax.legend(["Portfolio"], loc="upper left", frameon=True, framealpha=0.5)
    ax.set_xlabel("")
    if marca_blanca==False:
        ax.annotate('QA',#0.85 .20
                    xy=(0.85, .15), xycoords='figure fraction',
                    horizontalalignment='right', verticalalignment='top',
                    fontsize=45, color='blue',
                    fontname='Source Code Pro',
                    weight='bold',
                    alpha=0.4)
    return ax

def plot_rolling_volatility(
    returns,
    factor_returns=None,
    rolling_window=APPROX_BDAYS_PER_MONTH * 6,
    legend_loc="best",
    ax=None,
    marca_blanca=False,
    **kwargs,
):
    """
    Plots the rolling volatility versus date.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series, optional
        Daily noncumulative returns of the benchmark factor for which the
        benchmark rolling volatility is computed. Usually a benchmark such
        as market returns.
         - This is in the same style as returns.
    rolling_window : int, optional
        The days window over which to compute the volatility.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    rolling_vol_ts = rolling_volatility(returns, rolling_window)
    rolling_vol_ts.plot(alpha=0.7, lw=2, color="royalblue", ax=ax, **kwargs)
    if factor_returns is not None:
        rolling_vol_ts_factor = rolling_volatility(
            factor_returns, rolling_window
        )
        rolling_vol_ts_factor.plot(alpha=0.7, lw=2, color="grey", ax=ax, **kwargs)

    ax.set_title("Rolling volatility (6-month)")
    ax.axhline(rolling_vol_ts.mean(), color="orangered", linestyle="--", lw=2)

    ax.axhline(0.0, color="black", linestyle="--", lw=1, zorder=2)

    ax.set_ylabel("Volatility")
    ax.set_xlabel("")
    if factor_returns is None:
        ax.legend(
            ["Volatility", "Average volatility"],
            loc=legend_loc,
            frameon=True,
            framealpha=0.5,
        )
    else:
        ax.legend(
            ["Volatility", "Benchmark volatility", "Average volatility"],
            loc=legend_loc,
            frameon=True,
            framealpha=0.5,
        )
    if marca_blanca==False:
        ax.annotate('QA',#0.85 .20
                    xy=(0.85, .10), xycoords='figure fraction',
                    horizontalalignment='right', verticalalignment='top',
                    fontsize=45, color='blue',
                    fontname='Source Code Pro',
                    weight='bold',
                    alpha=0.4)
    ax.set_title("Rolling Volaility (6-Months) ratio corr:" + str(round(rolling_vol_ts.corr(rolling_vol_ts_factor),2)))
    return ax

    """
    Plots the rolling 6-month and 12-month beta versus date.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series
        Daily noncumulative returns of the benchmark factor to which betas are
        computed. Usually a benchmark such as market returns.
         - This is in the same style as returns.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    ax.set_title("Rolling portfolio beta to " + str(factor_returns.name))
    ax.set_ylabel("Beta")
    rb_1 = rolling_beta(
        returns, factor_returns, rolling_window=APPROX_BDAYS_PER_MONTH * 6
    )
    rb_1.plot(color="royalblue", lw=2, alpha=0.6, ax=ax, **kwargs)
    rb_2 = rolling_beta(
        returns, factor_returns, rolling_window=APPROX_BDAYS_PER_MONTH * 12
    )
    rb_2.plot(color="grey", lw=2, alpha=0.4, ax=ax, **kwargs)
    ax.axhline(rb_1.mean(), color="royalblue", linestyle="--", lw=2)
    ax.axhline(1.0, color="black", linestyle="--", lw=1)

    ax.set_xlabel("")
    ax.legend(
        ["6-mo", "12-mo", "6-mo Average"],
        loc=legend_loc,
        frameon=True,
        framealpha=0.5,
    )
    # ax.set_ylim((-0.5, 1.5))
    return ax

def plot_rolling_beta(returns, factor_returns, legend_loc="best", ax=None, **kwargs):
    """
    Plots the rolling 6-month and 12-month beta versus date.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series
        Daily noncumulative returns of the benchmark factor to which betas are
        computed. Usually a benchmark such as market returns.
         - This is in the same style as returns.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    ax.set_title("Rolling portfolio beta to Factor")
    ax.set_ylabel("Beta")
    rb_1 = rolling_beta(
        returns, factor_returns, rolling_window=APPROX_BDAYS_PER_MONTH * 6
    )
    rb_1.plot(color="royalblue", lw=2, alpha=0.6, ax=ax, **kwargs)
    rb_2 = rolling_beta(
        returns, factor_returns, rolling_window=APPROX_BDAYS_PER_MONTH * 12
    )
    rb_2.plot(color="grey", lw=2, alpha=0.4, ax=ax, **kwargs)
    ax.axhline(rb_1.mean(), color="royalblue", linestyle="--", lw=2)
    ax.axhline(1.0, color="black", linestyle="--", lw=1)

    ax.set_xlabel("")
    ax.legend(
        ["6-mo", "12-mo", "6-mo Average"],
        loc=legend_loc,
        frameon=True,
        framealpha=0.5,
    )
    # ax.set_ylim((-0.5, 1.5))
    return ax

def plot_rolling_alpha(returns, factor_returns, legend_loc="best", ax=None, **kwargs):
    """
    Plots the rolling 6-month and 12-month beta versus date.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series
        Daily noncumulative returns of the benchmark factor to which betas are
        computed. Usually a benchmark such as market returns.
         - This is in the same style as returns.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    ax.set_title("Rolling portfolio Alpha to Factor")
    ax.set_ylabel("Alpha")
    rb_1 = rolling_alpha(
        returns, factor_returns, rolling_window=APPROX_BDAYS_PER_MONTH * 6
    )
    rb_1.plot(color="royalblue", lw=2, alpha=0.6, ax=ax, **kwargs)
    rb_2 = rolling_alpha(
        returns, factor_returns, rolling_window=APPROX_BDAYS_PER_MONTH * 12
    )
    rb_2.plot(color="grey", lw=2, alpha=0.4, ax=ax, **kwargs)
    ax.axhline(rb_1.mean(), color="royalblue", linestyle="--", lw=2)
    ax.axhline(1.0, color="black", linestyle="--", lw=1)

    ax.set_xlabel("")
    ax.legend(
        ["6-mo", "12-mo", "6-mo Average"],
        loc=legend_loc,
        frameon=True,
        framealpha=0.5,
    )
    # ax.set_ylim((-0.5, 1.5))

    return ax

def plot_rolling_sharpe(
    returns,
    factor_returns=None,
    rolling_window=APPROX_BDAYS_PER_MONTH * 6,
    legend_loc="best",
    ax=None,
    **kwargs,
):
    """
    Plots the rolling Sharpe ratio versus date.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series, optional
        Daily noncumulative returns of the benchmark factor for
        which the benchmark rolling Sharpe is computed. Usually
        a benchmark such as market returns.
         - This is in the same style as returns.
    rolling_window : int, optional
        The days window over which to compute the sharpe ratio.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    rolling_sharpe_ts = rolling_sharpe(returns, rolling_window)
    rolling_sharpe_ts.plot(alpha=0.7, lw=2, color="royalblue", ax=ax, **kwargs)

    if factor_returns is not None:
        rolling_sharpe_ts_factor = rolling_sharpe(
            factor_returns, rolling_window
        )
        rolling_sharpe_ts_factor.plot(alpha=0.7, lw=2, color="grey", ax=ax, **kwargs)

    ax.set_title("Sharpe ratio corr:" + str(round(rolling_sharpe_ts.corr(rolling_sharpe_ts_factor),2)))
    ax.axhline(rolling_sharpe_ts.mean(), color="orangered", linestyle="--", lw=2)
    ax.axhline(0.0, color="black", linestyle="--", lw=1, zorder=2)

    ax.set_ylabel("Rolling Sharpe Ratio 6-mo vs Factor")
    ax.set_xlabel("")
    if factor_returns is None:
        ax.legend(["Sharpe", "Average"], loc=legend_loc, frameon=True, framealpha=0.5)
    else:
        ax.legend(
            ["Sharpe", "Benchmark Sharpe", "Average"],
            loc=legend_loc,
            frameon=True,
            framealpha=0.5,
        )

    return ax

def plot_rolling_var(
    returns,
    factor_returns=None,
    rolling_window=APPROX_BDAYS_PER_MONTH * 6,
    legend_loc="best",
    ax=None,
    **kwargs,
):
    """
    Plots the rolling Sharpe ratio versus date.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series, optional
        Daily noncumulative returns of the benchmark factor for
        which the benchmark rolling Sharpe is computed. Usually
        a benchmark such as market returns.
         - This is in the same style as returns.
    rolling_window : int, optional
        The days window over which to compute the sharpe ratio.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    rolling_sharpe_ts = rolling_var(returns, rolling_window)
    rolling_sharpe_ts.plot(alpha=0.7, lw=2, color="royalblue", ax=ax, **kwargs)

    if factor_returns is not None:
        rolling_sharpe_ts_factor = rolling_var(
            factor_returns, rolling_window
        )
        rolling_sharpe_ts_factor.plot(alpha=0.7, lw=2, color="grey", ax=ax, **kwargs)

    ax.set_title("Rolling VaR ratio corr:" + str(round(rolling_sharpe_ts.corr(rolling_sharpe_ts_factor),2)))
    ax.axhline(rolling_sharpe_ts.mean(), color="orangered", linestyle="--", lw=2)
    ax.axhline(0.0, color="black", linestyle="--", lw=1, zorder=2)

    ax.set_ylabel("Rolling VaR Ratio 6-mo vs Factor")
    ax.set_xlabel("")
    if factor_returns is None:
        ax.legend(["VaR", "Average"], loc=legend_loc, frameon=True, framealpha=0.5)
    else:
        ax.legend(
            ["VaR", "Benchmark VaR", "Average"],
            loc=legend_loc,
            frameon=True,
            framealpha=0.5,
        )

    return ax

def plot_rolling_var_usd(
    returns,
    factor_returns=None,
    rolling_window=APPROX_BDAYS_PER_MONTH * 6,
    legend_loc="best",
    ax=None,
    **kwargs,
):
    """
    Plots the rolling Sharpe ratio versus date.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series, optional
        Daily noncumulative returns of the benchmark factor for
        which the benchmark rolling Sharpe is computed. Usually
        a benchmark such as market returns.
         - This is in the same style as returns.
    rolling_window : int, optional
        The days window over which to compute the sharpe ratio.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()

    y_axis_formatter = FuncFormatter(two_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    rolling_sharpe_ts = var_usd(returns.rolling(rolling_window))
    rolling_sharpe_ts = pd.DataFrame(rolling_sharpe_ts).dropna()
    rolling_sharpe_ts.plot(alpha=0.7, lw=2, color="royalblue", ax=ax, **kwargs)

    if factor_returns is not None:
        rolling_sharpe_ts_factor = var_usd(factor_returns.rolling(rolling_window))
        rolling_sharpe_ts_factor = pd.DataFrame(rolling_sharpe_ts_factor).dropna()
        rolling_sharpe_ts_factor.plot(alpha=0.7, lw=2, color="grey", ax=ax, **kwargs)

    ax.set_title("VaR ratio en USD")
    ax.axhline(rolling_sharpe_ts.mean()[0], color="orangered", linestyle="--", lw=2)
    ax.axhline(0.0, color="black", linestyle="--", lw=1, zorder=2)

    ax.set_ylabel("Rolling VaR Ratio 6-mo vs Factor")
    ax.set_xlabel("")
    if factor_returns is None:
        ax.legend(["VaR", "Average"], loc=legend_loc, frameon=True, framealpha=0.5)
    else:
        ax.legend(
            ["VaR", "Benchmark VaR", "Average"],
            loc=legend_loc,
            frameon=True,
            framealpha=0.5,
        )

    return ax

def plot_montecarlo(
    montecarlo,
    ax=None,
    marca_blanca=False,
    **kwargs,
):
    """
    Plotea los retornos acumulados rolantes contra un factor(benchmark)
    Los resultados del modelo dentro de muestra, salen en verde, los periodos fuera de muestra, en rojo.
    Ademas de unas bandas no parametricas de expectativas, añadidas a la zona fuera de muestra.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series, optional
        Daily noncumulative returns of the benchmark factor to which betas are
        computed. Usually a benchmark such as market returns.
         - This is in the same style as returns.
    live_start_date : datetime, optional
        The date when the strategy began live trading, after
        its backtest period. This date should be normalized.
    logy : bool, optional
        Whether to log-scale the y-axis.
    cone_std : float, or tuple, optional
        If float, The standard deviation to use for the cone plots.
        If tuple, Tuple of standard deviation values to use for the cone plots
         - See forecast_cone_bounds for more details.
    legend_loc : matplotlib.loc, optional
        The location of the legend on the plot.
    volatility_match : bool, optional
        Whether to normalize the volatility of the returns to those of the
        benchmark returns. This helps compare strategies with different
        volatilities. Requires passing of benchmark_rets.
    cone_function : function, optional
        Function to use when generating forecast probability cone.
        The function signiture must follow the form:
        def cone(in_sample_returns (pd.Series),
                 days_to_project_forward (int),
                 cone_std= (float, or tuple),
                 starting_value= (int, or float))
        See forecast_cone_bootstrap for an example.
    ax : matplotlib.Axes, optional
        Axes upon which to plot.
    **kwargs, optional
        Passed to plotting function.
    Returns
    -------
    ax : matplotlib.Axes
        The axes that were plotted on.
    """

    if ax is None:
        ax = plt.gca()
    sns.set(font='Bloomberg')
    ax.set_xlabel("")
    ax.set_ylabel("MONTECARLO ANALISIS",font='Bloomberg')
    ax.set_yscale("linear")

    montecarlo.plot(alpha=0.7, lw=2, ax=ax,legend=False, **kwargs)
    y_axis_formatter = FuncFormatter(two_dec_places)
    ax.axhline(0.0, linestyle="--",lw=1)

    font_files = font_manager.findSystemFonts(fontpaths=os.getcwd())
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    if marca_blanca==False:
        ax.annotate('QA',#0.85 .20
                    xy=(0.85, .25), xycoords='figure fraction',
                    horizontalalignment='right', verticalalignment='top',
                    fontsize=45, color='blue',
                    fontname='Source Code Pro',
                    weight='bold',
                    alpha=0.4)
    ax.set_title("Retornos Acumulados en (%)")

    return ax

def plot_stats(stats,dark, ax=None,**kwargs):
    font_files = font_manager.findSystemFonts(fontpaths=os.getcwd())
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
    sns.set(font='bloomberg')

    if ax is None:
        fig, ax = plt.subplots(figsize=(0.7,0.7))

    if dark == False:
        color1 = 'black'
        color2 = 'grey'
        color3 = 'black'
    else:
        color1 = '#fb8b1e'
        color2 = '#0068ff'
        color3 = '#000000'

    rows = len(stats)
    use_r = rows +1
    cols = 2   
    if ax is None:
        fig, ax = plt.subplots(figsize=(3.25,18))
    ax.set_ylim(-1, rows + 1)
    ax.set_xlim(0, cols + .5)
    data = []
    for i, row in stats.iterrows():
        data.append({'name': i, 'value': row.values[0]})
        ax.text(-1, 55, 'Ratio', weight='bold', ha='left',color=color3)
        ax.text(1.15, 55, 'Value', weight='bold', ha='right', color=color3)
    for row in range(rows):
        d = data[row]
        ax.text(x=-1, y=row+(0.2*row), s=d['name'], va='center', ha='left',color=color1)
        ax.text(x=1.20, y=row+(0.2*row), s=d['value'], va='center', ha='right', weight='bold',color=color2)
    ax.axis('off')
    return ax

def plot_drawdown_tops(df, dark, ax=None, **kwargs):
    dds = show_worst_drawdown_periods(df, top=5, by='pct')
    dds2 = show_worst_drawdown_periods(df, top=5, by='days')

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))  # Tamaño ajustado para mayor espacio

    if dark:
        color1 = '#ff433d'
        color2 = 'white'
        color3 = '#fb8b1e'
    else:
        color1 = 'black'
        color2 = 'black'
        color3 = 'black'

    ax.set_ylim(4.5, 10)
    ax.set_xlim(0.5, 7.5)  # Ajustar límites para mayor espacio horizontal

    # Datos para el primer bloque (Top 5 por MaxDD)
    data = []
    for i, row in dds.iterrows():
        data.append({
            'Net DD in %': row['Net drawdown in %'],
            'Duration': row['Duration'],
            'Peak date': row['Peak date'],
            'Valley date': row['Valley date'],
            'Recovery Date': row['Recovery date']
        })

    # Títulos del primer bloque
    ax.text(0.5, 10.5, 'Top 5 DD by MaxDD', weight='bold', ha='left', color=color1, fontsize=12)
    ax.text(0.5, 9.75, 'DD in %', weight='bold', ha='left', color=color2, fontsize=10)
    ax.text(1.75, 9.75, 'Duration', weight='bold', ha='left', color=color2, fontsize=10)
    ax.text(3.15, 9.75, 'Peak Date', weight='bold', ha='left', color=color2, fontsize=10)
    ax.text(4.9, 9.75, 'Valley Date', weight='bold', ha='left', color=color2, fontsize=10)
    ax.text(6.75, 9.75, 'Recovery Date', weight='bold', ha='left', color=color2, fontsize=10)

    # Datos del primer bloque
    for row in range(len(dds)):
        d = data[row]
        ax.text(x=0.5, y=9.5 - (0.4 * row), s=round(d['Net DD in %'], 2), va='center', ha='left', color=color3, fontsize=9)
        ax.text(x=1.75, y=9.5 - (0.4 * row), s=round(d['Duration'], 2), va='center', ha='left', color=color3, fontsize=9)
        ax.text(x=3.15, y=9.5 - (0.4 * row), s=d['Peak date'].date(), va='center', ha='left', color=color3, fontsize=9)
        ax.text(x=4.9, y=9.5 - (0.4 * row), s=d['Valley date'].date(), va='center', ha='left', color=color3, fontsize=9)
        ax.text(x=6.75, y=9.5 - (0.4 * row), s=d['Recovery Date'].date(), va='center', ha='left', color=color3, fontsize=9)

    # Datos para el segundo bloque (Top 5 por días)
    data2 = []
    for i, row in dds2.iterrows():
        data2.append({
            'Net DD in %': row['Net drawdown in %'],
            'Duration': row['Duration'],
            'Peak date': row['Peak date'],
            'Valley date': row['Valley date'],
            'Recovery Date': row['Recovery date']
        })

    # Títulos del segundo bloque
    ax.text(0.5, 7.25, 'Top 5 DD by Days', weight='bold', ha='left', color=color1, fontsize=12)
    ax.text(0.5, 6.75, 'DD in %', weight='bold', ha='left', color=color2, fontsize=10)
    ax.text(1.75, 6.75, 'Duration', weight='bold', ha='left', color=color2, fontsize=10)
    ax.text(3.15, 6.75, 'Peak Date', weight='bold', ha='left', color=color2, fontsize=10)
    ax.text(4.9, 6.75, 'Valley Date', weight='bold', ha='left', color=color2, fontsize=10)
    ax.text(6.75, 6.75, 'Recovery Date', weight='bold', ha='left', color=color2, fontsize=10)

    # Datos del segundo bloque
    for row in range(len(dds2)):
        d = data2[row]
        ax.text(x=0.5, y=6.5 - (0.4 * row), s=round(d['Net DD in %'], 2), va='center', ha='left', color=color3, fontsize=9)
        ax.text(x=1.75, y=6.5 - (0.4 * row), s=round(d['Duration'], 2), va='center', ha='left', color=color3, fontsize=9)
        ax.text(x=3.15, y=6.5 - (0.4 * row), s=d['Peak date'].date(), va='center', ha='left', color=color3, fontsize=9)
        ax.text(x=4.9, y=6.5 - (0.4 * row), s=d['Valley date'].date(), va='center', ha='left', color=color3, fontsize=9)
        ax.text(x=6.75, y=6.5 - (0.4 * row), s=d['Recovery Date'].date(), va='center', ha='left', color=color3, fontsize=9)

    ax.axis('off')  # Ocultar los ejes
    return ax

def plot_drawdown_tops(df,dark, ax=None, **kwargs):
    dds = show_worst_drawdown_periods(df,top=5,by='pct')
    dds2 = show_worst_drawdown_periods(df,top=5,by='days')

    if ax is None:
        fig, ax = plt.subplots(figsize=(0.7,0.7))

    if dark == True:
        color1 = '#ff433d'
        color2 = 'white'
        color3 = '#fb8b1e'
    else:
        color1 = 'black'
        color2 = 'black'
        color3 = 'black'

    ax.set_ylim(4.5,10)
    ax.set_xlim(1, 9)
    data = [] 
    for i, row in dds.iterrows():
        data.append({'Net DD in %': row['Net drawdown in %'], 'Duration':row['Duration'],'Peak date':row['Peak date'],'Valley date':row['Valley date'],'Recovery Date':row['Recovery date']})
    ax.text(0.5,10.5, 'Top 5 DD by MaxDD',weight='bold', ha='left',color=color1)
    ax.text(0.5 ,9.75, 'DD in %', weight='bold', ha='left',color=color2)
    ax.text(1.75 ,9.75, 'Duration', weight='bold', ha='left',color=color2)
    ax.text( 3.15,9.75, 'Peak Date', weight='bold', ha='left',color=color2)
    ax.text(4.9 ,9.75, 'Valley Date', weight='bold', ha='left',color=color2)
    ax.text(6.75 ,9.75, 'Recovery Date', weight='bold', ha='left',color=color2)
    for row in range(len(dds)):
        d = data[row]
        ax.text(x=0.5, y=9.5 - (0.4 * row) , s=round(d['Net DD in %'],2), va='center', ha='left',color=color3)
        ax.text(x=1.75, y=9.5 - (0.4 * row) , s=round(d['Duration'],2), va='center', ha='left',color=color3)
        ax.text(x=3.15, y=9.5 - (0.4 * row) , s=d['Peak date'].date(), va='center', ha='left',color=color3)
        ax.text(x=4.9, y=9.5 - (0.4 * row) , s=d['Valley date'].date(), va='center', ha='left',color=color3)
        ax.text(x=6.75, y=9.5 - (0.4 * row) , s=d['Recovery Date'].date(), va='center', ha='left',color=color3)

    data2 = []

    for i, row in dds2.iterrows():
        data2.append({'Net DD in %': row['Net drawdown in %'], 'Duration':row['Duration'],'Peak date':row['Peak date'],'Valley date':row['Valley date'],'Recovery Date':row['Recovery date']})
    ax.text(0.5,7.25, 'Top 5 DD by days',weight='bold', ha='left',color=color1)
    ax.text(0.5 ,6.75, 'DD in %', weight='bold', ha='left',color=color2)
    ax.text(1.75 ,6.75, 'Duration', weight='bold', ha='left',color=color2)
    ax.text(3.15 ,6.75, 'Peak Date', weight='bold', ha='left',color=color2)
    ax.text(4.9 ,6.75, 'Valley Date', weight='bold', ha='left', color=color2)
    ax.text(6.75 ,6.75, 'Recovery Date', weight='bold', ha='left' ,color=color2) 
    for row in range(len(dds2)):
        d = data2[row]
        ax.text(x=0.5,  y=6.5 - (0.4*row), s=round(d['Net DD in %'],2), va='center', ha='left',color=color3)
        ax.text(x=1.75, y=6.5 - (0.4 * row)  , s=round(d['Duration'],2), va='center', ha='left',color=color3)
        ax.text(x=3.15, y=6.5 - (0.4 * row), s=d['Peak date'].date(), va='center', ha='left',color=color3)
        ax.text(x=4.9,  y=6.5 - (0.4 * row), s=d['Valley date'].date(), va='center', ha='left',color=color3)
        ax.text(x=6.75, y=6.5 - (0.4 * row), s=d['Recovery Date'].date(), va='center', ha='left',color=color3)
    ax.axis('off')
    return ax

def plot_stress_events(returns,dark,ax=None,**kwargs):
    if ax is None:
        fig, ax = plt.subplots(figsize=(0.7,0.7))

    if dark == True:
        color1 = '#ff433d'
        color2 = 'white'
        color3 = '#fb8b1e'
    else:
        color1 = 'black'
        color2 = 'black'
        color3 = 'black'

    font_files = font_manager.findSystemFonts(fontpaths=os.getcwd())
   
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
    sns.set(font='bloomberg')

    dds=get_drawdown_stats(returns,display=False)
    dds = dds.reindex(index=dds.index[::-1])
    ax.set_ylim(2,10)
    ax.set_xlim(1, 10)
    dds = round(dds,3)
    ax.axis('on')
    
    data = []
    
    for i, row in dds.iterrows():
        data.append({'E': row.name,'N':row['N'],'Std':row['Std'],'X':row['X'],'min':row['min'],'max':row['max']})
    
    ax.text(0.5 ,10.25, 'Evento', weight='bold', ha='left',size=13,color=color2)
    ax.text(2.5 ,10.25, 'Periodo', weight='bold', ha='left',size=13,color=color2)
    ax.text(4 ,10.25, 'Volatilidad', weight='bold', ha='left',size=13,color=color2)
    ax.text(6 ,10.25, 'Ret Medio', weight='bold', ha='left',size=13,color=color2)
    ax.text(7.9 ,10.25, 'Minimo', weight='bold', ha='left',size=13,color=color2)
    ax.text(9.5,10.25, 'Maximo', weight='bold', ha='left',size=13,color=color2)
    
    for row in range(len(dds)):
        d = data[row]
        ax.text(x=0.5,  y=9.75 - (row * 0.6), s=d['E'][0:20], va='center', ha='left',color='black')
        ax.text(x=2.5,y=9.75 - (row * 0.6), s=d['N'], va='center', ha='left',color='black')
        ax.text(x=4,  y=9.75 - (row * 0.6), s=d['Std'], va='center', ha='left',color='black')
        ax.text(x=6,  y=9.75 - (row * 0.6), s=d['X'], va='center', ha='left',color='black')
        ax.text(x=7.9,y=9.75 - (row * 0.6), s=d['min'], va='center', ha='left',color='black')
        ax.text(x=9.5,y=9.75 - (row * 0.6), s=d['max'], va='center', ha='left',color='black')
    ax.axis('off')
    
    return ax

def plot_montecarlo_odds(result, dd_result, ax=None, **kwargs):
    all_data = mc_perf_probs(result,dd_result).reset_index()
    print(all_data)
    if ax is None:
        fig, ax = plt.subplots(figsize=(3,3))

    ax.set_ylim(6,10)
    ax.set_xlim(1, 3)
    data = [] 

    for i, row in all_data.iterrows():
       data.append({'Odds': row['index'], 'Performance':row['Performance'],'Max Drawdown':row['Max Drawdown']})
    ax.text(0.5,10, 'Montecarlo Analisis',weight='bold', ha='left',color='darkred')
    ax.text(0.5 ,9.75, 'Odds', weight='bold', ha='left')
    ax.text(1.35 ,9.75, 'Ret', weight='bold', ha='left')
    ax.text(2.25 ,9.75, 'MDD', weight='bold', ha='left')
    for row in range(len(all_data)):
        d = data[row]
        ax.text(x=0.5, y=9.5 - (0.4 * row) , s=d['Odds'], va='center', ha='left',color='black')
        ax.text(x=1.35, y=9.5 - (0.4 * row) , s=d['Performance'], va='center', ha='left',color='black')
        ax.text(x=2.25, y=9.5 - (0.4 * row) , s=d['Max Drawdown'], va='center', ha='left',color='black')

    ax.axis('off')

    return ax

def plot_montecarlo_graph(result, ax=None, **kwargs):
    if not ax:
        fig, ax = plt.subplots(figsize=(6,6))
    
    sns.lineplot(data=result, palette="mako",legend=False)

    return ax 
