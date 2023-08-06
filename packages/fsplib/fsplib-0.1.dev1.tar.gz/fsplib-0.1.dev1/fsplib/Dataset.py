import re

import numpy as np
import pandas as pd


def name_fix(input: str) -> str:
    return re.sub('[!,*/]', '', input).lower()


class Dataset():
    """Dataset class to handle training/testing data
    """

    TARGET = 'item_cnt_day'

    def __init__(self, data=None) -> None:
        self.df = None
        self.cat_cols = []
        self.encoder = None

    def read_file(self, datapath: str) -> None:
        """Reads data from .csv file and performs ETL actions

        Parameters
        ----------
        datapath : str
            path to .csv file
        """

        self.datapath = datapath

        df = pd.read_csv(self.datapath + 'sales_train.csv')

        test = pd.read_csv(self.datapath + 'test.csv').drop(columns='ID')
        test['date_block_num'] = 34
        self.df = pd.concat([df, test])

        self.shops = pd.read_csv(self.datapath + 'shops.csv')
        self.items = pd.read_csv(self.datapath + 'items.csv')
        self.item_categories = pd.read_csv(
            self.datapath + 'item_categories.csv')

        # 0. etl
        # sells
        self.df.drop_duplicates(inplace=True)
        self.df.loc[1163158, 'item_cnt_day'] = 522
        self.df.loc[1163158, 'item_price'] /= 522
        self.df.loc[1163158, 'item_id'] = 6065

        outliers = [484683, 2909818]
        self.df.drop(outliers, inplace=True)
        self.df = self.df[self.df['item_cnt_day'] >= 0]
        self.df = self.df[self.df['item_price'] >= 0]

        # categories
        drop_cats = [8, 80]
        to_drop = self.item_categories[self.item_categories['item_category_id'].isin(
            drop_cats)].index
        self.item_categories.drop(to_drop, inplace=True)

        self.item_categories['item_category_name'] = self.item_categories['item_category_name'].apply(
            lambda x: x.lower().split(' - ')
        )
        self.item_categories['item_cat'] = self.item_categories['item_category_name'].apply(
            lambda x: x[0]
        )
        self.item_categories['item_sub_cat'] = self.item_categories['item_category_name'].apply(
            lambda x: x[1] if len(x) > 1 else '')

        extra_cats = [26, 27, 28, 29, 30, 31]
        extra_cats = self.item_categories[self.item_categories['item_category_id'].isin(
            extra_cats)]
        self.item_categories.loc[extra_cats.index, 'item_cat'] = extra_cats['item_cat'].transform(
            lambda x: x.split()[0])
        self.item_categories.loc[extra_cats.index, 'item_sub_cat'] = extra_cats['item_cat'].transform(
            lambda x: x.split()[1]) + ' ' + extra_cats['item_sub_cat']

        # items
        self.items['item_name'] = self.items['item_name'].transform(name_fix)

        # shops
        self.shops['shop_name'] = self.shops['shop_name'].transform(name_fix)
        self.shops['shop_city'] = self.shops['shop_name'].apply(
            lambda x: x.split()[0])
        fix_shops = {
            0: 57,
            1: 58,
            11: 10,
            # 23: 24  # ???
        }
        for k, v in fix_shops.items():
            self.shops.loc[self.shops['shop_id'] == k, 'shop_id'] = v
            self.df.loc[self.df['shop_id'] == k, 'shop_id'] = v

        self.shops.drop_duplicates(
            subset='shop_id',
            inplace=True
        )

    def transform(self):
        self.df = self.df.groupby(
            by=[
                'date_block_num',
                'shop_id',
                'item_id'
            ]
        ).agg(
            {
                'item_cnt_day': 'sum',
                'item_price': 'mean' #TODO mean or median?
            }
        ).reset_index()

        self.df = self.df.merge(
            self.shops,
            on='shop_id',
            how='left'
        ).merge(
            self.items,
            on='item_id',
            how='left'
        ).merge(
            self.item_categories,
            on='item_category_id',
            how='left'
        )

        self.cat_cols.extend([
            'shop_name',
            'shop_city',
            'item_cat',
            'item_sub_cat',
        ])

        self.df = self.df.drop(
            columns=[
                # 'shop_id',
                # 'item_id',
                # 'item_category_id',
                'item_category_name'
                ]
        )


        self.df['item_cnt_day'] = self.df['item_cnt_day']
        self.df['item_price'] = self.df['item_cnt_day']

        def add_group_feature(df, group, col, agg, feature_name):
            feature = df.groupby(by=group).agg({col: agg})
            feature.columns = [feature_name]
            feature[feature_name] = feature[feature_name]
            feature.reset_index(inplace=True)
            return pd.merge(df, feature, how='left', on=group)

        def add_lag_feature(df, lags, cols):
            for col in cols:
                print(col)
                tmp = df[["date_block_num", "shop_id","item_id", col]]
                for i in lags:
                    shifted = tmp.copy()
                    shifted.columns = ["date_block_num", "shop_id", "item_id", col + "_lag_"+str(i)]
                    shifted.date_block_num = shifted.date_block_num + i
                    df = pd.merge(df, shifted, on=['date_block_num','shop_id','item_id'], how='left')
                del tmp
            return df.fillna(0)


        lags = [1,2,3,6,12]

        self.df.loc[:, 'item_revenue'] = self.df['item_cnt_day'] * self.df['item_price']

        self.df = add_lag_feature(self.df, lags, ['item_cnt_day', 'item_price', 'item_revenue'])

        self.df = add_group_feature(self.df, ['date_block_num'], 'item_cnt_day', 'mean', 'avg_month_cnt')
        self.df = add_lag_feature(self.df, lags, ['avg_month_cnt'])

        self.df = add_group_feature(self.df, ['date_block_num', 'item_id'], 'item_cnt_day', 'mean', 'avg_month_item_cnt')
        self.df = add_group_feature(self.df, ['date_block_num', 'item_id'], 'item_price', 'mean', 'avg_month_item_price')
        self.df = add_lag_feature(self.df, lags, ['avg_month_item_cnt', 'avg_month_item_price'])

        self.df = add_group_feature(self.df, ['date_block_num', 'shop_id'], 'item_cnt_day', 'mean', 'avg_month_shop_cnt')
        self.df = add_group_feature(self.df, ['date_block_num', 'shop_id'], 'item_price', 'mean', 'avg_month_shop_price')
        self.df = add_lag_feature(self.df, lags, ['avg_month_shop_cnt', 'avg_month_shop_price'])

        self.df = add_group_feature(self.df, ['date_block_num', 'item_cat'], 'item_cnt_day', 'mean', 'avg_month_cat_cnt')
        self.df = add_group_feature(self.df, ['date_block_num', 'item_cat'], 'item_price', 'mean', 'avg_month_cat_price')
        self.df = add_lag_feature(self.df, lags, ['avg_month_cat_cnt', 'avg_month_cat_price'])

        self.df = add_group_feature(self.df, ['date_block_num', 'item_sub_cat'], 'item_cnt_day', 'mean', 'avg_month_sub_cat_cnt')
        self.df = add_lag_feature(self.df, lags, ['avg_month_sub_cat_cnt'])

        self.df = add_group_feature(self.df, ['date_block_num', 'shop_id', 'item_cat'], 'item_cnt_day', 'mean', 'avg_month_shop_cat_cnt')
        self.df = add_lag_feature(self.df, lags, ['avg_month_shop_cat_cnt'])

        self.df = add_group_feature(self.df, ['date_block_num', 'shop_id', 'item_sub_cat'], 'item_cnt_day', 'mean', 'avg_month_shop_sub_cat_cnt')
        self.df = add_lag_feature(self.df, lags, ['avg_month_shop_sub_cat_cnt'])

        self.df = add_group_feature(self.df, ['date_block_num', 'shop_city', 'item_id'], 'item_cnt_day', 'mean', 'avg_month_city_item_cnt')
        self.df = add_lag_feature(self.df, lags, ['avg_month_city_item_cnt'])

        self.df = add_group_feature(self.df, ['date_block_num', 'shop_city', 'item_cat'], 'item_cnt_day', 'mean', 'avg_month_city_cat_cnt')
        self.df = add_lag_feature(self.df, lags, ['avg_month_city_cat_cnt'])

        self.df = add_group_feature(self.df, ['date_block_num', 'shop_city', 'item_sub_cat'], 'item_cnt_day', 'mean', 'avg_month_city_sub_cat_cnt')
        self.df = add_lag_feature(self.df, lags, ['avg_month_city_sub_cat_cnt'])

        self.df.loc[:, 'rel_cnt_month'] = self.df['item_cnt_day']/(self.df['avg_month_item_cnt'] + 1e-5)
        self.df.loc[:, 'rel_price_month'] = self.df['item_price']/(self.df['avg_month_item_price'] + 1e-5)
        self.df = add_lag_feature(self.df, lags, ['rel_cnt_month', 'rel_price_month'])

        self.df = self.df[self.df['date_block_num'] > 12]
        self.df = self.df.drop(columns=['item_price',
                                        'avg_month_cnt',
                                        'item_revenue',
                                        'avg_month_item_cnt',
                                        'avg_month_item_price',
                                        'avg_month_shop_cnt',
                                        'avg_month_shop_price',
                                        'avg_month_cat_cnt',
                                        'avg_month_cat_price',
                                        'avg_month_sub_cat_cnt',
                                        'avg_month_shop_cat_cnt',
                                        'avg_month_shop_sub_cat_cnt',
                                        'avg_month_city_item_cnt',
                                        'avg_month_city_cat_cnt',
                                        'avg_month_city_sub_cat_cnt',
                                        'rel_cnt_month',
                                        'rel_price_month'
                                        ])

        self.df.loc[:, 'dateX'] = np.cos(
            self.df.loc[:, 'date_block_num'] / 12 * 2 * np.pi)
        self.df.loc[:, 'dateY'] = np.sin(
            self.df.loc[:, 'date_block_num'] / 12 * 2 * np.pi)

    def getX(self):
        return self.df[self.df['date_block_num'] < 34].drop(
            columns=['item_cnt_day']
        )

    def getY(self):
        return self.df.loc[self.df['date_block_num'] < 34, 'item_cnt_day']

    def create_test(self):
        """Generates dataset with features to create submission
        """

        return self.df[self.df['date_block_num'] == 34].drop(
            columns=['item_cnt_day']
        )