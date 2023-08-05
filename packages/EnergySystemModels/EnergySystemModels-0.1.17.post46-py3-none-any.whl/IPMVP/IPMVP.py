import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import numpy as np
#pip install statsmodels
import statsmodels.api as sm


def Mathematical_Models(y,X,start_baseline_period,end_baseline_period,start_reporting_period,end_reporting_period):
    #remettre les données dans l'ordre
    y=pd.DataFrame(y).sort_index(axis=0, ascending=True, inplace=False, kind="quicksort")
    X=pd.DataFrame(X).sort_index(axis=0, ascending=True, inplace=False, kind="quicksort")
    #calculer de delta t
    dt = y.index.to_series().diff().astype('timedelta64[h]')
    curent_delta_time=dt.mean()
    #print(curent_delta_time)


    # if end_reporting_period is None :
    #     end_reporting_period = df.tail(1).index.strftime("%Y/%m/%d")[0]
    #     print("the end of the reporting period is the current date",end_reporting_period)

    #le jeu de données de la periode de référence
    X_bl = X.loc[(X.index >= start_baseline_period) & (X.index <= end_baseline_period)]
    #print("X base line", X_bl.head)

    y_bl = y.loc[(y.index >= start_baseline_period) & (y.index <= end_baseline_period)]
    #print("y base line", y_bl)
  

    # Modeling :
    
    model = LinearRegression()
    model.fit(X_bl,y_bl)
    y_pred = model.predict(X_bl) # predicted consumption
    
    n = len(y_bl) # nombre de population
    p=X_bl.shape[1] #nb variables explicatives

    # Calcul du R2
    r2 = model.score(X_bl, y_bl)
    #print('R2:', r2)

    # Affichage des coefficients et l'intercept
    coefficients = []
    for p_ in range(p):
        coefficients.append(model.coef_[0, p_])
    
    const = model.intercept_[0]



    # Calcul du RMSE
    mse = mean_squared_error(y_bl, y_pred, squared=True)
    ddof=max(n-p-1,0) # le degrès de liberté (comme celui d'excel)
    rmse=(mse*((n)/ddof))**0.5 #comme celui d'excel
   

    #calcul du CV_RMSE
    cv_rmse=rmse/y_bl.mean()[0]
   

    # calcul des erreurs standard...................................................
    # Calculer les erreurs types des coefficients
    # add a constant term to the input data for statsmodels
    X_bl_withConst = sm.add_constant(X_bl)
    # fit a linear regression model using statsmodels
    model_sm = sm.OLS(y_bl, X_bl_withConst).fit()
    # extract the standard errors of the coefficients from the statsmodels model
    serr = pd.DataFrame(model_sm.bse).T
    serr = serr.rename(index={0: 'ANTE-POST'})
    #serr=serr.add_prefix("SE_")

    # print the standard errors
    print("serr====================",serr)

    const_coef=(pd.DataFrame([np.concatenate(([const], coefficients))],columns=np.concatenate((['const'], X_bl.columns)).tolist()).rename(index={0: 'ANTE-POST'})).astype(float)
    print("const_coef=========================",const_coef)

    #calcul de la statistique t de chaque coef
    #stat_t=const_coef.astype(float).div(serr.astype(float))
   
    print(list(serr.columns),list(const_coef.columns))
    stat_t=const_coef.div(serr)
    
    print("stat_t===============",stat_t)

    stat_t=stat_t.add_prefix("stat_t_")

    print("stat_t===============",stat_t)
   
    

    # Modèle y_predicted_arr = modèle y avec arrondis [const,DJU,planning]:
    df=pd.DataFrame([[r2,rmse,cv_rmse,ddof]], columns=["r2","rmse","cv_rmse","ddof"], index=["ANTE-POST"])
  
    df=pd.merge( const_coef.add_prefix("coef_"),df, left_index=True, right_index=True)
    df=pd.merge(df, serr.add_prefix("serr_"), left_index=True, right_index=True)
    df=pd.merge(df,stat_t, left_index=True, right_index=True).T

    y_pred=pd.DataFrame(y_pred)   
    y_pred = y_pred.set_index(y_bl.index)     

    return  y_pred,df
   
  

