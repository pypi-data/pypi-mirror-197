import lightgbm as lgb
import numpy as np
import pandas as pd
from category_encoders import OrdinalEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import neptune
from neptune.integrations.lightgbm import NeptuneCallback



class Model:

    def __init__(self, dataset):
        self.dataset = dataset
        self.model = None

        self.run = neptune.init_run(
            project='lev.taborov/FutureSalesPredict',
            api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJkNTQ5YzlhNS03NDNiLTRjYmItYmQ5Ni1lMWViOTViNjllNmIifQ==',
            capture_stdout=True,
            capture_stderr=True,
            capture_traceback=True,
            capture_hardware_metrics=True
        )
        self.callbacks = NeptuneCallback(run=self.run)

    def fit(self, X_train, y_train, X_test, y_test):
        ...

    def cross_validation(self, cv, data):
        self.val_scores = []
        result_df = pd.DataFrame()
        encoder = OrdinalEncoder()
        df = encoder.fit_transform(data.df)
        for train_idx, test_idx in cv.split(df):
            train_set = df.loc[train_idx]
            test_set = df.loc[test_idx]

            X_train = train_set.drop(columns='item_cnt_day')
            y_train = train_set['item_cnt_day']

            X_test = test_set.drop(columns='item_cnt_day')
            y_test = test_set['item_cnt_day']

            self.fit(X_train, y_train, X_test, y_test)
            y_pred = self.model.predict(X_test)

            err = mean_squared_error(y_test,
                                     y_pred,
                                     squared=False)
            print(err)
            self.val_scores.append(err)
            self.run['cross_validation/predictions'].append(np.mean(y_pred))
            self.run['cross_validation/true_values'].append(np.mean(y_test))
            self.run['cross_validation/errors'].append(err)
            analysis_df = encoder.inverse_transform(analysis_df)
            analysis_df.loc[:, [
                'date_block_num',
                'shop_id',
                'item_id',
                'item_cnt_day',
                'shop_name',
                'shop_city',
                'item_name',
                'item_cat',
                'item_sub_cat']]
            analysis_df.loc[:,'y_true'] = y_test
            analysis_df.loc[:,'y_pred'] = y_pred
            analysis_df.loc[:,'err'] = abs(y_test - y_pred)

            result_df = pd.concat([result_df, analysis_df])



        print('val error ', np.mean(self.val_scores))
        result_df.to_csv('result.csv', index=False)

    def save_model(self):
        ...

    def predict(self, test):
        ...


class LGBModel(Model):
    """_summary_
    """

    def __init__(self, dataset, callbacks=None) -> None:
        """_summary_
        """
        self.params = {
            'boosting_type': 'gbdt',
            'objective': 'regression',
            'metric': 'RMSE',
            'verbose': 0,
            'device': 'gpu',
            'early_stopping_rounds': 10,
            'bagging_fraction': 0.6793494258435211,
            'feature_fraction': 0.579095904496765,
            'bagging_freq': 5,
            'learning_rate': 0.034625641668389995,
            'max_depth': 86,
            'min_data_in_leaf': 300,
            'n_estimators': 120,
            'num_leaves': 860
        }
        super().__init__(dataset, callbacks)
        self.model = lgb.LGBMModel()
        self.model.set_params(**self.params)

    def fit(self, X_train, y_train, X_test, y_test):
        self.model.fit(X_train, y_train,
                       eval_set=(X_test, y_test),
                       categorical_feature=self.dataset.cat_cols,
                       callbacks=[self.callbacks])

    def save_model(self):
        self.model.booster_.save_model('model/LGBModel.txt')

class RFModel(Model):

    def __init__(self, dataset, callbacks=None) -> None:
        '''_summary_
        '''
        self.params = {
            'boosting_type': 'rf',
            'metric': 'RMSE',
            'objective': 'regression',
            'device': 'gpu',
            'verbose': 0,
            'early_stopping_rounds': 10,
            'bagging_fraction': 0.6793494258435211,
            'feature_fraction': 0.579095904496765,
            'bagging_freq': 5,
            'learning_rate': 0.034625641668389995,
            'max_depth': 86,
            'min_data_in_leaf': 300,
            'n_estimators': 120,
            'num_leaves': 860
        }
        super().__init__(dataset, callbacks)
        self.model = lgb.LGBMModel()
        self.model.set_params(**self.params)

    def fit(self, X_train, y_train, X_test, y_test):
        self.model.fit(X_train, y_train,
                       eval_set=(X_test, y_test),
                       categorical_feature=self.dataset.cat_cols,
                       callbacks=[self.callbacks])

class LinModel(Model):

    def __init__(self, dataset):
        super().__init__(dataset)
        self.model = LinearRegression(n_jobs=-1)

    def fit(self, X_train, y_train, X_test, y_test):
        self.model.fit(X_train, y_train)

    def predict(self, test):
        return self.model.predict(test)
