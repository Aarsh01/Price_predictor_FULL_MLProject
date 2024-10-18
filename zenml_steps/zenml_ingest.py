import pandas as pd
from src.data_ingest_sample_code import DataIngestionFactory
from zenml import step

@step
def data_ingestion_zenmlStep(file_path:str)->pd.DataFrame:
    file_extension='.zip'
    data_ingestor=DataIngestionFactory.get_data_ingestor(file_extension=file_extension)
    df=data_ingestor.ingestion(file_path=file_path)
    return df 
