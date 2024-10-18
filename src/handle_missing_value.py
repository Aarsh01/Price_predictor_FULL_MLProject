from abc import ABC, abstractmethod
import pandas as pd
import logging
from sklearn.impute import SimpleImputer

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class HandleMissingValue(ABC):
    @abstractmethod
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

# Taken the reference from "data_analysis\data_src\HandlingMissingDataRow.py" and "data_analysis\data_src\HandlingMissingDataColumn.py"
class DropMissingValuesStrategy(HandleMissingValue):
    def __init__(self, axis, threshold):
        self.axis = axis
        self.threshold = threshold
    
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info(f"Dropping missing values with axis: {self.axis} with threshold: {self.threshold}")
        df_cleaned = df.dropna(axis=self.axis, thresh=self.threshold)
        logging.info("Missing value cleaned")
        return df_cleaned
    
class ImputeMissingStrategy(HandleMissingValue):
    def __init__(self, strategy, fill_with=None):
        self.strategy = strategy
        self.fill_with = fill_with
    
    def handle(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info(f"Filling missing values using method: {self.strategy}")
        df_cleaned = df.copy()
        cols_categorical = [col for col in df_cleaned.columns if df_cleaned[col].dtype == 'object']
        cols_numerical = [col for col in df_cleaned.columns if df_cleaned[col].dtype != 'object']

        if self.strategy == 'mean': 
            impute = SimpleImputer(strategy='mean')
            df_cleaned[cols_numerical] = impute.fit_transform(df_cleaned[cols_numerical])

        elif self.strategy == 'median': 
            impute = SimpleImputer(strategy='median')  # Corrected to 'median'
            df_cleaned[cols_numerical] = impute.fit_transform(df_cleaned[cols_numerical])

        elif self.strategy == 'most_frequent': 
            impute = SimpleImputer(strategy='most_frequent')
            df_cleaned[cols_categorical] = impute.fit_transform(df_cleaned[cols_categorical])

        elif self.strategy == 'mode':
            impute = SimpleImputer(strategy='most_frequent')  # Use 'most_frequent' for mode
            df_cleaned[cols_categorical] = impute.fit_transform(df_cleaned[cols_categorical])    

        elif self.strategy == "constant":
            df_cleaned = df_cleaned.fillna(self.fill_with)
        
        else:
            logging.warning(f"Unknown method '{self.strategy}'. No missing values handled.")

        logging.info("Missing values filled.")
        return df_cleaned

class MissingValueHandler:
    def __init__(self, strategy: HandleMissingValue):
        self._strategy = strategy

    def set_strategy(self, strategy: HandleMissingValue):
        logging.info("Switching missing value handling strategy.")
        self._strategy = strategy

    def excute(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info("Executing missing value handling strategy.")
        return self._strategy.handle(df)
    
# # Example usage
# if __name__ == "__main__":
#     # Example dataframe
#     df = pd.read_csv('/Users/aarsh/Downloads/mlops/extracted_data/titanic_toy.csv')

#     # Initialize missing value handler with a specific strategy
#     missing_value_handler = MissingValueHandler(DropMissingValuesStrategy(axis=0, threshold=3))
#     df_cleaned = missing_value_handler.handle_missing_values(df)

#     # Switch to filling missing values with mean
#     missing_value_handler.set_strategy(ImputeMissingStrategy(strategy='mean'))
#     df_filled = missing_value_handler.handle_missing_values(df)
