# -*- coding: gbk -*-
import json
from lxml import etree


with open('parse.txt') as file:
    tree = file.readlines()
print(tree)

tree_node = etree.HTML(tree)
tweet_nodes = tree_node.xpath('//div[@id="interest_sectl"]/div[@class="rating_wrap clearbox"]')
item=dict()
for node in tweet_nodes:
    for i in node.xpath('//a[@class="rating_people"]/span'):
        item['votes']=i.text()
        print(item['votes'])



