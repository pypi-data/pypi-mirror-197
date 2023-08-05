from itertools import product
from time import sleep
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, date
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as smapi


def seasonal_difference(a, period):
    a2 = a.copy()
    a2.iloc[:] = np.nan
    a2.iloc[period:] = np.array(a)[period::] - np.array(a)[:-period:]
    a2 = a2[~pd.isna(a2)].copy()

    return a2


def func1_0_plot_series(t_series, title):
    ''' Have a look at the time series to observe seasonality and heteroscedasticity '''
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(1, 1, 1)
    sns.lineplot(x=t_series.index, y=t_series, linewidth=3, ax=ax)
    ax.set_title(title, fontsize=15, color='grey', loc='left')
    ax.set_xlabel('Day', fontsize=15, color='grey')
    ax.set_ylabel('Value', fontsize=15, color='grey')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', colors='grey')
    ax.tick_params(axis='y', colors='grey')


def func1_0_plot_series_traintest(t_series_train, t_series_test, title):
    ''' Have a look at the time series to observe seasonality and heteroscedasticity '''
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(1, 1, 1)
    sns.lineplot(x=t_series_train.index, y=t_series_train, linewidth=3, ax=ax, color='#2596be', label='Train')
    sns.lineplot(x=t_series_test.index, y=t_series_test, linewidth=3, ax=ax, color='#e28743', label='Test')
    ax.set_title(title, fontsize=15, color='grey', loc='left')
    ax.set_xlabel('Day', fontsize=15, color='grey')
    ax.set_ylabel('Value', fontsize=15, color='grey')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', colors='grey')
    ax.tick_params(axis='y', colors='grey')


def func1_1_plot_acf_pacf(t_series, lags):
    ''' If seasonality is difficult to observe, look at the acf,pacf '''
    # Plot the ACF and PACF
    f = plot_acf(t_series, lags=lags)
    f = plot_pacf(t_series, method='yw', lags=lags)


def func1_2_difference(t_series, period):
    ''' If seasonality is observed, do seasonality differencing '''
    t_series = seasonal_difference(t_series, period)
    return t_series


def func2_0_check_stationarity(t_series):
    ''' Check stationarity '''
    s = stationarity_check(t_series)
    print('The random time series is {}'.format(s))


def func2_1_difference(t_series, times=1):
    ''' If trend is observed or calculated, do differencing '''
    for i in range(times):
        t_series = func1_2_difference(t_series, 1)
    return t_series


def func2_2_check_stationarity(t_series):
    ''' Check stationarity after differencing '''
    func2_0_check_stationarity(t_series)


def func3_0_check_ljungbox(t_series):
    ''' Does ljung box test show evidence of autocorrelation? '''
    ljung_box_pvalue = \
    smapi.stats.acorr_ljungbox(t_series, lags=[np.log(len(t_series))], return_df=True)['lb_pvalue'].values[0]
    if ljung_box_pvalue <= 0.05:
        print('By the Ljung-Box test, there is evidence of autocorrelation. Pvalue:{}'.format(ljung_box_pvalue))
    else:
        print('By the Ljung-Box test, there no is evidence of autocorrelation. Pvalue:{}'.format(ljung_box_pvalue))


def func4_0_get_order(t_series, lags):
    func1_1_plot_acf_pacf(t_series, lags)


def func7_0_apply_all_models(t_series_train, p_ls, d_ls, q_ls, P_ls, D_ls, Q_ls, s_ls, trend_ls, max_order=8,
                             t_series_test=None, min_order=0, t_series_full=None, exog_train=None, exog_test=None,
                             exog_full=None):
    ''' Iterate through all candidate models '''

    if exog_train is None:
        exog_test = None

    if exog_test is None:
        exog_train = None

    a = list(product(p_ls, d_ls, q_ls, P_ls, D_ls, Q_ls, s_ls, trend_ls))
    a = sorted(a, key=lambda x: np.sum(x[:-2]))
    idx_list = []
    aic_list = []
    lb_list = []
    mse_list = []
    degree_list = []
    p_list = []
    d_list = []
    q_list = []
    P_list = []
    D_list = []
    Q_list = []
    s_list = []
    t_list = []

    for idx, (p, d, q, P, D, Q, s, t) in enumerate(a):
        order = p + d + q + P + D + Q
        if (order <= max_order) and (order >= min_order):
            try:
                mod = SARIMAX(t_series_train, order=(p, d, q), seasonal_order=(P, D, Q, s), trend=t, exog=exog_train)
                model = mod.fit()

                if t_series_full is not None:
                    mod2 = SARIMAX(t_series_full, order=(p, d, q), seasonal_order=(P, D, Q, s), trend=t, exog=exog_full)
                    model2 = mod2.fit()
                    aic = model2.aic
                    lb = ljung_box_pvalue = \
                    smapi.stats.acorr_ljungbox(model2.resid, lags=[np.log(len(model2.resid))], return_df=True)[
                        'lb_pvalue'].values[0]
                else:
                    aic = model.aic
                    lb = ljung_box_pvalue = \
                    smapi.stats.acorr_ljungbox(model.resid, lags=[np.log(len(model.resid))], return_df=True)[
                        'lb_pvalue'].values[0]

                if t_series_test is not None:
                    preds = model.predict(len(t_series_train), len(t_series_train) + len(t_series_test) - 1,
                                          exog=exog_test)
                    mse_test = ((preds - t_series_test) ** 2).sum() / len(t_series_test)
                else:
                    mse_test = 0

                idx_list.append(idx)
                aic_list.append(aic)
                lb_list.append(lb)
                mse_list.append(mse_test)
                degree_list.append(order)
                p_list.append(p)
                d_list.append(d)
                q_list.append(q)
                P_list.append(P)
                D_list.append(D)
                Q_list.append(Q)
                s_list.append(s)
                t_list.append(t)

                if lb <= 0.05:
                    print(
                        '{idx} - SARIMA({p},{d},{q},{P},{D},{Q},{s}),trend={t} - aic:{aic}, test_mse = {mse_test}, Ljung-Box:{lb} - Degree={order}'.format(
                            idx=idx, p=p, d=d, q=q, P=P, D=D, Q=Q, s=s, t=t, aic=aic, mse_test=mse_test, lb=lb,
                            order=order))
                else:
                    print(
                        '{idx} - SARIMA({p},{d},{q},{P},{D},{Q},{s}),trend={t} - aic:{aic}, test_mse = {mse_test}, Ljung-Box:{lb} - Degree={order} - LB Not Significant'.format(
                            idx=idx, p=p, d=d, q=q, P=P, D=D, Q=Q, s=s, t=t, aic=aic, mse_test=mse_test, lb=lb,
                            order=order))
            except:
                pass

    df_results = pd.concat(
        [pd.Series(idx_list), pd.Series(aic_list), pd.Series(lb_list), pd.Series(mse_list), pd.Series(degree_list),
         pd.Series(p_list), pd.Series(d_list), pd.Series(q_list), pd.Series(P_list), pd.Series(D_list),
         pd.Series(Q_list), pd.Series(s_list), pd.Series(t_list)], axis=1)
    df_results.columns = ['idx', 'AIC', 'LBPvalue', 'Test MSE', 'Degree', 'p', 'd', 'q', 'P', 'D', 'Q', 's', 't']

    return df_results


def func7_1_final_model(t_series, p, d, q, P, D, Q, s, trend='n', exog=None):
    mod = SARIMAX(t_series, order=(p, d, q), seasonal_order=(P, D, Q, s), trend=trend, exog=exog)
    model = mod.fit()
    t = pd.concat([model.params, model.pvalues], axis=1)
    t.columns = ['coefficients', 'pvalue']
    t = t[(t['pvalue'] <= 0.05) & (t.index.str.contains('.L'))].copy()
    print('***These are the lag coefficients in a regression***')
    display(t)
    print('***These are the full results of the regression***')
    print(model.summary())
    return model


def func8_predict_test(model, df_series, train_size, dynamic=True, val2=None, col='Day', val1='Value'):
    df_series_fit = df_series.set_index(col).iloc[:train_size]
    df_series_test = df_series.set_index(col).iloc[train_size:]
    t_series_fit = df_series_fit[val1]

    if val2 != None:
        t_series2_fit = df_series_fit[val2]
        t_series2_test = df_series_test[val2]

    start = len(t_series_fit)
    end = len(df_series) - 1

    # Predictions
    if val2 != None:
        t_series_predicted = model.predict(start, end, dynamic=dynamic, exog=t_series2_test).rename("Predictions")
    else:
        t_series_predicted = model.predict(start, end, dynamic=dynamic).rename("Predictions")

    t_series_fit = t_series_fit.append(t_series_predicted)
    df_series_final = pd.concat([df_series, t_series_fit.reset_index()[0]], axis=1)
    df_series_final = df_series_final.rename(columns={0: 'Predicted'})

    fig = plt.figure(figsize=(20, 6))
    ax = fig.add_subplot(1, 1, 1)
    sns.lineplot(x=df_series_final[col], y=df_series_final[val1], label='Original', ax=ax)
    sns.lineplot(x=df_series_final[col][train_size:], y=df_series_final['Predicted'][train_size:], label='Predicted',
                 ax=ax)


def func9_forecast(model, df_series, forecast_size, dynamic=True, exog=None, col='Day', val1='Value'):
    df_series_fit = df_series.set_index(col)
    t_series_fit = df_series_fit[val1]

    start = len(df_series)
    end = len(df_series) + forecast_size + 1

    if exog is not None:
        if end - start + 1 > len(exog):
            print('exog has {} rows but you are trying to forcast {}'.format(len(exog), forecast_size))
            print('Adjusting to compensate')
            forecast_size = len(exog) - 2
            end = len(df_series) + forecast_size + 1

    # Predictions
    if exog is not None:
        t_series_predicted = model.predict(start + 1, end, dynamic=dynamic, exog=exog.iloc[:end - start + 1, :]).rename(
            "Predictions")
    else:
        t_series_predicted = model.predict(start + 1, end, dynamic=dynamic).rename("Predictions")

    t_series_fit = t_series_fit.append(t_series_predicted)
    df_series_final = pd.concat([df_series, t_series_fit.reset_index()[0]], axis=1)
    df_series_final = df_series_final.rename(columns={0: 'Predicted'})

    df_new_predictions = pd.DataFrame({col: pd.date_range(df_series_final[col].max(), periods=end, freq='D'),
                                       'Predicted': df_series_final['Predicted'].shift(-1)
                                       })

    df_new_predictions = pd.concat([df_new_predictions, df_series_final[val1]], axis=1)
    df_new_predictions

    fig = plt.figure(figsize=(20, 6))
    ax = fig.add_subplot(1, 1, 1)
    sns.lineplot(x=df_new_predictions[col], y=df_new_predictions[val1], label='Original', ax=ax)
    sns.lineplot(x=df_new_predictions[col][start:], y=df_new_predictions['Predicted'][start:], label='Predicted', ax=ax)


def stationarity_check(t_series):
    pvalue = adfuller(t_series)[1]
    if pvalue <= 0.05:
        return 'stationary pvalue:{}'.format(pvalue)
    else:
        return 'not stationary pvalue:{}'.format(pvalue)


def analyse_time_series(t_series=None, title='', df_series=None, dynamic=True,
                        t_series2=None, col='Day', val1='Value', val2=None,
                        p_ls_user=None, d_ls_user=None, q_ls_user=None,
                        P_ls_user=None, D_ls_user=None, Q_ls_user=None,
                        s_ls_user=None, prop_user=None, max_order_user=None,
                        min_order_user=None, exog=None):
    if t_series is None:
        t_series = df_series.set_index(col)[val1]
        t_series.index = pd.DatetimeIndex(t_series.index.values,
                                          freq=t_series.index.inferred_freq)

    if (t_series2 is None) and (val2 != None):
        t_series2 = df_series.set_index(col)[val2]
        t_series2.index = pd.DatetimeIndex(t_series2.index.values,
                                           freq=t_series2.index.inferred_freq)

    if exog is not None:
        exog = exog.set_index(col)

    user_specified = False
    if (p_ls_user is not None) and (d_ls_user is not None) and (q_ls_user is not None) and (P_ls_user is not None) and (
            D_ls_user is not None) and (Q_ls_user is not None) and (s_ls_user is not None) and (
            prop_user is not None) and (max_order_user is not None) and (min_order_user is not None):
        user_specified = True

    # Set up some initial parameters
    d_ls = [0]
    D_ls = [0]
    s_ls = [0]

    # Get train test
    if not user_specified:
        prop = float(input('What proportion of the dataset should be the training set?'))
    else:
        prop = prop_user

    n_train = int(len(t_series) * prop)
    t_series_train = t_series[:n_train]
    t_series_test = t_series[n_train:]

    t_series2_train = None
    t_series2_test = None
    if val2 is not None:
        t_series2_train = t_series2[:n_train]
        t_series2_test = t_series2[n_train:]

    # Start the process
    print('*********1-Observe the time series for heteroscedasticity and seasonality')
    title = title
    sleep(1)
    func1_0_plot_series_traintest(t_series_train, t_series_test, title)
    plt.show()
    sleep(1)

    if not user_specified:
        while True:
            lags = input('How many lags to display (c to continue, q to quit)?')
            threshold = int(len(t_series_train) / 2)

            if (str.isdigit(lags)) and (int(lags) > threshold):
                print('Please choose a value < {}'.format(threshold))
            else:
                if lags.lower() == 'c':
                    break
                elif lags.lower() == 'q':
                    return None
                func1_1_plot_acf_pacf(t_series_train, int(lags))
                plt.show()

    sleep(1)

    print()

    if not user_specified:
        has_seasonality = input('Do you see seasonality (y/n)? (q to quit)')
        if has_seasonality.lower() == 'q':
            return None

        if has_seasonality.lower() in ['y', 'yes']:
            print('*********1-1-There is seasonality so we remove it')
            period = input('What is the period?')
            t_series_train = func1_2_difference(t_series_train, int(period))
            sleep(1)
            title = 'Seasonality Removed'
            s_ls = [int(period)]
            D_ls = [0, 1]
            d_ls = [0, 1]
            func1_0_plot_series(t_series_train, title)
            plt.show()
            sleep(1)
        else:
            print('*********1-1-There is no seasonality')

    print()

    print('*********2-Check Stationarity')
    func2_0_check_stationarity(t_series_train)

    print()

    if not user_specified:
        has_trend = input('Is there evidence of trend (y/n)? (q to quit)')
        if has_trend.lower() == 'q':
            return None
        if has_trend.lower() in ['y', 'yes']:
            print('*********2-1-There is trend so we difference')
            t_series_train = func2_1_difference(t_series_train, 1)
            d_ls = [0, 1]
            print('*********2-2-Check Stationarity')
            func2_2_check_stationarity(t_series_train)
        else:
            print('*********2-1-There is no trend')

    print()

    if not user_specified:
        trend_elements = input('Want to specify trend elements (y/n)?')
        if trend_elements.lower() in ['y', 'yes']:
            d_user = input('Specify max d?')
            d_ls = list(range(int(d_user) + 1))
            D_user = input('Specify max D?')
            D_ls = list(range(int(D_user) + 1))

        print('*********3-Test if there are any autocorrelation terms (Ljung box)')
        func3_0_check_ljungbox(t_series_train)

        lb_evidence = input('Is the lb p-value significant (y/n)? (q to quit)')
        if lb_evidence.lower() == 'q':
            return None
    else:
        lb_evidence = 'y'

    if lb_evidence.lower() in ['y', 'yes']:
        print('*********4/5-Get the order')
        sleep(1)

        if not user_specified:
            while True:
                lags = input('How many lags to display? (c to continue, q to quit)')
                threshold = int(len(t_series_train) / 2)

                if (str.isdigit(lags)) and (int(lags) > threshold):
                    print('Please choose a value < {}'.format(threshold))
                else:
                    if lags.lower() == 'c':
                        break
                    elif lags.lower() == 'q':
                        raise Exception('Quit!')
                    func4_0_get_order(t_series_train, int(lags))
                    plt.show()
        sleep(1)

        print()

        if not user_specified:
            print('*********7/8-Get the best model')
            p = input('What p order (PACF) do you want to try to?')
            p_ls = [i for i in range(int(p) + 1)]
            q = input('What q order (ACF) do you want to try to?')
            q_ls = [i for i in range(int(q) + 1)]
            P = input('What P order (PACF) do you want to try to?')
            P_ls = [i for i in range(int(P) + 1)]
            Q = input('What Q order (ACF) do you want to try to?')
            Q_ls = [i for i in range(int(Q) + 1)]
            trend_ls = ['n']
            max_order = int(input('What is the max order you want to try?'))
            min_order = int(input('What is the min order you want to try?'))
        else:
            p_ls = p_ls_user
            q_ls = q_ls_user
            P_ls = P_ls_user
            Q_ls = Q_ls_user
            d_ls = d_ls_user
            D_ls = D_ls_user
            trend_ls = ['n']
            s_ls = s_ls_user
            max_order = max_order_user
            min_order = min_order_user

        print(
            'Candidate models: p={p_ls},d={d_ls},q={q_ls},P={P_ls},D={D_ls},Q={Q_ls},s={s_ls},trend={trend_ls}'.format(
                p_ls=p_ls, d_ls=d_ls, q_ls=q_ls, P_ls=P_ls, D_ls=D_ls, Q_ls=Q_ls, s_ls=s_ls, trend_ls=trend_ls))
        t_series_train = t_series[:n_train]
        t_series_test = t_series[n_train:]
        if val2 is not None:
            t_series2_train = t_series2[:n_train]
            t_series2_test = t_series2[n_train:]

        df_results = func7_0_apply_all_models(t_series_train, p_ls=p_ls, d_ls=d_ls, q_ls=q_ls, P_ls=P_ls, D_ls=D_ls,
                                              Q_ls=Q_ls, s_ls=s_ls, trend_ls=trend_ls, max_order=max_order,
                                              t_series_test=t_series_test, min_order=min_order, t_series_full=t_series,
                                              exog_train=t_series2_train, exog_test=t_series2_test, exog_full=t_series2)
        display(df_results[df_results['LBPvalue'] > 0.05].sort_values(by='AIC').head(30))

        while True:
            idx = input('Choose the idx of the model you want or specify (p,d,q,P,D,Q,s)')
            if ',' in idx:
                (p, d, q, P, D, Q, s) = idx.split(',')
            else:
                idx = int(idx)
                df_temp = df_results[df_results['idx'] == idx].copy()
                p = df_temp['p']
                d = df_temp['d']
                q = df_temp['q']
                P = df_temp['P']
                D = df_temp['D']
                Q = df_temp['Q']
                s = df_temp['s']
                t = df_temp['t']

            print('Your chosen model = {}'.format(
                'SARIMA({p},{d},{q},{P},{D},{Q},{s}),trend=n'.format(p=p, d=d, q=q, P=P, D=D, Q=Q, s=s)))
            model = func7_1_final_model(t_series, p=int(p), d=int(d), q=int(q), P=int(P), D=int(D), Q=int(Q), s=int(s),
                                        exog=t_series2)

            func8_predict_test(model, df_series, len(t_series_train), dynamic=dynamic, val2=val2, col=col, val1=val1)
            plt.show()
            sleep(1)
            print('*********9-Forecast')
            sleep(1)
            forecast_size = int(input('Specify forecast size:'))

            func9_forecast(model, df_series, forecast_size, dynamic=dynamic, exog=exog, col=col, val1=val1)
            plt.show()
            sleep(1)

            rep = input('Happy with this model (y/n)? (q to quit)')
            if rep.lower() == 'q':
                return None

            if rep.lower() in ['y', 'yes']:
                return {'model': model, 'df_results': df_results.sort_values(by='AIC'), 'p': p, 'd': d, 'q': q, 'P': P,
                        'D': D, 'Q': Q, 's': s}