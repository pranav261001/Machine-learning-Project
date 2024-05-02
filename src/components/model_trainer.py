import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer(ModelTrainerConfig):

    def initiate_model_training(self, train_arr, test_arr):
        try:
            logging.info("splitting the training & testing data ")
            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models = {
                "Random Forest" : RandomForestRegressor(),
                "Decision tree" : DecisionTreeRegressor(),
                "Gradient Boosting" : GradientBoostingRegressor(),
                "KNN Regressor" : KNeighborsRegressor(),
                "XGboost": XGBRegressor(),
                "Adaboost": AdaBoostRegressor(),
                "Linear Regression": LinearRegression(),
                "cat boost": CatBoostRegressor(verbose=False)

            }

            # intended to be a dictionary as evaluate model func return a dictionary

            model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models)

            best_model_score = max(sorted(model_report.values())) # gets the max r2 score

            best_model_name = list(model_report.keys())[   # creates list of model names
                list(model_report.values()).index(best_model_score)  #providing the index of best r2 score
                                                        ]
            
            best_model = models[best_model_name]
            # holds the actual machine learning model object that achieved the highest R-squared score

            if best_model_score < 0.6:
                raise CustomException("No Best Model Present")
            else:
                logging.info("Best Model Found ")

            save_object(
                file_path=self.trained_model_file_path,
                obj= best_model
            )

            prediction = best_model.predict(X_test)
            Rsquare = r2_score(y_test, prediction)

            return f"Best performing model: {best_model_name} and R-square: {Rsquare}"

        except Exception as e :
            raise CustomException(e, sys)
