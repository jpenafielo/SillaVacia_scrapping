import scrapy
import pandas as pd

class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = [
        "https://www.lasillavacia.com"   ]
    
    texts=[]
    links=[]
    count = 1
    
    texts_response= ''
    links_response= ''
    
   

    def parse(self, response):
        
        
        h1articles(self, response)
        h3titles(self, response)
        h2WhiteTitle(self, response)
    
        

        request = scrapy.Request(
            "https://www.lasillavacia.com/elementAjax/EnVivo/list2EnVivo?page=" + str(self.count),
            callback=self.parse_page2,
            errback=self.errback_page2,
            cb_kwargs=dict(main_url=response.url))
            
            
        yield request
            
    def parse_page2(self, response, main_url):
        
        self.count += 1
        
        urlNextPage = "https://www.lasillavacia.com/elementAjax/EnVivo/list2EnVivo?page=" + str(self.count)
    
        
        texts_response = response.css('article h3 a::text').getall()
        links_response = response.css('article h3 a::attr(href)').getall()
        
        
        for i in texts_response:
            self.texts.append(i)
        for i in links_response:
            self.links.append(i)
        
        
        if self.count <= 50:
            
            
            request = scrapy.Request(
            urlNextPage,
            callback=self.parse_page2,
            errback=self.errback_page2,
            cb_kwargs=dict(main_url=response.url))
            
            
            yield request
        else:
            
            self.count = 1
            url = "https://www.lasillavacia.com/elementAjax/LaSillaVacia/ListHistorias?page=" + str(self.count)
            request = scrapy.Request(
            urlNextPage,
            callback=self.parse_page3,
            errback=self.errback_page2,
            cb_kwargs=dict(main_url=response.url))
            
            
            yield request
            


    def errback_page2(self, failure):
        yield dict(
            main_url=failure.request.cb_kwargs["main_url"],
        )
        
    def parse_page3(self, response, main_url):
        
        self.count += 1
        
        urlNextPage = "https://www.lasillavacia.com/elementAjax/LaSillaVacia/ListHistorias?page=" + str(self.count)
    
        
        texts_response = response.css('article h3 a::text').getall()
        links_response = response.css('article h3 a::attr(href)').getall()
        
        
        for i in texts_response:
            self.texts.append(i)
        for i in links_response:
            self.links.append(i)
        
        
        if self.count <= 11:
            
            
            request = scrapy.Request(
            urlNextPage,
            callback=self.parse_page3,
            errback=self.errback_page2,
            cb_kwargs=dict(main_url=response.url))       
            yield request
            
        else:
            
            temp=[]
            
            for i in self.texts:
                if i not in temp:
                    temp.append(i)
                else:
                    self.texts.pop(self.texts.index(i))
                    self.links.pop(self.texts.index(i))


            data = {'Link': self.links, "Title": self.texts}
            df = pd.DataFrame(data)
            df.to_excel('datos.xlsx', index=False)
        
    
def h1articles(self, response):
    
    self.texts_response = response.css('h1 a::text').getall()
    self.links_response = response.css('h1 a::attr(href)').getall()

    for i in self.texts_response:
        self.texts.append(i)
    for i in self.links_response:
        self.links.append(i)
        
def h3titles(self, response):
    
    self.texts_response = response.css(' h3 a::text').getall()
    self.links_response = response.css(' h3 a::attr(href)').getall()

    for i in self.texts_response:
        self.texts.append(i)
    for i in self.links_response:
        self.links.append(i)
    
    
def h2WhiteTitle(self, response):
    
    self.texts_response = response.css('h2.h2.white.font-martin.normal.letter-0-4.uppercase.mb-5.mb-md-10 a::text').getall()
    self.links_response = response.css('h2.h2.white.font-martin.normal.letter-0-4.uppercase.mb-5.mb-md-10 a::attr(href)').getall()

    for i in self.texts_response:
        self.texts.append(i)
    for i in self.links_response:
        self.links.append(i)
    