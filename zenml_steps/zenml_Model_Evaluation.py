from zenml import step
from src.model_Evaluation import ModelEvaluator, RegressionModelEvaluationStrategy
import pandas as pd
import logging
from typing import Tuple
from sklearn.pipeline import Pipeline


@step(enable_cache=False)
def model_evaluator_zenmlStep(trained_model: Pipeline, X_test: pd.DataFrame, Y_test: pd.Series) -> Tuple[dict, float]:
    # Ensure the inputs are of the correct type
    if not isinstance(X_test, pd.DataFrame):
        raise TypeError("X_test must be a pandas DataFrame.")
    if not isinstance(Y_test, pd.Series):
        raise TypeError("y_test must be a pandas Series.")
    
    logging.info("Applying the same preprocessing to the test data.")
    # Apply the preprocessing and model prediction
    X_test_processed = trained_model.named_steps["preprocessor"].transform(X_test)
    evaluator = ModelEvaluator(strategy=RegressionModelEvaluationStrategy())
    # Perform the evaluation
    evaluation_metrics = evaluator.evaluate(
        trained_model.named_steps["model"], X_test_processed, Y_test
    )
    mse = evaluation_metrics.get("Mean Squared Error", None)
    return evaluation_metrics, mse

