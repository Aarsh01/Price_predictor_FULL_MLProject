from abc import ABC, abstractmethod
import pandas as pd 
import matplotlib.pyplot as plt

class MissingDataSteps(ABC):
    def num_analyse(self, df:pd.DataFrame):
        self.num_missing_data(df)
        self.num_plot(df)


    def cat_analyse(self,df:pd.DataFrame):
        self.cat_missing_data(df)
        self.cat_plot(df)

    @abstractmethod
    def num_missing_data(self,df:pd.DataFrame):
            pass
    
    @abstractmethod
    def cat_missing_data(self,df:pd.DataFrame):
            pass
    
    @abstractmethod
    def num_plot(self,df:pd.DataFrame):
            pass 
    
    @abstractmethod
    def cat_plot(self,df:pd.DataFrame):
            pass 

class MissingValuesAnalysis(MissingDataSteps):
    

    def num_missing_data(self,df:pd.DataFrame):
        num=[col for col in df.columns if df[col].dtype!='object']

        missing_num=(df[num].isnull().sum().sort_values(ascending=False) / df.shape[0]) * 100
        print("Missing percentage of numerical Data in the DataSet:/n")
        print(missing_num)

    
    def cat_missing_data(self,df:pd.DataFrame):
        cat=[col for col in df.columns if df[col].dtype=='object']
        missing_cat=(df[cat].isnull().sum().sort_values(ascending=False) / df.shape[0]) * 100
        print("Missing percentage of Categorical Data in the DataSet:/n")
        print(missing_cat)
        
    def num_plot(self, df: pd.DataFrame):
        num = [col for col in df.columns if df[col].dtype != 'object']
        missing_num=(df[num].isnull().sum().sort_values(ascending=False) / df.shape[0]) * 100
        
        plt.figure(figsize=(10, 6))
        missing_num.plot(kind='bar', color='skyblue')
        plt.title('Missing Data Percentage in Numerical Columns')
        plt.xlabel('Numerical Columns')
        plt.ylabel('Percentage of Missing Data (%)')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()

    def cat_plot(self, df: pd.DataFrame):
        cat = [col for col in df.columns if df[col].dtype == 'object']
        missing_cat=(df[cat].isnull().sum().sort_values(ascending=False) / df.shape[0]) * 100
        
        plt.figure(figsize=(10, 6))
        missing_cat.plot(kind='bar', color='salmon')
        plt.title('Missing Data Percentage in Categorical Columns')
        plt.xlabel('Categorical Columns')
        plt.ylabel('Percentage of Missing Data (%)')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.show()
