import pandas as pd

def basic (df):
    dup= df.duplicated().sum()
    nuls= df.isna().sum()
    
def basic_col (df,column,Issues):
    df[column]=df[column].astype("string").str.strip().str.upper()
    dup= df[column].duplicated().sum()
    nuls= df[column].isna().sum()

def numeric (df,column,Issues):

    mask_negativos=df[column]<0
    nuls=df[column].isna().sum()
    if mask_negativos.sum()>0:
       Issues[f"{column}_negativos"] =  df.loc[mask_negativos].copy()          
                
def mask(df,column,pattern,Issues):
    mask_valid=df[column].astype(str).str.match(pattern, na=False)
    mask_invalid=~ mask_valid
    if mask_invalid.sum()>0:
        Issues[f"{column}_invalidos"] =  df.loc[mask_invalid].copy()
    return mask_valid, mask_invalid    

def fecha (df,column):
    df[column]=pd.to_datetime(df[column],format="mixed",errors="coerce",dayfirst="true")
    invalid= df[column].isna().sum()
    
def export_issues(Issues, ISSUES):


    for nombre, df_issue in Issues.items():

        df_issue.to_csv(ISSUES / f"{nombre}.csv",index=False)  
    
 