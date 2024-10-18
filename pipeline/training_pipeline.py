from zenml import Model, pipeline, step
from zenml_steps.zenml_ingest import data_ingestion_zenmlStep
from zenml_steps.zenml_missing_value import handleMissingData_zenmlStep
from zenml_steps.zenml_featureEngineering import feature_engineering_step
from zenml_steps.zenml_OutlierDetection import outlier_detection_step
from zenml_steps.zenml_data_spliting import data_split_zenmlStep
from zenml_steps.zenml_modelBuilding import model_building_step
from zenml_steps.zenml_Model_Evaluation import model_evaluator_zenmlStep

@pipeline(
    model=Model(
        name="price_predictor"
    ),
)
def ml_pipeline():
    # # Taking user input for the pipeline parameters
    # data_path = input("Enter the path to the dataset (zip file): ")
    # strategy_handleMissing = input("Enter the strategy for handling missing values (drop, mean, median, mode, most_frequent, constant): ")
    # axis = int(input("Enter the axis for dropping values (0 for rows, 1 for columns): "))
    
    # threshold = None
    # if strategy_handleMissing == 'drop':
    #     threshold = int(input("Enter the threshold for dropping values (only used if strategy is 'drop'): "))
    
    # colType_fE = input("Enter the column type (a. 'Numerical' or b. 'Categorical'): ")
    # strategy_fE = input("Enter the method (a. 'MinMax', b. 'StandardScaler', c. 'OHC'): ")
    # columns_fE_input = input("Enter the columns that want feature transformation (comma-separated): ")
    # columns_fE = [col.strip() for col in columns_fE_input.split(',')]  # Convert input to a list




    # Data ingestion Step
    raw_data = data_ingestion_zenmlStep(
            file_path="/Users/aarsh/Downloads/mlops/data/archive.zip"
        )


    # Handling Missing Values Step
    filtered_data = handleMissingData_zenmlStep(raw_data)
    
    # Feature Engineering Step
    engineered_data = feature_engineering_step(
        filtered_data, strategy="log", features=["Gr Liv Area", "SalePrice"]
    )

    # Outliers Handling 
    clean_data = outlier_detection_step(engineered_data, column_name='SalePrice')

    # Data Splitting Step
    X_train, X_test, Y_train, Y_test = data_split_zenmlStep(clean_data,'SalePrice')

    # Model Building Step
    model = model_building_step(X_train=X_train, y_train=Y_train)

    # Model Evaluation Step
    evaluation_metrics, mse = model_evaluator_zenmlStep(model, X_test,Y_test)

    
    return model



if __name__ == "__main__":
   

    # Run the pipeline with user inputs
    run = ml_pipeline()
    print("Pipeline executed successfully. Cleaned data is ready for further processing.")
