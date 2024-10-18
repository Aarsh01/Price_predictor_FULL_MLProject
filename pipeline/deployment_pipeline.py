from zenml import pipeline
from zenml.integrations.mlflow.steps import mlflow_model_deployer_step
from zenml_steps.dynamic_importer import dynamic_importer
from zenml_steps.prediction_service_loader import prediction_service_loader
from zenml_steps.predictor import predictor

import os

from pipeline.training_pipeline import ml_pipeline

@pipeline
# This function is responsible for deploying the model in service 
def continuous_deployment_pipeline():
    """Run a training job and deploy an MLflow model deployment."""
    # Run the training pipeline
    trained_model = ml_pipeline()  # No need for is_promoted return value anymore

    # (Re)deploy the trained model
    # In-Build function to deploy the model in ZenML 
    # It wil deploy the model
    mlflow_model_deployer_step(workers=3, deploy_decision=True, model=trained_model)

@pipeline(enable_cache=False)
def inference_pipeline():
    """Run a batch inference job with data loaded from an API."""
    # Load batch data for inference
    batch_data = dynamic_importer()


    # Load the deployed model service
    model_deployment_service = prediction_service_loader(
        pipeline_name="continuous_deployment_pipeline",
        step_name="mlflow_model_deployer_step",
    )

    # Run predictions on the batch data
    predictor(service=model_deployment_service, input_data=batch_data)

