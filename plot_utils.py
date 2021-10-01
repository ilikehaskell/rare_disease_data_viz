import pandas as pd

# concat trick needed because of strange Altair+Streamlit+Pandas pivoted DF interaction resulting in
# ValueError: variable encoding field is specified without a type; the type cannot be inferred because it does not match any column in the data.
def plotable(df):
    return pd.concat([pd.Series(df[col_name]) for col_name in df.columns], axis=1)