# import&init
from fsplib import Dataset, Model, ExpandingWindowCV
import pandas as pd
import numpy as np
from boruta import BorutaPy
import shap
import neptune.new as neptune
from neptune.new.integrations.lightgbm import NeptuneCallback


def execute(datapath: str):

    DATAPATH = datapath

    # init neptune run
    run = neptune.init_run(
        project='lev.taborov/FutureSalesPredict',
        api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJkNTQ5YzlhNS03NDNiLTRjYmItYmQ5Ni1lMWViOTViNjllNmIifQ=='
    )
    neptune_callback = NeptuneCallback(run=run)

    data = Dataset.Dataset()
    data.read_file(DATAPATH)
    data.transform()
    # data.df.to_csv('data.csv', index=False)

    model = Model.LGBModel(data, [neptune_callback])

    # boruta feature selection
    X = data.getX().values
    y = data.getY().values

    from neptune.new.types import File
    feat_selector = BorutaPy(model.model)
    feat_selector.fit(X, y)

    run['boruta_result'].upload(File.as_html(
        pd.DataFrame({
            'col': data.df.drop(columns='item_cnt_day').columns,
            'ranks': feat_selector.ranking_,
            'support': (feat_selector.support_ | feat_selector.support_weak_)
        }).sort_values(by='ranks', ascending=False)
    ))

    columns = data.df.drop(columns='item_cnt_day').columns
    columns = columns[~(feat_selector.support_ | feat_selector.support_weak_)]

    data.df = data.df.drop(columns=columns)
    run['data_cols'] = data.df.columns.tolist()

    # hypeopt parameters tuning
    from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
    from hyperopt.pyll.base import scope

    cv = ExpandingWindowCV.ExpandingWindowCV(2)

    def fn(params):
        model = Model.LGBModel(data, [neptune_callback])
        model.model.set_params(**params)

        model.train(cv)

        return {
            'loss': np.mean(model.val_scores),
            'params': params,
            'status': STATUS_OK
        }

    space = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'device': 'cpu',
        'verbose': 0,
        'early_stopping_rounds': 10,
        'num_leaves': scope.int(hp.quniform('num_leaves', 10, 1000, 10)),
        'max_depth': scope.int(hp.quniform('max_depth', 1, 100, 1)),
        'learning_rate': hp.uniform('learning_rate', 0.01, 0.9),
        'n_estimators': scope.int(hp.quniform('n_estimators', 10, 1000, 10)),
        'min_data_in_leaf': scope.int(hp.quniform('min_data_in_leaf', 100, 10000, 100)),
        'feature_fraction': hp.uniform('feature_fraction', 0.1, 1.0),
        'bagging_fraction': hp.uniform('bagging_fraction', 0.1, 0.9),
        'bagging_freq': 5
    }

    trials = Trials()
    best = fmin(
        fn=fn,
        space=space,
        algo=tpe.suggest,
        max_evals=100,
        trials=trials,
        show_progressbar=True
    )
    run['params/best'] = str(best)

    # train model
    model = Model.LGBModel(data, [neptune_callback])
    model.model.set_params(**best)
    model.train(cv)

    model.model.booster_.save_model('LGBModel.txt')
    run['model/model'].upload('LGBModel.txt')

    # shap explainability
    explainer = shap.TreeExplainer(model.model.booster_)
    # test = data.create_test()
    test = data.df[data.df['date_block_num'] == 33]
    shap_values = explainer(test)
    run['shap_vals'] = shap_values
    shap.waterfall_plot(shap_values[0])

    # create submission file
    result = model.model.predict(data.create_test())
    result = result.clip(0, 20)

    id = pd.read_csv(DATAPATH + 'test.csv')['ID']
    submission = pd.DataFrame(
        {
            'ID': id,
            'item_cnt_month': result
        }
    )
    submission.to_csv('submission.csv', index=False)
    run['submission'].upload('submission.csv')

    run.stop()
