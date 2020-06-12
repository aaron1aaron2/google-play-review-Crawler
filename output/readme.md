# Google play comment

## data_helper.py
- python 讀取 json 檔的方法

## Top20_free_game_rankings、Top20_paid_games_rankings
- 資料欄位
	- name: 遊戲名 
	- developer: 開發者 
	- star: 評分 
	- url: 主要網址
	- img_url: 遊戲圖片網址
	- developer_url: 開發者簡介網址
	- type: 遊戲類型
	- recommend_ls: 推薦列表
		- list -> [g1, g2, g3, g4, g5] 
	- describe: 遊戲描述
	- comment_num: 總評論數(包含已刪除之評論，與實際爬到的數量會有落差)
	- comment_get_num: 爬取到的評論
	- comment : 評論 (上限 10000)
		- list -> [["使用者","評分","日期","按讚數","內容","全部內容(如果太長才有可能有)"], [...], [...],...]
- `.csv`: 不包括 comment 的檔案
- `.json`: 全部檔案