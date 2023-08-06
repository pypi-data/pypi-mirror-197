import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import numpy as np
#pip install statsmodels 
import statsmodels.api as sm

def drop_outliers (df,threshold):
    # Select only the numeric columns
    df = df.select_dtypes(include=np.number)    
    # Calculate the z-score for the numeric columns
    z_scores = (df - df.mean()) / df.std()
    print(z_scores)
    # Get the location of the outliers
    outlier_location = np.argwhere((z_scores > threshold).values)
    #valeur à supprimer
    df_out = df[(z_scores >= threshold).any(axis=1)]

    if df_out.empty or df_out.isnull().all(axis=1).any():
        pass
    else:
        print("valeurs à supprimer",df_out,outlier_location )
        

  
        

    # # Exclude rows where any z-score is greater than 3
    df = df[(z_scores < threshold).all(axis=1)]
    #print(df)
    return df




def conformite_ipmvp(r2,cv_remse,stat_t): #,,
    conformite=[]
    if r2>=0.75:
        conformite.append([r2,True])
    else:
        conformite.append([r2,False])
    if cv_remse<=0.2:
        conformite.append([cv_remse,True])
    else:
        conformite.append([cv_remse,False])

    conformite=(pd.DataFrame(conformite,index=["r2","cv_remse"],columns=["valeur","conformité IPMVP"]))
    stat_t = stat_t.rename(index={stat_t.index[0]: 'valeur'})
    stat_t_T=stat_t.T
    stat_t_T["conformité IPMVP"] = stat_t_T["valeur"].apply(lambda x: True if (x is not None and float(x) >= 2) else False) 
    
    conformite=pd.concat([conformite,stat_t_T])
    # print(conformite)

    return conformite

# stat_t=pd.DataFrame([[-0.072971,12.51099,None,None]],columns=["stat_t_const",  "stat_t_DJU",  "stat_t_x2" , "stat_t_x3"],index=["valeur"])    
# conformite_ipmvp(0.9,0.1,stat_t)

def Mathematical_Models(y,X,start_baseline_period,end_baseline_period,start_reporting_period,end_reporting_period):
    #remettre les données dans l'ordre
    y=pd.DataFrame(y).sort_index(axis=0, ascending=True, inplace=False, kind="quicksort")
    X=pd.DataFrame(X).sort_index(axis=0, ascending=True, inplace=False, kind="quicksort")
    drop_outliers(y,3)
    #drop_outliers(X,3)

    #calculer de delta t
    dt = y.index.to_series().diff().astype('timedelta64[h]')
    curent_delta_time=dt.median()
    print("curent_delta_time (heures)",curent_delta_time)


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

    conformite=conformite_ipmvp(r2,cv_rmse,stat_t)   

    return  y_pred,df,conformite
   
  

