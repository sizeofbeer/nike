import json, pymysql
import asyncio
import aiohttp
async def crawl(url):
    data = None
    async with aiohttp.ClientSession() as s:
        async with s.post(url) as r:
            if r.status != 200:
                raise Exception("Http Status Code is {}".format(r.status))
            data = json.loads(await r.text())['msg']
    return data

async def nike_task(task_types, task_ids):
    url = "http://192.168.15.77:1887/{0}/{1}"
    tasks = [crawl(url.format(tp, id)) for i, tp in enumerate(task_types) for j, id in enumerate(task_ids) if i == j]
    for r in asyncio.as_completed(tasks):
        item = await r
        print("任务编号: " + item + " 已完成")
import time
if __name__ == "__main__":
    while True:
        print("start")
        # 建立数据库连接
        conn = pymysql.connect(host='192.168.15.77',user='root',password='123456',db='nike',charset='utf8')
        # 创建游标和sql语句
        cur = conn.cursor()
        sql = "select * from nike_task;"
        # 执行SQL
        total_num = cur.execute(sql)
        result = cur.fetchall()
        task_ids, task_types= [], []
        for task in result:
            if task[4]:
                continue
            if task[3] == '100':
                continue
            if task[1] == "NIke OB 账单":
                task_types.append("Nike_Deal_Ob_Bill")
                task_ids.append(task[0])
            else:
                continue
        ioloop = asyncio.get_event_loop()
        ioloop.run_until_complete(nike_task(task_types, task_ids))
        conn.close()
        time.sleep(120)
        print("next")
