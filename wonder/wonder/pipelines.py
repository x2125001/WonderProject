# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2


from itemadapter import ItemAdapter


class NPipeline:
    def process_item(self, item, spider):
        return item









class WonderPipeline:

    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'Xw21872802?'
        database = 'wonders'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Wonder(
            id text, 
            dao text,
            name text,
            tags text,
            description text,
            ASSIGNEES text,
            creator text, 
            priority text,  
            status_current text, 
            auditLog text,
            rewards text,
            review  text, 
            reactions text,
            thread  text,
            createdAt   text,
            dueDate    text,
            skills text
        )
        """)
  









    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute("select * from Wonder where id= %s", (item['id'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['id'])


        ## If text isn't in the DB, insert data
        else:
          self.cur.execute(""" insert into Wonder(id, 
            dao,
            name,
            tags,
            description,
            ASSIGNEES,
            creator, 
            priority,  
            status_current, 
            auditLog,
            rewards,
            review, 
            reactions,
            thread,
            createdAt,
            dueDate,
            skills) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(
            str(item["id"]),
            str(item["dao"]),
            str(item["name"]),
            str(item["tags"]),
            str(item["description"]),
            str(item["ASSIGNEES"]),
            str(item["creator"]),
            str(item["priority"]),
            str(item["status_current"]),
            str(item["auditLog"]),
            str(item["rewards"]),
            str(item["review"]),
            str(item["reactions"]),
            str(item["thread"]),
            str(item["createdAt"]),
            str(item["dueDate"]),
            str(item['skills'])

        ))

        ## Execute insert of data into database
          self.connection.commit()
          return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()




class additionPipeline:

    def __init__(self):
        ## Connection Details
        hostname = 'localhost'
        username = 'postgres'
        password = 'Xw21872802?'
        database = 'wonders'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Wonder_additions(
            id text, 
            rewards text,
            thread  text
        )
        """)
  









    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute("select * from Wonder_additions where id= %s", (item['id'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['id'])


        ## If text isn't in the DB, insert data
        else:
          self.cur.execute(""" insert into Wonder_additions(id, 
            rewards,
            thread) values (%s,%s,%s)""",(
            str(item["id"]),
            str(item["rewards"]),
            str(item["thread"])

        ))

        ## Execute insert of data into database
          self.connection.commit()
          return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
