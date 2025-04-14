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
import datetime
import datetime
import ffn 

def run_monte_carlo_parametric(returns,trading_days,simulations):    
    df_list = []
    result = []
    S = 100
    T = trading_days
    mu = returns.mean()
    vol = returns.std()
    dd_result = []
    for i in range(simulations):
        daily_returns=np.random.normal(mu,vol,T)+1
        price_list = [S]
        for x in daily_returns:
            price_list.append(price_list[-1]*x)
        df = pd.DataFrame(price_list)
        max_dd = ffn.calc_max_drawdown(df)
        dd_result.append(max_dd)
        df_list.append(df)
        result.append(price_list[-1])
    df_master = pd.concat(df_list,axis=1)
    df_master.columns = range(len(df_master.columns)) 
    return df_master,result,dd_result

def extract_best_worst(monte_carlo_results,trading_days):
    today =  datetime.datetime.today().strftime('%d/%m/%Y')
    date_range = pd.bdate_range(end=today, periods=trading_days+1, freq='B')
    monte_carlo_results.columns = range(len(monte_carlo_results.columns))
    last_row = monte_carlo_results.iloc[-1]
    max_col = last_row.idxmax()
    best_df = monte_carlo_results[max_col]
    min_col = last_row.idxmin()
    worst_df = monte_carlo_results[min_col]
    best_df = best_df.to_frame()
    worst_df = worst_df.to_frame()
    best_df = best_df.set_index(date_range)
    worst_df = worst_df.set_index(date_range)
    mc_best_worst_df = pd.concat([best_df,worst_df],axis=1)
    mc_best_worst_df.columns = ['Best','Worst']    
    return mc_best_worst_df

def calc_mc_var(monte_carlo_results,confidence): 
    mc_as_array = np.array(monte_carlo_results)
    mc_low_perc = round(((np.percentile(mc_as_array, 100-confidence) /100) - 1) * 100,2)
    mc_high_perc = round(((np.percentile(mc_as_array, confidence) /100) - 1) * 100,2)
    return mc_low_perc,mc_high_perc

def mc_perf_probs(monte_carlo_results,mc_max_dd_list):    
    mc_as_array = np.array(monte_carlo_results)
    mc_5perc = round(((np.percentile(mc_as_array, 5) /100) - 1) * 100,2)
    mc_95perc = round(((np.percentile(mc_as_array, 95) /100) - 1) * 100,2)
    mc_1perc = round(((np.percentile(mc_as_array, 1) /100) - 1) * 100,2)
    mc_10perc = round(((np.percentile(mc_as_array, 10) /100) - 1) * 100,2)
    mc_20perc = round(((np.percentile(mc_as_array, 20) /100) - 1) * 100,2)
    mc_30perc = round(((np.percentile(mc_as_array, 30) /100) - 1) * 100,2)
    mc_40perc = round(((np.percentile(mc_as_array, 40) /100) - 1) * 100,2)
    mc_50perc = round(((np.percentile(mc_as_array, 50) /100) - 1) * 100,2)
    mc_60perc = round(((np.percentile(mc_as_array, 60) /100) - 1) * 100,2)
    mc_70perc = round(((np.percentile(mc_as_array, 70) /100) - 1) * 100,2)
    mc_80perc = round(((np.percentile(mc_as_array, 80) /100) - 1) * 100,2)
    mc_90perc = round(((np.percentile(mc_as_array, 90) /100) - 1) * 100,2)
    mc_99perc = round(((np.percentile(mc_as_array, 99) /100) - 1) * 100,2)
    mc_as_array_dd = np.array(mc_max_dd_list)
    mc_5perc_dd = round((np.percentile(mc_as_array_dd, 5)) * 100,2)
    mc_95perc_dd = round((np.percentile(mc_as_array_dd, 95)) * 100,2)
    mc_1perc_dd = round((np.percentile(mc_as_array_dd, 1)) * 100,2)
    mc_10perc_dd = round((np.percentile(mc_as_array_dd, 10)) * 100,2)
    mc_20perc_dd = round((np.percentile(mc_as_array_dd, 20)) * 100,2)
    mc_30perc_dd = round((np.percentile(mc_as_array_dd, 30)) * 100,2)
    mc_40perc_dd = round((np.percentile(mc_as_array_dd, 40)) * 100,2)
    mc_50perc_dd = round((np.percentile(mc_as_array_dd, 50)) * 100,2)
    mc_60perc_dd = round((np.percentile(mc_as_array_dd, 60)) * 100,2)
    mc_70perc_dd = round((np.percentile(mc_as_array_dd, 70)) * 100,2)
    mc_80perc_dd = round((np.percentile(mc_as_array_dd, 80)) * 100,2)
    mc_90perc_dd = round((np.percentile(mc_as_array_dd, 90)) * 100,2)
    mc_99perc_dd = round((np.percentile(mc_as_array_dd, 99)) * 100,2)
        
    mc_dict_perf = {
            '1%':[mc_1perc,mc_1perc_dd],
            '5%':[mc_5perc,mc_5perc_dd],
            '20%':[mc_20perc,mc_20perc_dd],
            '30%':[mc_30perc,mc_30perc_dd],
            '40%':[mc_40perc,mc_40perc_dd],
            '50%':[mc_50perc,mc_50perc_dd],
            '60%':[mc_60perc,mc_60perc_dd],
            '70%':[mc_70perc,mc_70perc_dd],
            '80%':[mc_80perc,mc_80perc_dd],
            '90%':[mc_90perc,mc_90perc_dd],
            '95%':[mc_95perc,mc_95perc_dd],
            '99%':[mc_99perc,mc_99perc_dd],
            }    
    max_min = pd.DataFrame.from_dict(mc_dict_perf, orient='index', columns=['Performance','Max Drawdown'])

    return max_min   
