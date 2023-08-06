import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from scipy.stats import t
from sklearn.metrics import mean_squared_error



import numpy as np
#pip install statsmodels 
import statsmodels.api as sm




# supp les val aber.
def drop_outliers (df,threshold):
    # Select only the numeric columns
    df = df.select_dtypes(include=np.number)    
    # Calculate the z-score for the numeric columns
    z_scores = (df - df.mean()) / df.std()
    print("z_scores----------------------------",z_scores.max())
    # Get the location of the outliers
    outlier_location = np.argwhere((z_scores > threshold).values)
    #valeur à supprimer
    df_out = df[(z_scores >= threshold).any(axis=1)]
    print(df_out.index,type(df_out.index))

    if df_out.empty or df_out.isnull().all(axis=1).any():
        pass
    else:
        print("valeurs à supprimer",df_out,outlier_location )

    # # Exclude rows where any z-score is greater than 3
    df = df[(z_scores < threshold).all(axis=1)]
    #print(df)
    return df,df_out


def conformite_ipmvp(r2,cv_remse,stat_t,stat_t_normale95): #,,
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
    stat_t_T["conformité IPMVP"] = stat_t_T["valeur"].apply(lambda x: True if (x is not None and float(x) >= stat_t_normale95) else False) 
    
    conformite=pd.concat([conformite,stat_t_T])
    # print(conformite)

    return conformite

# stat_t=pd.DataFrame([[-0.072971,12.51099,None,None]],columns=["stat_t_const",  "stat_t_DJU",  "stat_t_x2" , "stat_t_x3"],index=["valeur"])    
# conformite_ipmvp(0.9,0.1,stat_t)
def regression_model(X_bl,y_bl,approache):
    #approache="ANTE-POST"
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

    stat_t_normale95=t.ppf(1-0.05/2, ddof)
    print("statistique ************************************* loi normale",ddof,stat_t_normale95)
    
   
    #calcul du CV_RMSE
    cv_rmse=rmse/y_bl.mean()[0]

    ######################calculs d'incertitude##################################################
    niveau_confiance=0.8
    gamma=(1-niveau_confiance)/2
    stat_t_normale=t.ppf(niveau_confiance+gamma, ddof)
    
    print("statistique t loi normale",ddof,stat_t_normale)
    precision_absolue=stat_t_normale*rmse
    precision_relative=precision_absolue/y_bl.mean()[0]


    table_incertitude=pd.DataFrame({"valeurs":[gamma,niveau_confiance,stat_t_normale,rmse,precision_absolue,precision_relative]},index=["gamma","niveau_confiance","stat_t_normale","Erreur type (rmse)","precision_absolue","precision_relative"]).round(2)
    print(table_incertitude)
    #############################################################################################################################################################################################################
   

    # calcul des erreurs standard...................................................
    # Calculer les erreurs types des coefficients
    # add a constant term to the input data for statsmodels
    X_bl_withConst = sm.add_constant(X_bl)
    # fit a linear regression model using statsmodels
    model_sm = sm.OLS(y_bl, X_bl_withConst).fit()
    # extract the standard errors of the coefficients from the statsmodels model
    serr = pd.DataFrame(model_sm.bse).T
    serr = serr.rename(index={0: approache})
    #serr=serr.add_prefix("SE_")

    # print the standard errors
    print("serr====================",serr)

    const_coef=(pd.DataFrame([np.concatenate(([const], coefficients))],columns=np.concatenate((['const'], X_bl.columns)).tolist()).rename(index={0: approache})).astype(float)
    print("const_coef=========================",const_coef)

    #calcul de la statistique t de chaque coef
    #stat_t=const_coef.astype(float).div(serr.astype(float))
   
    print(list(serr.columns),list(const_coef.columns))
    stat_t=const_coef.div(serr)
    
    print("stat_t===============",stat_t)

    stat_t=stat_t.add_prefix("stat_t_")

    print("stat_t===============",stat_t)
   
    

    # Modèle y_predicted_arr = modèle y avec arrondis [const,DJU,planning]:
    df=pd.DataFrame([[r2,rmse,cv_rmse,ddof]], columns=["r2","rmse","cv_rmse","ddof"], index=[approache])
  
    df=pd.merge( const_coef.add_prefix("coef_"),df, left_index=True, right_index=True)
    df=pd.merge(df, serr.add_prefix("serr_"), left_index=True, right_index=True)
    df=pd.merge(df,stat_t, left_index=True, right_index=True).T

    y_pred=pd.DataFrame(y_pred)   
    y_pred = y_pred.set_index(y_bl.index)  

    conformite=conformite_ipmvp(r2,cv_rmse,stat_t,stat_t_normale95)

    return model,y_pred,df,conformite,table_incertitude


def Mathematical_Models(y,X,start_baseline_period,end_baseline_period,start_reporting_period,end_reporting_period):
    #remettre les données dans l'ordre
    y=pd.DataFrame(y).sort_index(axis=0, ascending=True, inplace=False, kind="quicksort")
    X=pd.DataFrame(X).sort_index(axis=0, ascending=True, inplace=False, kind="quicksort")
    y,y_out=drop_outliers(y,3)
    #X,X_out=drop_outliers(X,3)
    X= X.drop(y_out.index, axis=0)

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

    # jeu de données de la periode de suivi
    X_report = X.loc[(X.index >= start_reporting_period) & (X.index <= end_reporting_period)]
    y_report = y.loc[(y.index >= start_reporting_period) & (y.index <= end_reporting_period)]

  
##########################################################################################################################""
    # # Modeling :
   

    model_bl,y_pred,df,conformite,table_incertitude=regression_model(X_bl,y_bl,"ANTE-POST") 

    model_report,y_pred_report,df_report,conformite_report,table_incertitude_report=regression_model(X_report,y_report,"POST-ANTE") 

    sum_report_prediction= sum(model_bl.predict(X_report))[0]
    sum_bl_prediction= sum(model_report.predict(X_bl))[0]

    sum_bl=y_bl.sum().values[0]
    sum_report=y_report.sum().values[0]

    savings_post=(sum_report_prediction-sum_report)/sum_report*100
    saving_ante=(sum_bl_prediction-sum_bl)/sum_bl*100

    df_savings=pd.DataFrame({"ANTE-POST":[sum_report,sum_report_prediction,savings_post],"POST-ANTE":[sum_bl,sum_bl_prediction,saving_ante]},index=["Relevé de consommation","Prédiction","pourcentage d'économie>0"]).round(2)

    return  y_pred,df,conformite,table_incertitude,y_pred_report,df_report,conformite_report,table_incertitude_report,df_savings
   
  

