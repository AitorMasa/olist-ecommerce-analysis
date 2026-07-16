import pandas as pd

def basic (df):
    print(df.head())
    print(df.shape)
    print(df.columns)
    dup= df.duplicated().sum()
    print("DUPLICADOS:", dup)
    nuls= df.isna().sum()
    print("NULOS:", nuls)
    if dup<0:
        print(df.loc[df.duplicated(keep=False)])
    if nuls.sum()<0:
        print(df.loc[df.isna()])
    
def basic_col (df,column,Issues):
    print(df[column].head())
    print(df[column].shape)
    print(df[column].describe())
    df[column]=df[column].astype("string").str.strip().str.upper()
    print(df[column].value_counts())
    dup= df[column].duplicated().sum()
    print("DUPLICADOS:", dup)
    nuls= df[column].isna().sum()
    print("NULOS:", nuls)
    if dup<0:
        print(df.loc[df.duplicated(keep=False)])
    if nuls<0:
        print(df.loc[df.isna()])

def numeric (df,column,Issues):
    print(df[column].shape)
    print(df[column].describe())
    mask_negativos=df[column]<0
    nuls=df[column].isna().sum()
    print("NULOS",nuls)
    print("NEGATIVOS", mask_negativos.sum())
    print(df.loc[mask_negativos])
    if mask_negativos.sum()>0:
       Issues[f"{column}_negativos"] =  df.loc[mask_negativos].copy()   
    print("MIN",df[column].min())
    print("MAX",df[column].max())           
                
def mask(df,column,pattern,Issues):
    mask_valid=df[column].astype(str).str.match(pattern, na=False)
    print("VALIDAS:", mask_valid.sum())
    mask_invalid=~ mask_valid
    print("INVALIDAS:",mask_invalid.sum())
    if mask_invalid.sum()>0:
        print(df[column].loc[mask_invalid])
        Issues[f"{column}_invalidos"] =  df.loc[mask_invalid].copy()
    return mask_valid, mask_invalid    

def fecha (df,column):
    df[column]=pd.to_datetime(df[column],format="mixed",errors="coerce",dayfirst="true")
    invalid= df[column].isna().sum()
    print("FECHAS INVALIDAS", invalid)
    print(df[column].loc[invalid])
    if invalid>0:
        print("NO VALIDAS",invalid)
    else:
        print("VALIDAS")
    
def export_issues(Issues, ISSUES):

    print("EXPORTANDO A:", ISSUES)
    for nombre, df_issue in Issues.items():
        print("GUARDANDO:", nombre)
        df_issue.to_csv(ISSUES / f"{nombre}.csv",index=False)  
    
 