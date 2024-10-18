from zenml import step
from src.handle_missing_value import MissingValueHandler, DropMissingValuesStrategy, ImputeMissingStrategy
import pandas as pd

@step
def handleMissingData_zenmlStep(df: pd.DataFrame, st: str = 'mean', ax: int = 0, th = None, fl = None) -> pd.DataFrame:
    """
    Handles missing data in the provided DataFrame based on the specified strategy.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing missing values.
    st (str): The strategy to use for handling missing values ('drop', 'mean', 'median', 'mode', 'most_frequent', 'constant').
    ax (int): Axis to drop values along (0 for rows, 1 for columns).
    th (int): Threshold for dropping values (only used if st is 'drop').
    fl (any): Fill value for imputation (only used if st is 'constant').

    Returns:
    pd.DataFrame: The cleaned DataFrame with missing values handled.
    """
    if st == 'drop':
        if th is None:
            raise ValueError("Threshold (th) must be provided when using 'drop' strategy.")
        handler = MissingValueHandler(strategy=DropMissingValuesStrategy(axis=ax, threshold=th))
    elif st in ['mean', 'median', 'mode', 'most_frequent', 'constant']:
        handler = MissingValueHandler(strategy=ImputeMissingStrategy(strategy=st, fill_with=fl))
    else:
        raise ValueError(f"Unknown strategy: {st}. Must be one of 'drop', 'mean', 'median', 'mode', 'most_frequent', 'constant'.")

    df_cleaned = handler.excute(df)
    return df_cleaned
