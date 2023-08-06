# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy 
from scrapy.item import Item, Field


class WonderItem(scrapy.Item):
    name=scrapy.Field()
    dao=scrapy.Field()
    description=scrapy.Field()
    id=scrapy.Field()
    ASSIGNEES=scrapy.Field()
    creator=scrapy.Field()
    tags=scrapy.Field()
    priority=scrapy.Field()
    status_current=scrapy.Field()
    auditLog=scrapy.Field()
    rewards=scrapy.Field()
    review=scrapy.Field()
    reactions=scrapy.Field()
    thread=scrapy.Field()
    createdAt=scrapy.Field()
    dueDate=scrapy.Field()
    skills=scrapy.Field()
class seperateItem(scrapy.Item):
    thread=scrapy.Field()
    rewards=scrapy.Field()
    id=scrapy.Field()
 
 