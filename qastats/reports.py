####
# QUANTARMY 2022 - PRIVATE CODE - ALL RIGTHS RESERVED
# QUANTARMY 2023 - PRIVATE CODE - ALL RIGTHS RESERVED
# QUANTARMY 2024 - GNU PUBLIC LICENSE (ALL SOURCE RELEASED)
# by jcx - jcx@quantarmy.com | https://quantarmy.com
####
# Noviembre 2022
# Enero 2023 - 
# Feb 2024 - Update 2.0
##### armystats v2
#
#### 
#To-Do
# -> Tests

import warnings
from time import time
import empyrical as ep
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from .plots import * 
from .plots import customize as qa_plot
from .randomizer import *
from IPython.display import display, Markdown
from IPython.display import (display as iDisplay, HTML as iHTML)
from .plots import customize as qa_plot
from .stats import *
import pyfolio as ppf
from .interesting_periods import PERIODS

def create_return_dd(data=None,live_start_date=None,dark=False,name=None):
    if dark == True:
        plt.style.use('dark_background')

    iDisplay(iHTML('<h4> [JCX] - QUANTARMY </h4>'))


    if live_start_date is not None:
        live_start_date = ep.utils.get_utc_timestamp(live_start_date)

    fig = plt.figure(figsize=(15, 15 * 7))
    gs = gridspec.GridSpec(18, 6, wspace=0.2, hspace=0.3,)
    ax_logo = plt.subplot(gs[0:1, :])
    ax_rolling_returns = plt.subplot(gs[1:2,2:])
    ax_table= plt.subplot(gs[1:3,0:2])
    ax_dd_underwater = plt.subplot(gs[2:3,2:])
    ax_montly_returns = plt.subplot(gs[3, :])
    ax_yearly_bars = plt.subplot(gs[4,0:3])
    ax_monthly_dist = plt.subplot(gs[4,3:])
    ax_monthly_heatmap = plt.subplot(gs[5,:])
    ax_dds_zonas = plt.subplot(gs[6,:])
    ax_dds_periods = plt.subplot(gs[7,:])
    ax_dds_stress = plt.subplot(gs[8,:])
    ax_rol_vol = plt.subplot(gs[10,:])
    ax_rol_alpha = plt.subplot(gs[11,:])
    ax_rol_beta = plt.subplot(gs[12,:])
    ax_rol_sharpe = plt.subplot(gs[13,:])
    ax_rol_var = plt.subplot(gs[14,:])
    ax_var_usd = plt.subplot(gs[15,:])
    ax_stats_mc= plt.subplot(gs[16,:2])
    ax_plot_mc =  plt.subplot(gs[16,2:])


    stats = get_daily_stats(data)
    stats = stats.reindex(index=stats.index[::-1])
    master, result, dd_result = run_monte_carlo_parametric(data['Close'],300,500)

    plot_ref(ax=ax_logo,dark=dark)
    plot_rolling_returns(data['Close'],factor_returns=data['bench'],live_start_date=live_start_date,ax=ax_rolling_returns,marca_blanca=True)
    plot_stats(stats,dark=dark,ax=ax_table)
    plot_drawdown_underwater(data['Close'], ax=ax_dd_underwater,marca_blanca=True)
    plot_monthly_returns_timeseries(data['Close'], ax=ax_montly_returns)
    plot_monthly_returns_heatmap(data['Close'], ax=ax_monthly_heatmap,marca_blanca=True)
    plot_annual_returns(data['Close'], ax=ax_yearly_bars,marca_blanca=True)
    plot_monthly_returns_dist(data['Close'], ax=ax_monthly_dist, marca_blanca=True)
    plot_drawdown_tops(data['Close'], ax=ax_dds_zonas,dark=dark,marca_blanca=True)
    plot_drawdown_periods(data['Close'], ax=ax_dds_periods,marca_blanca=True)
    plot_stress_events(data['Close'],dark=dark,show=False,ax=ax_dds_stress)
    plot_rolling_volatility(data['Close'], data['bench'], ax=ax_rol_vol,marca_blanca=True)
    plot_rolling_alpha(data['Close'], data['bench'], ax=ax_rol_alpha)
    plot_rolling_beta(data['Close'], data['bench'], ax=ax_rol_beta)
    plot_rolling_sharpe(data['Close'], data['bench'], ax=ax_rol_sharpe)
    plot_rolling_var(data['Close'].mul(100), data['bench'].mul(100), ax=ax_rol_var)
    plot_rolling_var_usd(data['Close'], data['bench'], ax=ax_var_usd)
    plot_montecarlo_odds(result,dd_result,ax=ax_stats_mc)
    plot_montecarlo_graph(master,ax=ax_plot_mc)

    fig.tight_layout()

    if name is None :
        fig.savefig('noname.pdf', bbox_inches='tight', pad_inches=0.1)
        fig.savefig('noname.png', bbox_inches='tight', pad_inches=0.1)
    else:
        fig.savefig(str(name)+'.pdf', bbox_inches='tight', pad_inches=0.1)
    qa_plot(fig)

