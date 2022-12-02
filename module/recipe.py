# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:30:20 2022

@author: YURAN
"""

import requests
import json
import time
import pandas as pd
# from pprint import pprint

class Recipe:
    
    # 楽天レシピから検索ワードについてのレシピを取得する
    def get_recipe(self, replyText):
        # 1. 楽天レシピのレシピカテゴリ一覧を取得する
        
        res = requests.get('https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId=1069200340839550186')
        
        json_data = json.loads(res.text)
        
        parent_dict = {} # mediumカテゴリの親カテゴリの辞書
        
        df = pd.DataFrame(columns=['category1','category2','category3','categoryId','categoryName'])
        
        for category in json_data['result']['large']:
            df = df.append({'category1':category['categoryId'],'category2':"",'category3':"",'categoryId':category['categoryId'],'categoryName':category['categoryName']}, ignore_index=True)
        
        for category in json_data['result']['medium']:
            df = df.append({'category1':category['parentCategoryId'],'category2':category['categoryId'],'category3':"",'categoryId':str(category['parentCategoryId'])+"-"+str(category['categoryId']),'categoryName':category['categoryName']}, ignore_index=True)
            parent_dict[str(category['categoryId'])] = category['parentCategoryId']
        
        for category in json_data['result']['small']:
            df = df.append({'category1':parent_dict[category['parentCategoryId']],'category2':category['parentCategoryId'],'category3':category['categoryId'],'categoryId':parent_dict[category['parentCategoryId']]+"-"+str(category['parentCategoryId'])+"-"+str(category['categoryId']),'categoryName':category['categoryName']}, ignore_index=True)
        
        # 2. キーワードからカテゴリを抽出する
        df_keyword = df.query('categoryName.str.contains('+ '"' + replyText + '"' + ')', engine='python')
        
        # pprint(df_keyword)
        
        # 3. 人気レシピを取得する
        #df_recipe = pd.DataFrame(columns=['recipeId', 'recipeTitle', 'recipeUrl', 'foodImageUrl', 'recipeMaterial', 'recipeCost', 'recipeIndication', 'categoryId', 'categoryName'])
        recipesUrl = []
        recipesImg = []
        recipesTitle = []
        i = 0
        for index, row in df_keyword.iterrows():
            if i > 0: 
                break
            i += 1
            time.sleep(3) # 連続でアクセスすると先方のサーバに負荷がかかるので少し待つのがマナー

            url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1069200340839550186&categoryId='+row['categoryId']
            res = requests.get(url)

            json_data = json.loads(res.text)
            recipes = json_data['result']

            for recipe in recipes:
                #df_recipe = df_recipe.append({'recipeId':recipe['recipeId'],'recipeTitle':recipe['recipeTitle'],'recipeUrl':recipe['recipeUrl'],'foodImageUrl':recipe['foodImageUrl'],'recipeMaterial':recipe['recipeMaterial'],'recipeCost':recipe['recipeCost'],'recipeIndication':recipe['recipeIndication'],'categoryId':row['categoryId'],'categoryName':row['categoryName']}, ignore_index=True)
                recipesUrl.append(recipe['recipeUrl'])
                recipesImg.append(recipe['foodImageUrl'])
                recipesTitle.append(recipe['recipeTitle'])
        return recipesUrl, recipesImg, recipesTitle
    '''
    def create_db(self, conn, cur):
        print("テーブルは存在しません")
        # テーブルを作成
        cur.execute('CREATE TABLE Recipes(categoryId STRING, category1 INTEGER, category2 INTEGER, category3 INTEGER, categoryName STRING)')

        res = requests.get('https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId=1069200340839550186')
        json_data = json.loads(res.text)
        parent_dict = {} # mediumカテゴリの親カテゴリの辞書

        # 3.テーブルに人名データを登録する
        # 例では、personsテーブルのnameカラムに「Sato」「Suzuki」「Takahashi」というデータを登録
        for category in json_data['result']['large']:
            sql = 'INSERT INTO Recipes (categoryId, category1, categoryName) values (?,?,?)'
            data = [category['categoryId'], category['categoryId'], category['categoryName']]
            cur.execute(sql, data)
            
        for category in json_data['result']['medium']:
            cateId = str(category['parentCategoryId'])+"-"+str(category['categoryId'])
            sql = 'INSERT INTO Recipes (categoryId, category1, category2, categoryName) values (?,?,?,?)'
            data = [cateId, category['parentCategoryId'], category['categoryId'], category['categoryName']]
            cur.execute(sql, data)

            parent_dict[str(category['categoryId'])] = category['parentCategoryId']

        for category in json_data['result']['small']:
            cateId = parent_dict[category['parentCategoryId']]+"-"+str(category['parentCategoryId'])+"-"+str(category['categoryId'])
            sql = 'INSERT INTO Recipes (categoryId, category1, category2, category3, categoryName) values (?,?,?,?,?)'
            data = [cateId, parent_dict[category['parentCategoryId']], category['parentCategoryId'], category['categoryId'], category['categoryName']]
            cur.execute(sql, data)

        # 4.データベースに情報をコミット
        conn.commit()
        time.sleep(3)
'''
#recipe = Recipe()
#recipeUrl, imgUrl = recipe.get_recipe("さつまいも")
#print(recipeUrl)
#print(imgUrl)
