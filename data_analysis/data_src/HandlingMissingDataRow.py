# import pandas as pd
# import matplotlib.pyplot as plt
# from abc import ABC, abstractmethod
# from sklearn.impute import SimpleImputer 

# class HandlingMissingDataRow(ABC):
#     @abstractmethod
#     def handle(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Abstract method to handle missing data in a DataFrame."""
#         pass

# class HandlingMissingNumericalDataRow(HandlingMissingDataRow):
#     def handle(self, df: pd.DataFrame) -> pd.DataFrame:
#         # Identify numerical columns in the DataFrame
#         cols_numerical = [num for num in df.columns if df[num].dtype != 'object']
#         print("Numerical Data Columns:", cols_numerical)

#         # Drop rows with missing values in numerical columns
#         df_new = df.dropna(subset=cols_numerical)        
#         print(f"New DataFrame shape after dropping rows: {df_new.shape}, Original shape: {df.shape}")

#         # Plot histograms and PMFs for the numerical columns that remain
#         for col in cols_numerical:
#             if col in df_new.columns:
#                 self.plot_new_old(df, df_new, column=col)
#                 self.pmf(df, df_new, column=col)

#         return df_new  # Return the updated DataFrame

#     def plot_new_old(self, df_old_one, df_new_one, column):
#         fig = plt.figure()
#         ax = fig.add_subplot(111)

#         # Plot histogram for the old DataFrame (with missing values)
#         df_old_one[column].hist(bins=50, ax=ax, density=True, color='red', alpha=0.5, label='Old')
        
#         # Plot histogram for the new DataFrame (after dropping rows)
#         df_new_one[column].hist(bins=50, ax=ax, density=True, color='green', alpha=0.8, label='New')

#         # Adding labels and legend to the plot
#         ax.set_title(f'Histogram of {column}')
#         ax.set_xlabel(column)
#         ax.set_ylabel('Density')
#         ax.legend()
#         plt.show()

#     def pmf(self, df_old_one, df_new_one, column):
#         fig = plt.figure()
#         ax = fig.add_subplot(111)

#         # Plot density for the old DataFrame
#         df_old_one[column].plot.density(color='red', label='Old')
        
#         # Plot density for the new DataFrame
#         df_new_one[column].plot.density(color='green', label='New')

#         # Adding labels and legend to the PMF plot
#         ax.set_title(f'Density Plot of {column}')
#         ax.set_ylabel('Density')
#         ax.legend()
#         plt.show()

# class HandlingMissingCategoricalDataRow(HandlingMissingDataRow):
#     def __init__(self, strategy='drop'):
#         """
#         Initialize the handler with a strategy for handling missing data.
        
#         :param strategy: 'drop' to drop rows with missing values, 
#                          'impute' to fill missing values with the most frequent category.
#         """
#         if strategy not in ['drop', 'impute']:
#             raise ValueError("Invalid strategy. Choose 'drop' or 'impute'.")
#         self.strategy = strategy

#     def handle(self, df: pd.DataFrame) -> pd.DataFrame:
#         # Identify categorical columns in the DataFrame
#         df_old=df.copy()
#         cols_categorical = [col for col in df.columns if df[col].dtype == 'object']
#         print("Categorical Data Columns:", cols_categorical)

#         if self.strategy == 'impute':
#             imputer = SimpleImputer(strategy='most_frequent')
#             df[cols_categorical] = imputer.fit_transform(df[cols_categorical])
#             print("Missing values imputed with the most frequent category.")
#             df_new = df  # No need to create a new DataFrame as we are modifying in place

#         elif self.strategy == 'drop':
#             df_new = df.dropna(subset=cols_categorical)
#             print(f"New DataFrame shape after dropping rows: {df_new.shape}, Original shape: {df.shape}")

#             # Compare category percentages for each categorical column
#             for col in cols_categorical:
#                     result = self.compare_category_percentages(df_old, df_new, col)
#                     print(f"Comparison for column '{col}':\n", result)

#         return df_new  # Return the updated DataFrame

#     def compare_category_percentages(self, df_old: pd.DataFrame, df_new: pd.DataFrame, column: str) -> pd.DataFrame:
#         # Calculate percentages for the original data
#         original_counts = df_old[column].value_counts(normalize=True)

#         # Calculate percentages for the new data
#         new_counts = df_new[column].value_counts(normalize=True)

#         # Combine the results into a single DataFrame
#         result = pd.DataFrame({
#             'original': original_counts,
#             'new': new_counts
#         }).fillna(0)  # Fill NaN values with 0 for categories not present in one of the DataFrames

#         # Calculate the percentage change
#         result['percentage_change'] = ((result['new'] - result['original']) / result['original'].replace(0, 1)) * 100

#         return result

# class HandleMissingDataAnalyzerRow:
#     def __init__(self, strategy: HandlingMissingDataRow):
#         self._strategy = strategy

#     def set_strategy(self, strategy: HandlingMissingDataRow):
#         self._strategy = strategy

#     def execute_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
#         return self._strategy.handle(df)
