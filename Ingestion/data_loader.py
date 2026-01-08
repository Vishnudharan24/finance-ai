import pandas as pd
from pathlib import Path

supported_extensions = [".csv", ".xlsx", ".json", ".xls"]

def data_loader(file_path: str) -> pd.DataFrame:
    """
    Input: 
      -> Filepath of the excel/csv/json has been inputted.

    Output:
      -> It is being converted into a pandas dataframe.

    """

    path = Path(file_path)
    # print(path.suffix)

    if path.suffix not in supported_extensions:
        # print(f"Unsupported file type: {path.suffix}")
        raise ValueError(f"Unsupported file type: {path.suffix}")
    
    if path.suffix == ".csv":
        data_df = pd.read_csv(path)

    elif path.suffix == ".xlsx" or path.suffix == ".xls":
        data_df = pd.read_excel(path)
    
    elif path.suffix == ".json":
        data_df = pd.read_json(path)
    
    return data_df


# file_path = input("Enter the filepath : ")
# data_loader(file_path)