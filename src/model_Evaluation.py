import logging
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from sklearn.base import RegressorMixin
from sklearn.metrics import mean_absolute_error, r2_score

# # Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ModelEvaluationStrategy(ABC):
    @abstractmethod
    def evalutionStrategy(self, model:'RegressorMixin', X_test:pd.DataFrame, Y_test:pd.Series)->dict:
        pass

class RegressionModelEvaluationStrategy(ModelEvaluationStrategy):
    def evalutionStrategy(self, model, X_test, Y_test)->dict:

        y_pred=model.predict(X_test)

        logging.info("Calculating evaluation metrics.")
        mse = mean_absolute_error(Y_test, y_pred)
        r2 = r2_score(Y_test, y_pred)
        metrics = {"Mean Squared Error": mse, "R-Squared": r2}

        logging.info(f"Model Evaluation Metrics: {metrics}")
        return metrics
        
# Context Class for Model Evaluation
class ModelEvaluator:
    def __init__(self, strategy: ModelEvaluationStrategy):
        """
        Initializes the ModelEvaluator with a specific model evaluation strategy.

        Parameters:
        strategy (ModelEvaluationStrategy): The strategy to be used for model evaluation.
        """
        self._strategy = strategy

    def set_strategy(self, strategy: ModelEvaluationStrategy):
        """
        Sets a new strategy for the ModelEvaluator.

        Parameters:
        strategy (ModelEvaluationStrategy): The new strategy to be used for model evaluation.
        """
        logging.info("Switching model evaluation strategy.")
        self._strategy = strategy
    
    def evaluate(self, model: RegressorMixin, X_test: pd.DataFrame, Y_test: pd.Series) -> dict:
        logging.info("Evaluating the model using the selected strategy./n")
        return self._strategy.evalutionStrategy(model,X_test,Y_test)