# -*- coding:UTF-8 -*-
import scrapy
import json
import shutil
import os

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

if os.path.isdir("./blogs"):
    shutil.rmtree('./blogs')
os.mkdir("./blogs")

jsonFileName = "./list.json"
oldArray = []
with open(jsonFileName, 'r') as data_file:
    json_data = data_file.read()
    print "json_data:", json_data
    oldArray = json.loads(json_data)


contentHead = """
<link rel="stylesheet" href="https://csdnimg.cn/public/common/toolbar/content_toolbar_css/content_toolbar.css">
<script id="toolbar-tpl-scriptId" src="https://csdnimg.cn/public/common/toolbar/js/content_toolbar.js" type="text/javascript" domain="https://blog.csdn.net/"></script>
<link rel="stylesheet" href="https://csdnimg.cn/release/phoenix/template/css/blog_code-c3a0c33d5c.css">
<link rel="stylesheet" href="https://csdnimg.cn/release/phoenix/vendor/pagination/paging.css">

"""
contentSurffix = """

"""

class CsdnDetailSpider(scrapy.spiders.Spider):
    name = "csdn-detail"
    allowed_domains = ["https://blog.csdn.net"]
    start_urls = oldArray

    def parse(self, response):
        filename = response.url.replace(":","_").replace("/","_").replace(".","_").replace("?","_").replace("&","_")
        with open(filename, 'wb') as f:
            f.write(response.body)

        print "===================================="
        for sel in response.xpath("//div[@class='blog-content-box']"):
            title = sel.xpath("//div[@class='article-header-box']/div/div/h1/text()").extract_first()
            time = sel.xpath("//div[@class='article-info-box']/div/span/text()").extract_first()
            content = sel.xpath("//div[@class='htmledit_views']").extract_first()
        
            mdFileName = "./blogs/移动端_"+title.replace("【","").replace("】","_").replace(" ","_").replace("〖","").replace("〗","")+".html"
            contentPrefix =  "---"+ "\ntitle: 移动端_IOS"+title+"\ndate: "+time+"\ncategories: [技术]"+ "\ntags: [移动端]"+ "\n---\n"
            # print title, time
            # print content
            print mdFileName
            with open(mdFileName, 'wb') as f:
                f.write(contentPrefix +contentHead+content+contentSurffix)    
        print "===================================="    
