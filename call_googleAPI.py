#encoding:utf-8
RED     = '\033[31m'
CYAN    = '\033[36m'
GREEN   = '\033[92m'
ENDC    = '\033[0m'
import urllib
import urllib.request
import json
import sys
import pandas as pd


def scrape_serps(phrase,maxrank,df_api,api_counter,j,try_cnt):
    try:
        #api_counter
        url_list = []
        a = list(df_api["log"])
        cnt=0
        while(cnt<maxrank):
            if api_counter < 100:
                print("[page_num]-->"+str(cnt))
                API_KEY = df_api["API_KEY"][j]
                ENGINE_ID = df_api["API_ID"][j]
                print (CYAN+"[api_cnt]-->"+GREEN+str(api_counter)+ENDC)
                print ("[API_KEY]-->"+str(API_KEY))
                print ("[API_NUM]-->"+str(j))
                print ("------------")
                req_url = "https://www.googleapis.com/customsearch/v1?hl=ja&key="+API_KEY+"&cx="+ENGINE_ID+"&alt=json&q="+ phrase +"&start="+ str(cnt+1)
                headers={'User-Agent': 'Mozilla/5.0'}
                headers = {"User-Agent": 'Mozilla /5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B5110e Safari/601.1'}
                # 以下５行をコメントアウトすればリクセストなし
                req = urllib.request.Request(req_url,headers=headers)
                res = urllib.request.urlopen(req)
                dump = json.loads(res.read())
                for p in range(len(dump["items"])):
                    url_list.append(dump['items'][p]['link'])
                api_counter = api_counter + 1
                cnt = cnt +1
            else:
                j = j + 1
                api_counter = 0
            exit()
        df_api["log"] = a
        return url_list,df_api,api_counter,j

    # if 503 or 403error returned (when the http server do not temporary accept your request)
    except Exception as e:
        try_cnt += 1
        if try_cnt <= 2:
            scrape_serps(key_,page,df_api,api_counter,j)
        else:
            print ('server error occured')













def main():
    api_counter = 0
    j = 0
    page = input("how many page do you want?(1or2)")
    page = int(page)
    df = pd.read_csv("suggest.csv",header=None)
    df.columns=["suggest"]
    sg = list(df["suggest"])
    urls = []
    urls_ = []
    sgs = []
    df_api = pd.read_csv("api.csv")
    ct = 0
    for key in sg:
        ct = ct + 1
        try_cnt = 0
        print ("")
        print (GREEN+str(ct)+ENDC)
        print("====================================")
        print(key)
        key_ = urllib.parse.quote(key)
        url_list,df_api,api_counter,j = scrape_serps(key_,page,df_api,api_counter,j,try_cnt)
        urls_.extend(url_list)
        for i in range(page*10):
            sgs.append(key)
        urls += [url_list]
    #df_api.to_csv("api.csv")
    urls = pd.DataFrame(urls)
    df = pd.concat([df,urls],axis=1)
    df.to_csv("urls.csv")
    df_ = pd.concat([pd.Series(urls_),pd.Series(sgs)],axis=1)
    df_.columns = ["url","suggest"]
    df_.to_csv("sg_urls.csv")


main()
