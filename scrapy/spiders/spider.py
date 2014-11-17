#!/usr/bin/env python
# coding: utf-8
# author: yuxq
# create_at: 2014-10-29
# vim: set noexpandtab tabstop=4 shiftwidth=4 softtabstop=4

import os
import sys
import re
import pprint
import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from fml.items import FmlItem

class MySpider(CrawlSpider):
	name = 'haoduanzi'
	allowed_domains = ['haoduanzi.com']
	start_urls = ["http://www.haoduanzi.com/catalog.asp?page=1"]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		page = hxs.select('//div[@class="pagebar"]/span[@class="now-page"]/text()').extract()[0]
		next_page = int(page) + 1
		
		url = urlparse.urljoin(response.url, "?page=%s" % next_page)
		self.log(url)
		yield Request(url, callback=self.parse)
		
		for p in hxs.select('//div[@class="post2"]/div[@class="post-contents"]/p').extract():
			_url = ''
			cont = re.sub(r'<[^>]*?>', '', p).strip()
			if cont:
				yield FmlItem(cont=cont, url=_url)
