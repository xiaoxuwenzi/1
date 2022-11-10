#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64

class Spider(Spider):  # 元类 默认的元类 type
    def getName(self):
        return "哔哩哔哩"
    def init(self,extend=""):
        print("============{0}============".format(extend))
        pass
    def isVideoFormat(self,url):
        pass
    def manualVideoCheck(self):
        pass
    def homeContent(self,filter):
        result = {}
        cateManual = {
            "动态":"动态",
            "热门":"热门",
            "排行榜":"排行榜",
            "频道":"频道",
            "舞蹈":"舞蹈",
            "相声小品":"相声小品",
            "电影解说":"电影解说",
            "昆虫":"昆虫",
            "动物世界":"动物世界",
            "纪录片":"纪录片",
            "搞笑":"搞笑",
            "演唱会":"演唱会"
        }
        classes = []
        for k in cateManual:
            classes.append({
                'type_name':k,
                'type_id':cateManual[k]
            })
        result['class'] = classes
        if(filter):
            result['filters'] = self.config['filter']
        return result
    def homeVideoContent(self):
        result = {
            'list':[]
        }
        return result
    cookies = ''
    def getCookie(self):
        import requests
        import http.cookies
        ### 这里加cookie
        raw_cookie_line = "l=v; buvid3=2CF2485B-2D82-BD62-85A3-695AAB5FA6B063651infoc; rpdid=|(J|)|)Jklul0J'uYlmY|kkYR; fingerprint=c199b54d522ea78467e5655877b69bdd; buvid_fp=2CF2485B-2D82-BD62-85A3-695AAB5FA6B063651infoc; buvid_fp_plain=undefined; SESSDATA=3e7d5e73%2C1677038443%2C6fe60%2A81; bili_jct=9b714c8b6002e40f04f5c93efda8a983; DedeUserID=7168543; DedeUserID__ckMd5=b85817f0ee6a28c2; CURRENT_QUALITY=80; sid=75jxjtcr; i-wanna-go-back=-1; b_ut=5; nostalgia_conf=-1; CURRENT_BLACKGAP=0; b_nut=100; LIVE_BUVID=AUTO5816633815327224; CURRENT_FNVAL=4048; blackside_state=0; bp_video_offset_7168543=726518500256907300; innersign=0"
        simple_cookie = http.cookies.SimpleCookie(raw_cookie_line)
        cookie_jar = requests.cookies.RequestsCookieJar()
        cookie_jar.update(simple_cookie)
        return cookie_jar
    def get_dynamic(self,pg):
        result = {}
        if int(pg) > 1:
            return result
        offset = ''
        videos = []
        for i in range(0,10):
            url= 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all?timezone_offset=-480&type=all&page={0}&offset={1}'.format(pg,offset)
            rsp = self.fetch(url,cookies=self.getCookie())
            content = rsp.text
            jo = json.loads(content)
            if jo['code'] == 0:
                offset = jo['data']['offset']
                vodList = jo['data']['items']
                for vod in vodList:
                    if vod['type'] == 'DYNAMIC_TYPE_AV':
                        ivod = vod['modules']['module_dynamic']['major']['archive']
                        aid = str(ivod['aid']).strip()
                        title = ivod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                        img =  ivod['cover'].strip()
                        remark = str(ivod['duration_text']).strip()
                        videos.append({
                            "vod_id":aid,
                            "vod_name":title,
                            "vod_pic":img,
                            "vod_remarks":remark
                        })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result
    def get_hot(self,pg):
        result = {}
        url= 'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={0}'.format(pg)
        rsp = self.fetch(url,cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                img =  vod['pic'].strip()
                remark = str(vod['duration']).strip()
                videos.append({
                    "vod_id":aid,
                    "vod_name":title,
                    "vod_pic":img,
                    "vod_remarks":remark
                })
            result['list'] = videos
            result['page'] = pg
            result['pagecount'] = 9999
            result['limit'] = 90
            result['total'] = 999999
        return result
    def get_rank(self):
        result = {}
        url= 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all'
        rsp = self.fetch(url,cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] == 0:
            videos = []
            vodList = jo['data']['list']
            for vod in vodList:
                aid = str(vod['aid']).strip()
                title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                img =  vod['pic'].strip()
                remark = str(vod['duration']).strip()
                videos.append({
                    "vod_id":aid,
                    "vod_name":title,
                    "vod_pic":img,
                    "vod_remarks":remark
                })
            result['list'] = videos
            result['page'] = 1
            result['pagecount'] = 1
            result['limit'] = 90
            result['total'] = 999999
        return result
    def get_channel(self,pg,cid):
        result = {}
        if int(pg) > 1:
            return result
        offset = ''
        videos = []
        for i in range(0,5):
            url= 'https://api.bilibili.com/x/web-interface/web/channel/multiple/list?channel_id={0}&sort_type=hot&offset={1}&page_size=30'.format(cid,offset)
            rsp = self.fetch(url,cookies=self.getCookie())
            content = rsp.text
            print(content)
            jo = json.loads(content)
            if jo['code'] == 0:
                offset = jo['data']['offset']
                vodList = jo['data']['list']
                for vod in vodList:
                    if vod['card_type'] == 'rank':
                        rankVods = vod['items']
                        for ivod in rankVods:
                            aid = str(ivod['id']).strip()
                            title = ivod['name'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                            img =  ivod['cover'].strip()
                            remark = str(ivod['duration']).strip()
                            videos.append({
                                "vod_id":aid,
                                "vod_name":title,
                                "vod_pic":img,
                                "vod_remarks":remark
                            })
                    elif vod['card_type'] == 'archive':
                        aid = str(vod['id']).strip()
                        title = vod['name'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
                        img =  vod['cover'].strip()
                        remark = str(vod['duration']).strip()
                        videos.append({
                            "vod_id":aid,
                            "vod_name":title,
                            "vod_pic":img,
                            "vod_remarks":remark
                        })
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result
    def categoryContent(self,tid,pg,filter,extend):	
        print(tid,pg,filter,extend)
        result = {}
        if tid == "热门":
            return self.get_hot(pg=pg)
        if tid == "排行榜" :
            return self.get_rank()
        if tid == '动态':
            return self.get_dynamic(pg=pg)
        if tid == '频道':
            cid = '9222'
            if 'cid' in extend:
                cid = extend['cid']
            return self.get_channel(pg=pg,cid=cid)
        url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page={1}'.format(tid,pg)
        if len(self.cookies) <= 0:
            self.getCookie()
        rsp = self.fetch(url,cookies=self.getCookie())
        content = rsp.text
        jo = json.loads(content)
        if jo['code'] != 0:			
            rspRetry = self.fetch(url,cookies=self.getCookie())
            content = rspRetry.text		
        jo = json.loads(content)
        videos = []
        vodList = jo['data']['result']
        for vod in vodList:
            aid = str(vod['aid']).strip()
            title = tid + ":" + vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
            img = 'https:
