from zenml import step 
from src.data_spliting import DataSpliterTrainTest,SimpleTrainTestSplitStrategy
import pandas as pd
from typing import Tuple


@step
def data_split_zenmlStep(df:pd.DataFrame,target)-> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    splitter=DataSpliterTrainTest(SimpleTrainTestSplitStrategy())
    X_train, X_test, Y_train, Y_test = splitter.split(df,target_column=target)
    return X_train, X_test, Y_train, Y_test
