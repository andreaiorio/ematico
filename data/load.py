import pandas as pd


def load_data(file_path):
    # Function to load and preprocess data
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, "Results", header=0)
    df[df.columns.drop("Data")] = df[df.columns.drop("Data")].apply(pd.to_numeric)

    df_rif = pd.read_excel(xls, "Ranges", header=0)
    df_rif.iloc[:-1, :] = df_rif.iloc[:-1, :].apply(pd.to_numeric)

    categories = pd.read_excel(xls, "Categories", header=0).to_dict(orient="list")
    categories = {
        key: [value for value in values if pd.notna(value)]
        for key, values in categories.items()
    }

    return df, df_rif, categories
