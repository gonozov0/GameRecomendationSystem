from os import path
import numpy as np
import pandas as pd
# from scipy.sparse import csr_matrix
# from surprise import SVD
# from surprise import Dataset, Reader
# from surprise import accuracy
# from surprise.model_selection import train_test_split
# from surprise.model_selection import GridSearchCV
# from surprise.model_selection import cross_validate


class Model:
    """Класс для предсказания рекомендаций видеоигр по пользователю.  
    Включает в себя 2 основных метода:
    * predict - выдать рекомендации видеоигр по пользователю
    * train - переобучить модель
    """
    best_params = {
        'n_factors': 100,
        'n_epochs': 100,
        'lr_all': 0.02,
        'reg_all': 0.01
    }
    prediction_data_path = path.join('data', 'predictions.csv')
    training_data_path = path.join('data', 'video_games.csv')

    def __init__(self):
        # считываем результаты предсказаний моделью для всех пар (пользователь, товар) из файла
        self.df_pred = pd.read_csv(self.prediction_data_path)

    def predict(self, user_id:str=None, best_k:int=1) -> str: 
        """Метод возвращает best_k рекомендаций товаров (видеоигр) для user_id 
        Если пользователь не был передан, возвращает 10 случайных пользователей и рекомендацию для них
        Аргументы:
        * user_id - ИД пользователя, для которого необходимо получить рекомендации
        * best_k - количество лучших товаров (видеоигр), которые будут возвращены для данного пользователя.
        По умолчанию - 1
        """
        if user_id is None:
            return self.df_pred.groupby('user') \
                .rating \
                .agg(['max', 'idxmax']) \
                .merge(self.df_pred, left_on='idxmax', right_index=True)[['item', 'max']] \
                .sample(10) \
                .rename({'max':'rating'}, axis=1) \
                .to_json(orient='index')
        else:
            return self.df_pred[self.df_pred['user'] == user_id] \
                .sort_values('rating', ascending=False)[['item', 'rating']] \
                .head(best_k) \
                .to_json(orient='records')