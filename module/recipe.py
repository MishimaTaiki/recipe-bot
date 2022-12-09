# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:30:20 2022

@author: YURAN
"""

import requests
import json
import time
import sqlite3
# import pandas as pd
# from pprint import pprint

class Recipe:

    # 楽天レシピから検索ワードについてのレシピを取得する
    def get_recipe(self, replyText):
        # 楽天レシピのレシピカテゴリ一覧を取得する
        
        # カレントディレクトリにrecipe.dbがなければ、作成します。
        # すでにTEST.dbが作成されていれば、recipe.dbに接続します。
        dbname = './recipe.db'
        conn = sqlite3.connect(dbname)

        # 2.sqliteを操作するカーソルオブジェクトを作成
        cur = conn.cursor()

        # 3.テーブルのCreate文を実行(例ではpersonsテーブルを作成)
        # テーブルが存在するか
        cur.execute("SELECT COUNT(*) FROM sqlite_master"
                "    WHERE TYPE = 'table' AND name = 'Recipes'")
        row = cur.fetchone() # SQL文の実行結果をtupleで得る
        if row[0] == 0:
            self.create_db(conn, cur)

        # データ検索
        cur.execute("SELECT categoryId FROM Recipes WHERE categoryName=" + "'" + replyText + "'")

        # 取得したデータはカーソルの中に入る
        recipesUrl = []
        recipesImg = []
        recipesTitle = []
        i = 0
        for row in cur:
            # 終了判定
            if i > 0: 
                break
            i += 1
            url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1069200340839550186&categoryId='+ f"{row[0]}"
            res = requests.get(url)

            json_data = json.loads(res.text)
            recipes = json_data['result']

            for recipe in recipes:
                #df_recipe = df_recipe.append({'recipeId':recipe['recipeId'],'recipeTitle':recipe['recipeTitle'],'recipeUrl':recipe['recipeUrl'],'foodImageUrl':recipe['foodImageUrl'],'recipeMaterial':recipe['recipeMaterial'],'recipeCost':recipe['recipeCost'],'recipeIndication':recipe['recipeIndication'],'categoryId':row['categoryId'],'categoryName':row['categoryName']}, ignore_index=True)
                recipesUrl.append(recipe['recipeUrl'])
                recipesImg.append(recipe['foodImageUrl'])
                recipesTitle.append(recipe['recipeTitle'])

        # 5.データベースの接続を切断
        cur.close()
        conn.close()

        return recipesUrl, recipesImg, recipesTitle

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

#recipe = Recipe()
#url,img,title = recipe.get_recipe("さつまいも")
#print(url)
#print(img)
#print(title)