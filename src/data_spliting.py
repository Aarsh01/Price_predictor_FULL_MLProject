from abc import ABC, abstractmethod
import pandas as pd
import logging
from sklearn.model_selection import train_test_split

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataSplitingStrategy(ABC):
    def splitData(self, df:pd.DataFrame, target_col):
        self.target_col=target_col

class SimpleTrainTestSplitStrategy(DataSplitingStrategy):

    def __init__(self, test_size=0.2, random_state=42):
        self.rs=random_state
        self.ts=test_size

    def splitData(self, df,target_col):
        logging.info("Performing simple train-test split.")
        X=df.drop(columns=target_col)
        Y=df[target_col]

        X_train,X_test, Y_train, Y_test = train_test_split(X,Y, random_state=self.rs, test_size=self.ts)

        return X_train, X_test, Y_train, Y_test
    
class DataSpliterTrainTest(DataSplitingStrategy):

    def __init__(self, strategy: DataSplitingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DataSplitingStrategy):
        logging.info("Switching data splitting strategy.")
        self._strategy = strategy

    def split(self, df: pd.DataFrame, target_column: str):
        logging.info("Splitting data using the selected strategy.")
        return self._strategy.splitData(df,target_col=target_column)
    