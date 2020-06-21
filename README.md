# google-play-review-Crawler
使用 python + selenium 多進程爬蟲，爬取 2020年6月初，的 googleplay 遊戲排名。

## crawler.py
### Step 1: 獲取「熱門免費遊戲前」20名的遊戲的主頁面網址

![](img/free_game_ls.png)

### Step 2: 從主頁面清單爬取下面的評論

![](img/game_info_page.png)

![](img/comment.png)

## main.py
使用多進程調用 crawler.py
