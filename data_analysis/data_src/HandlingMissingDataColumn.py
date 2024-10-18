# import pandas as pd
# import matplotlib.pyplot as plt
# from abc import ABC, abstractmethod

# class HandlingMissingDataColumn(ABC):
#     @abstractmethod
#     def handle(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Abstract method to handle missing data in a DataFrame."""
#         pass

# class HandlingMissingNumericalDataColumn(HandlingMissingDataColumn):
#     def handle(self, df: pd.DataFrame) -> pd.DataFrame:
#         # Identify numerical columns in the DataFrame
#         cols_numerical = [num for num in df.columns if df[num].dtype != 'object']
#         print("Numerical Data Columns:", cols_numerical)

#         # Calculate the percentage of missing values for each numerical column
#         missing_percentage = df[cols_numerical].isnull().mean() * 100
        
#         # Identify columns that have more than 5% missing values
#         cols_to_drop = missing_percentage[missing_percentage > 5].index.tolist()
        
#         # Drop the identified columns from the DataFrame
#         df_new = df.drop(columns=cols_to_drop)
#         print(f"Columns dropped: {cols_to_drop}")
#         print(f"New DataFrame shape after dropping columns: {df_new.shape}, Original shape: {df.shape}")
        
#         return df_new


# class HandlingMissingCategoricalDataColumn(HandlingMissingDataColumn):
#     def handle(self, df: pd.DataFrame) -> pd.DataFrame:
#         # Identify categorical columns in the DataFrame
#         cols_categorical = [num for num in df.columns if df[num].dtype == 'object']
#         print("Categorical Data Columns:", cols_categorical)

#         # Calculate the percentage of missing values for each categorical column
#         missing_percentage = df[cols_categorical].isnull().mean() * 100
        
#         # Identify columns that have more than 6% missing values
#         cols_to_drop = missing_percentage[missing_percentage > 6].index.tolist()
        
#         # Drop the identified columns from the DataFrame
#         df_new = df.drop(columns=cols_to_drop)
#         print(f"Columns dropped: {cols_to_drop}")
#         print(f"New DataFrame shape after dropping columns: {df_new.shape}, Original shape: {df.shape}")
        
#         return df_new
    


# class HandleMissingDataAnalyzerColumn:
#     def __init__(self, strategy: HandlingMissingDataColumn):
#         """
#         Initializes the HandleMissingDataAnalyzer with a specific strategy.

#         Parameters:
#         strategy (HandlingMissingDataColumn): The strategy to be used for handling missing data.
#         """
#         self._strategy = strategy

#     def set_strategy(self, strategy: HandlingMissingDataColumn):
#         """
#         Sets a new strategy for the HandleMissingDataAnalyzer.

#         Parameters:
#         strategy (HandlingMissingDataColumn): The new strategy to be used for handling missing data.
#         """
#         self._strategy = strategy

#     def execute_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
#         """
#         Executes the analysis using the current strategy.

#         Parameters:
#         df (pd.DataFrame): The DataFrame containing the data.

#         Returns:
#         pd.DataFrame: The DataFrame after handling missing data.
#         """
#         return self._strategy.handle(df)
