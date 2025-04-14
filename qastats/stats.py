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
import numpy as np
import quantstats as qs
import empyrical as qa
from .interesting_periods import PERIODS
from scipy.stats import norm
from IPython.display import display_html 
qs.extend_pandas()

def calculate_sqn(returns):
    """
    Calcula el System Quality Number (SQN) para una serie de retornos.

    Parameters
    ----------
    returns : pd.Series
        Serie de retornos diarios no acumulados.

    Returns
    -------
    sqn : float
        El valor del SQN calculado.
    """
    if len(returns) == 0:
        raise ValueError("La serie de retornos está vacía.")

    mean_returns = returns.mean()
    std_returns = returns.std()
    n = len(returns)

    if std_returns == 0:
        raise ValueError("La desviación estándar de los retornos es cero, no se puede calcular el SQN.")

    sqn = (mean_returns / std_returns) * (n ** 0.5)
    return sqn

def calculate_omega_ratio(returns, threshold=0):
    """
    Calcula el Omega Ratio para una serie de retornos.

    Parameters
    ----------
    returns : pd.Series
        Serie de retornos diarios no acumulados.
    threshold : float, optional
        Umbral de retorno (por defecto 0).

    Returns
    -------
    omega_ratio : float
        El Omega Ratio calculado.
    """
    if len(returns) == 0:
        raise ValueError("La serie de retornos está vacía.")

    # Retornos por encima y por debajo del umbral
    excess_returns = returns - threshold
    gains = excess_returns[excess_returns > 0].sum()
    losses = -excess_returns[excess_returns < 0].sum()

    if losses == 0:
        return np.inf  # Si no hay pérdidas, el Omega Ratio es infinito

    omega_ratio = gains / losses
    return omega_ratio

def get_daily_stats(data):
    """
    Obtiene todas las estadisticas relevantes. En timeframe diario,y devuelve un dataframe con las soluciones, y lo displayea en pantalla.

    Parameters
    ----------
    data : pd.Series
        Retornos diarios no acumulados de la serie a analizar.
    display : pd.Bool
        Muestra el resultado en pantalla o no

    Como debe llegar data
    ---------------------
    Debe ser un dataframe con la siguiente forma:
    Indice -> Fechas
    Col0 = 'Close' -> Donde traeran los retornos diarios no acumulados
    Col1 = 'bench' -> Donde traeran los retornos diarios no acumulados del factor de comparacion.

    Returns
    -------
    stats : pd.DataFrame()
        El dataframe con toda la informacion calculada.
    """
    v = {
        'AuM':'000.000.000$',
        'Start': data['Close'].index.strftime('%Y-%m-%d')[0],
        'End':data['Close'].index.strftime('%Y-%m-%d')[-1],
        'Period':len(data['Close']),
        'Total Return': qa.stats.cum_returns_final(data['Close'],100),
        'Factor Return':qa.stats.cum_returns_final(data['bench'],100),
        'Ret Corr with Factor':data['Close'].corr(data['bench'],method='kendall'),
        'Ret Corr with Factor + ':data[data['Close']>0].corr(method='kendall')['Close']['bench'],
        'Ret Corr with Factor -' :data[data['Close']<0].corr(method='kendall')['Close']['bench'],
        'CAGR':100 * data['Close'].cagr(),
        'Annualized Vol': 100 * qs.stats.volatility(data['Close']),
        'Max DD':round(data.max_drawdown() * 100 ,2),
        'Calmar Ratio': data.calmar()[0],
        'Sortino Ratio':qs.stats.sortino(data['Close']),
        'SQN': calculate_sqn(returns=data['Close']),
        'Omega Ratio':calculate_omega_ratio(returns=data['Close']),
        'Skew':data['Close'].skew(),
        'Kurt':data['Close'].kurt(),
        'VaR':round(data.value_at_risk()[0] * 100,2),
        'CVaR':qa.conditional_value_at_risk(data['Close']) * 100,
        'Stability':qa.stability_of_timeseries(data['Close']),
        'Riesgo Cola':qa.tail_ratio(data['Close']),
        'WinRate':qs.stats.win_rate(data['Close']),
        'Avg ret':qs.stats.avg_return(data['Close'])*100,
        'Best Day ':data['Close'].max()*100,
        'Worst Day ':data['Close'].min()*100,
        'Avg Good Day':qs.stats.avg_win(data['Close']*100),
        'Avg Bad Day':qs.stats.avg_loss(data['Close']*100),
        'Max consecutive wins': qs.stats.consecutive_wins(data['Close']),
        'Max consecutive losses':qs.stats.consecutive_losses(data['Close']),
        'Outlier win ratio':qs.stats.outlier_win_ratio(data['Close'], prepare_returns=False),
        'Outlier loose ratio':qs.stats.outlier_loss_ratio(data['Close'], prepare_returns=False),
        'Profit Factor':qs.stats.profit_factor(data['Close'], prepare_returns=False),
        'CPC Idx':qs.stats.cpc_index(data['Close']),
        'Expectancy': 100 * data['Close'].expected_return(),
        'Alpha':qa.alpha_beta(data['Close'],data['bench'],annualization=252)[0],
        'Alpha con Modelo +':qa.up_alpha_beta(data['Close'],data['bench'],annualization=252)[1],
        'Alpha con Moldelo -':qa.down_alpha_beta(data['Close'],data['bench'],annualization=252)[0],
        'Beta':qa.alpha_beta(data['Close'],data['bench'],annualization=252)[1],
        'Beta con Modelo +':qa.up_alpha_beta(data['Close'],data['bench'],annualization=252)[0],
        'Beta con Modelo -':qa.down_alpha_beta(data['Close'],data['bench'],annualization=252)[1],
        'Beta Fragility':qa.batting_average(data['Close'], data['bench'])[0],
        'Capture con Modelo +':qa.up_capture(data['Close'], data['bench']),
        'Capture con Modelo -':qa.down_capture(data['Close'], data['bench']),
        'QA Alpha Capture':qa.up_down_capture(data['Close'], data['bench'])
    }
    def round_dict(d):
        return {k: (round(v, 2) if isinstance(v, float) else v[:] if isinstance(v, str) else v) for k, v in d.items()}

    v_r = round_dict(v)
    stats = pd.DataFrame(v_r).T
    
    return stats[['Close']]

def get_montly_stats(data,display=True):
    """
    Obtiene todas las estadisticas relevantes. En timeframe Mensual,y devuelve un dataframe con las soluciones, y lo displayea en pantalla.

    Parameters
    ----------
    data : pd.Series
        Retornos diarios no acumulados de la serie a analizar.
    display : pd.Bool
        Muestra el resultado en pantalla o no

    Como debe llegar data
    ---------------------
    Debe ser un dataframe con la siguiente forma:
    Indice -> Fechas
    Col0 = 'Close' -> Donde traeran los retornos diarios no acumulados
    Col1 = 'bench' -> Donde traeran los retornos diarios no acumulados del factor de comparacion.

    Returns
    -------
    stats : pd.DataFrame()
        El dataframe con toda la informacion calculada.
    """


    v = {
        'AuM':'000.000.000$',
        'Start': data['Close'].index.strftime('%Y-%m-%d')[0],
        'End':data['Close'].index.strftime('%Y-%m-%d')[-1],
        'Period':len(data['Close']),
        'Total Return': data['Close'].cumsum()[-1],
        'Factor Return':data['bench'].cumsum()[-1],
        'Ret Corr with Factor':data['Close'].corr(data['bench'],method='kendall'),
        'Ret Corr with Factor + ':'COOMING',
        'Ret Corr with Factor -':'COOMING',
        'CAGR':data.cagr()[0],
        'Annualized Vol': qs.stats.volatility(data['Close']),
        'Max DD':data.max_drawdown()[0],
        'Sharpe Ratio':data.sharpe(periods=12)[0],
        'Calmar Ratio': data.calmar()[0],
        'Sortino Ratio':qs.stats.sortino(data['Close'],periods=12),
        'Omega Ratio':calculate_omega_ratio(returns=data['Close']),
        'Skew':data['Close'].skew(),
        'Kurt':data['Close'].kurt(),
        'VaR':data.value_at_risk()[0],
        'CVaR':qa.conditional_value_at_risk(data['Close']),
        'Stability':qa.stability_of_timeseries(data['Close']),
        'Riesgo Cola':qa.tail_ratio(data['Close']),
        'WinRate':qs.stats.win_rate(data['Close']),
        'Avg ret':qs.stats.avg_return(data['Close']),
        'Best Day ':data['Close'].max(),
        'Worst Day ':data['Close'].min(),
        'Avg Good Day':qs.stats.avg_win(data['Close']),
        'Avg Bad Day':qs.stats.avg_loss(data['Close']),
        'Max consecutive wins': qs.stats.consecutive_wins(data['Close']),
        'Max consecutive losses':qs.stats.consecutive_losses(data['Close']),
        'Outlier win ratio':qs.stats.outlier_win_ratio(data['Close'], prepare_returns=False),
        'Outlier loose ratio':qs.stats.outlier_loss_ratio(data['Close'], prepare_returns=False),
        'Profit Factor':qs.stats.profit_factor(data['Close'], prepare_returns=False),
        'CPC Idx':qs.stats.cpc_index(data['Close']),
        'Expectancy': qs.stats.expected_return(data['Close']),
        'alpha':qa.alpha_beta(data['Close'],data['bench'],annualization=12)[0],
        'alpha_alcista':qa.up_alpha_beta(data['Close'],data['bench'],annualization=12)[1],
        'alpha_bajista':qa.down_alpha_beta(data['Close'],data['bench'],annualization=12)[0],
        'beta':qa.alpha_beta(data['Close'],data['bench'],annualization=12)[1],
        'beta_alcista':qa.up_alpha_beta(data['Close'],data['bench'],annualization=12)[0],
        'beta_bajista':qa.down_alpha_beta(data['Close'],data['bench'],annualization=12)[1],
        'beta fragility':qa.batting_average(data['Close'], data['bench'])[0],
        'Capture UP':qa.up_capture(data['Close'], data['bench']),
        'Capture DW':qa.down_capture(data['Close'], data['bench']),
        'QA_AlphaCapture':qa.up_down_capture(data['Close'], data['bench']) * 100
    }

    stats = pd.DataFrame(v,index=['Value']).T
    return stats 

def get_drawdown_stats(returns,ax=None, **kwargs):
    from .timeseries import extract_interesting_date_ranges  # Local import
    rets_interesting = extract_interesting_date_ranges(returns)
    ret = pd.DataFrame(rets_interesting).describe().transpose().loc[:, ["count","std","mean", "min", "max"]] * 100
    ret.columns = ['N','Std','X','min','max']
    ret['N'] = ret['N']/100
    return ret

def get_vami_diario(pct):
    """
    Value Added Monthly Index (VAMI) 
    ---------------------------------
    Calcula el ratio VAMI sobre la serie de retornos no acumulado.

    Where->VAMI on Tsub0 = 1000
    Where->Ret on N = Return for period N
    
    Vami N = ( 1 + R(N) ) / Vami (N)-1

    Parameters
    ----------
    data : pd.Series
        Retornos diarios no acumulados de la serie a analizar.
    Como debe llegar data
    ---------------------
    Debe ser un dataframe con la siguiente forma:
    Indice -> Fechas
    Col0 = 'Close' -> Donde traeran los retornos diarios no acumulados
    Col1 = 'bench' -> Donde traeran los retornos diarios no acumulados del factor de comparacion.

    Returns
    -------
    matrix : pd.Series
        Serie con los resultados del ratio VAMI
    """
    pct = pct / 100
    matrix = pd.DataFrame(index=pct.index,columns=['VAMI'])
    matrix['VAMI'][0] = 1000
        
    for i in range(1,len(matrix)):
        matrix['VAMI'][i] = matrix['VAMI'][i - 1] + (matrix['VAMI'][i - 1] * pct[i])
    print('OK')
    return matrix

def show_worst_drawdown_periods(returns, top=5,by='duration',show=False):
    """
    Prints information about the worst drawdown periods.
    Prints peak dates, valley dates, recovery dates, and net
    drawdowns.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    top : int, optional
        Amount of top drawdowns periods to plot (default 5).
    """
    from .timeseries import gen_drawdown_table as gdd
    drawdown_df = gdd(returns, top=top)
    if by=='pct':
        if show==True:
            utils.print_table(
                drawdown_df.sort_values("Net drawdown in %", ascending=False),
                name="Worst drawdown periods in %",
                float_format="{0:.2f}".format,)
        drawdown_df=drawdown_df.sort_values("Net drawdown in %", ascending=False)
    if by=='days':
        if show==True:
            utils.print_table(
                drawdown_df.sort_values("Duration", ascending=False),
                name="Worst drawdown periods in days",
                float_format="{0:.2f}".format,
            )
        drawdown_df=drawdown_df.sort_values("Duration", ascending=False)

    return drawdown_df

def var_usd(returns, sigma=1, confidence=0.95, prepare_returns=True,capital=1000000):
    """
    Calculats the daily value-at-risk
    (variance-covariance calculation with confidence n)
    """
    mu = returns.mean()
    sigma *= returns.std()

    if confidence > 1:
        confidence = confidence/100

    alpha = norm.ppf(1-confidence, mu, sigma)
    return capital - capital * (alpha +1)

