# -*- coding: utf-8 -*-
__author__ = "yen-nan ho"

import os
import sys
import time
import logging
import datetime
import pandas as pd
from multiprocessing import Pool

from crawler import start_worker

class Crawler:
    def __init__(self, output_folder, file_path, chunk_size, file_name):
        self.mkdir(output_folder)
        self.chunk_size = chunk_size
        self.output_folder = output_folder
        self.input = pd.read_csv(file_path).head(20) # 只取前20
        self.target_ls = self.input.to_dict(orient='records')
        self.filename = file_name
        

    def check_data(self):
        print('Checking output folder!')
        if not os.path.exists(self.output_folder):
            self.mkdir(self.output_folder)
        path = self.output_folder+'/main.csv'
        if os.path.exists(path):
            df = pd.read_csv(path)
            self.target_ls = [i for i in self.target_ls if i['name'] not in df['name'].values]
            print('Read last progress in file -> {} \nHas been completed -> {} \nRemaining tasks -> {}'.format(path, len(df), len(self.target_ls)))
        else:
            print('No data in output folder!')
        time.sleep(5)

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _to_json_append(self, df, file_path):
        '''
        Load the file with
        pd.read_json(file,orient='records',lines=True)
        '''
        df.to_json('output/tmp.json', lines=True, orient='records', force_ascii=False)
        #append
        f=open('output/tmp.json', 'r')
        k=f.read()
        f.close()
        f=open(file_path, 'a', encoding='utf8')
        f.write('\n') #Prepare next data entry
        f.write(k)
        f.close()

    def output_data(self, data:list):
        data = [i for i in data if i['comment']!=None]
        df = pd.DataFrame(data)
        path = '{}/{}.csv'.format(self.output_folder, self.filename)
        usecols = df.columns.to_list()
        usecols.remove('comment')
        if os.path.exists(path):
            df[usecols].to_csv(path, mode='a', header=False, index=False)
        else:
            df[usecols].to_csv(path, index=False)

        path = '{}/{}.json'.format(self.output_folder, self.filename)
        if os.path.exists(path):
            self._to_json_append(df, path)
            # with open(path, mode = 'a+', encoding='utf-8') as f:
            #     df.head(1).append(df).to_json(f, lines=True, orient='records', force_ascii=False)
        else:
            with open(path, mode = 'w', encoding='utf-8') as f:
                df.to_json(f, lines=True, orient='records', force_ascii=False)

    def run(self, result = []):
        self.check_data()
        num = int(len(self.target_ls)/self.chunk_size) + 1
        for i in range(num):
            l = i*self.chunk_size
            r = (i+1)*self.chunk_size
            
            p = Pool() # Pool() 不放參數則默認使用電腦核的數量
            if i+1 == num-1:
                result = p.map(start_worker,self.target_ls[l:])
            else:
                result = p.map(start_worker,self.target_ls[l:r])

            p.close()
            p.join()
            
            print('Current progress: {}/{}'.format(i+1,num-1))
            if result != []:
	            try:
	                self.output_data(result)
	                print('data output success !')
	            except:
	                print('data output error')



if __name__ == "__main__":
    # Crawler = Crawler(
    #     file_path = 'data/Top50_free_game_rankings.csv',
    #     output_folder = 'output',
    #     file_name = 'Top50_free_game_rankings',
    #     chunk_size = 20
    # )
    # Crawler.run()

    # Crawler = Crawler(
    #     file_path = 'data/Top50_paid_games_rankings.csv',
    #     output_folder = 'output',
    #     file_name = 'Top50_paid_games_rankings',
    #     chunk_size = 20
    # )
    # Crawler.run()

    Crawler = Crawler(
        file_path = 'data/Top50_revenue_games_rankings.csv',
        output_folder = 'output',
        file_name = 'Top50_revenue_games_rankings',
        chunk_size = 20
    )
    Crawler.run()