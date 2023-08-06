import scrapy 
import json
import re
from wonder.items import WonderItem
from scrapy.http import JsonRequest
from wonder.items import seperateItem
class QuotesSpider(scrapy.Spider):
    name = "wonders_additions"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
    }
    
    def start_requests(self):
           start_urls = ['https://api.deworkxyz.com/graphql?op=GetPopularOrganizationsQuery']
           
           payload={"operationName":"GetPopularOrganizationsQuery","variables":{},"query":"query GetPopularOrganizationsQuery {\n  organizations: getPopularOrganizations {\n    ...Organization\n    userCount\n    __typename\n  }\n}\n\nfragment Organization on Organization {\n  id\n  name\n  imageUrl\n  slug\n  tagline\n  description\n  permalink\n  nodeId\n  __typename\n}\n"}
           for url in start_urls:
            yield scrapy.FormRequest(url=url,method='POST', callback=self.parse,formdata=payload)
    

    def parse(self, response):
        data=json.loads(response.text)
        task_url='https://api.deworkxyz.com/graphql?op=GetOrganizationTasksQuery'
        tasks_payload={"operationName":"GetOrganizationTasksQuery","variables":{"organizationId":"dde641cb-b50e-403f-955a-f83c154e441f"},"query":"query GetOrganizationTasksQuery($organizationId: UUID!, $filter: TaskFilterInput) {\n  organization: getOrganization(id: $organizationId) {\n    id\n    tasks(filter: $filter) {\n      ...TaskWithOrganization\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment TaskWithOrganization on Task {\n  ...Task\n  workspace {\n    ...Workspace\n    organization {\n      ...Organization\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Task on Task {\n  id\n  name\n  description\n  status\n  priority\n  sortKey\n  storyPoints\n  dueDate\n  createdAt\n  doneAt\n  deletedAt\n  template\n  templateTaskId\n  templateTask {\n    id\n    name\n    __typename\n  }\n  workspaceId\n  workspace {\n    ...Workspace\n    __typename\n  }\n  parentTaskId\n  parentTask {\n    id\n    name\n    __typename\n  }\n  sectionId\n  number\n  gating\n  openToBids\n  submissionCount\n  applicationCount\n  maxWinners\n  subtasks {\n    ...Subtask\n    __typename\n  }\n  tags {\n    ...TaskTag\n    __typename\n  }\n  skills {\n    ...Skill\n    __typename\n  }\n  assignees {\n    ...User\n    __typename\n  }\n  owners {\n    ...User\n    __typename\n  }\n  creator {\n    ...User\n    __typename\n  }\n  rewards {\n    ...TaskReward\n    __typename\n  }\n  review {\n    ...TaskReview\n    __typename\n  }\n  reactions {\n    ...TaskReaction\n    __typename\n  }\n  __typename\n}\n\nfragment TaskTag on TaskTag {\n  id\n  label\n  color\n  createdAt\n  deletedAt\n  workspaceId\n  __typename\n}\n\nfragment Skill on Skill {\n  id\n  name\n  emoji\n  imageUrl\n  __typename\n}\n\nfragment TaskReward on TaskReward {\n  id\n  amount\n  peggedToUsd\n  fundingSessionId\n  token {\n    ...PaymentToken\n    network {\n      ...PaymentNetwork\n      __typename\n    }\n    __typename\n  }\n  tokenId\n  payments {\n    id\n    amount\n    user {\n      ...User\n      __typename\n    }\n    payment {\n      ...Payment\n      __typename\n    }\n    __typename\n  }\n  count\n  type\n  __typename\n}\n\nfragment Payment on Payment {\n  id\n  status\n  data\n  createdAt\n  paymentMethod {\n    ...PaymentMethod\n    __typename\n  }\n  __typename\n}\n\nfragment PaymentMethod on PaymentMethod {\n  id\n  type\n  address\n  network {\n    ...PaymentNetwork\n    __typename\n  }\n  __typename\n}\n\nfragment PaymentNetwork on PaymentNetwork {\n  id\n  slug\n  name\n  type\n  config\n  sortKey\n  __typename\n}\n\nfragment PaymentToken on PaymentToken {\n  id\n  exp\n  type\n  name\n  symbol\n  address\n  identifier\n  usdPrice\n  networkId\n  visibility\n  imageUrl\n  __typename\n}\n\nfragment User on User {\n  id\n  username\n  imageUrl\n  permalink\n  nodeId\n  __typename\n}\n\nfragment Subtask on Task {\n  id\n  name\n  status\n  sortKey\n  __typename\n}\n\nfragment TaskReview on TaskReview {\n  id\n  message\n  rating\n  createdAt\n  __typename\n}\n\nfragment TaskReaction on TaskReaction {\n  id\n  userId\n  reaction\n  __typename\n}\n\nfragment Workspace on Workspace {\n  id\n  slug\n  name\n  icon\n  type\n  status\n  description\n  startAt\n  endAt\n  deletedAt\n  organizationId\n  permalink\n  sectionId\n  parentId\n  sortKey\n  roadmapSortKey\n  options {\n    showCommunitySuggestions\n    __typename\n  }\n  __typename\n}\n\nfragment Organization on Organization {\n  id\n  name\n  imageUrl\n  slug\n  tagline\n  description\n  permalink\n  nodeId\n  __typename\n}\n"}
        for  i in data['data']['organizations']:
                  tasks_payload['variables']['organizationId']=i['id']
                  request=JsonRequest(task_url,headers=self.headers,callback=self.parse_organization,data=tasks_payload,cb_kwargs=dict(dao=i['name']))
                  request.cb_kwargs['link']=i['permalink']
                  yield request
            
    def parse_organization(self, response,dao,link):
        data=json.loads(response.text)
        tasks=data['data']['organization']['tasks']
        print(len(tasks))
        print(dao)
        for i in tasks:
                id=i['id']
                url=link+'/board?taskId='+id
                yield scrapy.Request(url,callback=self.parse_id,cb_kwargs=dict(id=id,dao=dao))
    
    def parse_reward(self,reward,data):
            if isinstance(reward,list):
                 
                 if len(reward)>0:
                    reward=[data[i['__ref']] for i in reward]

                    reward=[(i['amount'],data[i['token']['__ref']]) for  i  in reward ]
                    return reward
                 else:
                    return ''
            else:
                  reward=data[reward['__ref']]
              
                  reward=(reward['amount'],data[reward['token']['__ref']])
               
                  return  reward 
  
            
  
    def parse_thread(self,thread,data):
    
                    messages=[data[i['__ref']] for i in data[thread['__ref']]['messages']]
                    creat=data[thread['__ref']]['createdAt']
                    return {'creat':creat,'messages':messages}

    def parse_reactions(self,reactions,data):
            if isinstance(reactions,list):
                 if len(reactions)>0:
                    return [data[i['__ref']] for i in reactions]
                 else:
                    return ''
            else:
                  return data[reactions['__ref']]
    
     
    
    def parse_id(self,response,id,dao):
            wonder_item = seperateItem()
            data=json.loads(response.css('#__NEXT_DATA__::text').get())
            full=data['props']['apolloState']['data']
            if 'Task:{}'.format(id) in full.keys():
                             data=full['Task:{}'.format(id)]
                             wonder_item['id']=data['id']
                             if data['rewards']==None:
                                     wonder_item['rewards']=''
                             else:
                                     wonder_item['rewards']=str(self.parse_reward(data['rewards'],full))
                            
                      
                             if data['thread']==None:
                                       wonder_item['thread']=''
                             else:
                                       wonder_item['thread']=str(self.parse_thread(data['thread'],full)) 
                            
                             return wonder_item