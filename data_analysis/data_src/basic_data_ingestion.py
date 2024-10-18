from abc import ABC, abstractmethod
import pandas as pd


# Abstract Base Class for Data Inspection Strategies
# --------------------------------------------------
# This class defines a common interface for data inspection strategies.
# Subclasses must implement the inspect method.
class BasicInspectionStrategy(ABC):
    @abstractmethod
    def inspect(self, df: pd.DataFrame):
        """
        Perform a specific type of data inspection.

        Parameters:
        df (pd.DataFrame): The dataframe on which the inspection is to be performed.

        Returns:
        None: This method prints the inspection results directly.
        """
        pass

class InfoInspectionOfData(BasicInspectionStrategy):
    def inspect(self, df: pd.DataFrame):
        print("Data Types and Non-Null Counts:")
        print(df.info())
        print("\n")

class DescribeTheData(BasicInspectionStrategy):
    def inspect(self, df:pd.DataFrame):
        print("Describe the DataSet:")
        print(df.describe())

class DescribeNumericalData(BasicInspectionStrategy):
    def inspect(self, df: pd.DataFrame):
        # Filter for numerical columns
        numerical_df = df.select_dtypes(include=['int64', 'float64'])
        
        print("Describe the Numerical Data:")
        print(numerical_df.describe())
        print("\n")

class CategoricalNumericalDataTypes(BasicInspectionStrategy):
    def inspect(self, df: pd.DataFrame):
        col_categorical = [col for col in df.columns if df[col].dtype == 'object']
        col_numerical = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
        
        print("Categorical Columns:")
        print(col_categorical)
        print("\nNumerical Columns:")
        print(col_numerical)
        print("\n")
# class MissingValuesInspection(BasicInspectionStrategy):
#     def inspect(self, df: pd.DataFrame):
#         # Calculate the percentage of missing values
#         missing_percentage = (df.isnull().sum().sort_values(ascending=False) / df.shape[0]) * 100
        
#         # Get the data types of the columns
#         data_types = df.dtypes
        
#         # Create a new DataFrame to combine both information
#         inspection_df = pd.DataFrame({
#             'Missing Percentage (%)': missing_percentage,
#             'Data Type': data_types
#         })
        
#         # Print the combined DataFrame
#         print(inspection_df)
#         print("\n")


# Context Class that uses a BasicInspectionStrategy
# ------------------------------------------------
# This class allows you to switch between different data inspection strategies.

class DataInspector:
    def __init__(self, strategy: BasicInspectionStrategy):
        """
        Initializes the DataInspector with a specific inspection strategy.

        Parameters:
        strategy (DataInspectionStrategy): The strategy to be used for data inspection.

        Returns:
        None
        """
        self._strategy = strategy

    def set_strategy(self, strategy: BasicInspectionStrategy):
        """
        Sets a new strategy for the DataInspector.

        Parameters:
        strategy (DataInspectionStrategy): The new strategy to be used for data inspection.

        Returns:
        None
        """
        self._strategy = strategy

    def execute_inspection(self, df: pd.DataFrame):
        """
        Executes the inspection using the current strategy.

        Parameters:
        df (pd.DataFrame): The dataframe to be inspected.

        Returns:
        None: Executes the strategy's inspection method.
        """
        self._strategy.inspect(df)


# Example usage
# if __name__ == "__main__":
#     # Example usage of the DataInspector with different strategies.

#     # Load the data
#     df = pd.read_csv('/Users/aarsh/Downloads/mlops/extracted_data/titanic_toy.csv')
#     strategies = [
#             InfoInspectionOfData(),
#             DescribeTheData(),
#             CategoricalNumericalDataTypes(),
#         ]
#     # Initialize the DataInspector with the strategies
#     inspector = DataInspector(strategies)
    
#     # Execute the inspections
#     inspector.execute_inspection(df)




