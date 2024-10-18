import zipfile
import os
import json
from abc import ABC, abstractmethod
import pandas as pd 

class DataIngestion(ABC):
    @abstractmethod
    def ingestion(self, file_path: str, specific_file: str = None) -> pd.DataFrame:
        pass

class ZipDataIngestionFactory(DataIngestion):
    def ingestion(self, file_path: str, specific_file: str = None) -> pd.DataFrame: 
        if not file_path.endswith(".zip"):
            raise ValueError("The provided file is not a zip file")
        
        extract_dir = "/Users/aarsh/Downloads/mlops/extracted_data"
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(file_path, "r") as zip_file:
            zip_file.extractall(extract_dir)
        
        extracted_files = os.listdir(extract_dir)
        csv_files = [file for file in extracted_files if file.endswith(".csv")]

        if len(csv_files) == 0:
            raise FileNotFoundError("No CSV file found in the zip archive.")
        if len(csv_files) > 1 and specific_file is None:
            raise ValueError("Multiple CSV files found. Please specify one.")

        if specific_file:
            if specific_file not in csv_files:
                raise ValueError(f"{specific_file} is not found in the extracted files.")
            csv_file_path = os.path.join(extract_dir, specific_file)
        else:
            csv_file_path = os.path.join(extract_dir, csv_files[0])

        df = pd.read_csv(csv_file_path)
        return df

# class JsonDataIngestionFactory(DataIngestion):
#     def ingestion(self, file_path: str) -> pd.DataFrame:
#         if not file_path.endswith(".json"):
#             raise ValueError("The provided file is not a JSON file")
        
#         with open(file_path, 'r') as json_file:
#             data = json.load(json_file)
        
#         df = pd.json_normalize(data)  # Normalize semi-structured JSON data into a flat table
#         return df

class DataIngestionFactory:
    @staticmethod
    def get_data_ingestor(file_extension: str) -> DataIngestion:
        if file_extension == '.zip':
            return ZipDataIngestionFactory()
        # elif file_extension == '.json':
        #     return JsonDataIngestionFactory()
        else:
            raise ValueError(f"No ingestor is available for file extension: {file_extension}")

if __name__ == "__main__":
    # Specify the folder containing ZIP files
    folder_path = "/Users/aarsh/Downloads/mlops/data"  # Update this path to your data folder
    zip_files = [f for f in os.listdir(folder_path) if f.endswith('.zip')]

    if not zip_files:
        raise FileNotFoundError("No ZIP files found in the specified folder.")

    print("Available ZIP files:")
    for i, zip_file in enumerate(zip_files):
        print(f"{i + 1}: {zip_file}")

    # Get user input for which ZIP file to use
    choice = int(input("Select the ZIP file to ingest (enter the number): ")) - 1
    if choice < 0 or choice >= len(zip_files):
        raise ValueError("Invalid choice. Please select a valid ZIP file number.")

    selected_zip_file = os.path.join(folder_path, zip_files[choice])
    zip_file_extension = os.path.splitext(selected_zip_file)[1]
    zip_data_ingestor = DataIngestionFactory.get_data_ingestor(file_extension=zip_file_extension)
    
    # Specify the CSV file you want to read
    specific_csv_file = input("Enter the name of the CSV file to extract (or press Enter to use the first one): ")
    
    zip_df = zip_data_ingestor.ingestion(selected_zip_file, specific_file=specific_csv_file or None)
    print(zip_df.head(5))