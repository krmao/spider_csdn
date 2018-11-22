import scrapy
import json

urls = []
pageCount = 5
jsonFileName = "./list.json"

for pageNum in range(1,pageCount+1):
    urls.append("https://blog.csdn.net/mkrcpp/article/list/"+str(pageNum))

class CsdnListSpider(scrapy.spiders.Spider):
    name = "csdn-list"
    allowed_domains = ["https://blog.csdn.net"]
    start_urls = urls

    def parse(self, response):

        filename = response.url.replace(":","_").replace("/","_").replace(".","_").replace("?","_").replace("&","_")
        with open(filename, 'wb') as f:
            f.write(response.body)

        oldArray = []
        with open(jsonFileName, 'r') as data_file:
            json_data = data_file.read()
            print "json_data:", json_data
            oldArray = json.loads(json_data)
        
        print "oldArray:", oldArray

        print "===================================="
        for sel in response.xpath("//main/div").xpath("//div[@class='article-item-box csdn-tracking-statistics']"):
            link = sel.xpath("h4/a/@href").extract_first()
            if "mkr127" in link or "mkrcpp" in link: # 你可能修改过用户名, 都写在这里
                title = sel.xpath("h4/a/text()").extract()[1].strip()
                time = sel.xpath("div[@class='info-box d-flex align-content-center']/p/span/text()").extract_first()
                # print title, time
                # print link, "\n"

                if not link in oldArray:
                    oldArray.append(link)
                
        with open(jsonFileName, 'w+') as f:
            f.write(json.dumps(oldArray,indent=4))
        print "===================================="