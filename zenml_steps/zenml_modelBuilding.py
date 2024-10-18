import logging
from typing import Annotated

import mlflow
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from zenml import ArtifactConfig, step
from zenml.client import Client
from zenml import Model

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set the stack and experiment tracker names
stack_name = "quickstart_stack"
experiment_tracker_name = "first_tracker"

# Get the active client and activate the specified stack
client = Client()
client.activate_stack(stack_name)  # Activate the specified stack

# Get the active experiment tracker from the active stack
experiment_tracker = client.active_stack.experiment_tracker

# Define the model metadata
model = Model(
    name="prices_predictor",
    version=None,
    license="Apache 2.0",
    description="Price prediction model for houses.",
)

@step(enable_cache=False, experiment_tracker=experiment_tracker_name, model=model)
def model_building_step(X_train: pd.DataFrame, y_train: pd.Series) -> Annotated[Pipeline, ArtifactConfig(name="sklearn_pipeline", is_model_artifact=True)]:
    """
    Builds and trains a Linear Regression model using scikit-learn wrapped in a pipeline.

    Parameters:
    X_train (pd.DataFrame): The training data features.
    y_train (pd.Series): The training data labels/target.

    Returns:
    Pipeline: The trained scikit-learn pipeline including preprocessing and the Linear Regression model.
    """
    # Input validation
    if not isinstance(X_train, pd.DataFrame):
        raise TypeError("X_train must be a pandas DataFrame.")
    if not isinstance(y_train, pd.Series):
        raise TypeError("y_train must be a pandas Series.")

    # Identify categorical and numerical columns
    categorical_cols = X_train.select_dtypes(include=["object", "category"]).columns.tolist()
    numerical_cols = X_train.select_dtypes(exclude=["object", "category"]).columns.tolist()

    logging.info(f"Categorical columns: {categorical_cols}")
    logging.info(f"Numerical columns: {numerical_cols}")

    # Define preprocessing for numerical and categorical features
    numerical_transformer = SimpleImputer(strategy="mean")
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    # Bundle preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_transformer, numerical_cols),
            ("cat", categorical_transformer, categorical_cols),
        ]
    )

    # Define the model training pipeline
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", LinearRegression())
    ])

    # Start an MLflow run to log the model training process
    mlflow.sklearn.autolog()  # Enable autologging before starting the run
    if not mlflow.active_run():
        mlflow.start_run()  # Start a new MLflow run if there isn't one active

    try:
        logging.info("Building and training the Linear Regression model.")
        pipeline.fit(X_train, y_train)
        logging.info("Model training completed.")
# 
        # # Log the expected columns
        # onehot_encoder = pipeline.named_steps["preprocessor"].transformers_[1][1].named_steps["onehot"]
        # expected_columns = numerical_cols + list(onehot_encoder.get_feature_names_out(categorical_cols))
        # logging.info(f"Model expects the following columns: {expected_columns}")

    except Exception as e:
        logging.error(f"Error during model training: {e}")
        raise e

    finally:
        # End the MLflow run
        mlflow.end_run()

    return pipeline
