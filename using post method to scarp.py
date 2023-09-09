import time
from aiohttp import ClientSession, ClientResponseError
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import requests
from sqlalchemy import create_engine
from tqdm import tqdm

def get_data(data):
      #try:assignees='|'.join([i['username'] for i in data['data']['task']['assignees']])
      #except: assignees=None 
      #try: comments=[i['content'] for i in data['data']['task']['thread']['messages']]
      #except:comments=None
      #try:tags=[i['label'] for i in data['data']['task']['tags']]
      #except:tags=None
      try: rewards=data['data']['task']['rewards'][0]['token']['usdPrice']
      except:rewards=None
      dic={
           'id': str(data['data']['task']['id']),
           #'name': str(data['data']['task']['name']),
           #'description':str(data['data']['task']['description']),
           #'organiazation':str(data['data']['task']['workspace']['organization']['name']),
           #'createdAt':str(data['data']['task']['createdAt']),
           #'creator':str(data['data']['task']['creator']['username']),
           #'audit_log':str(data['data']['task']['auditLog']),
           #'due_date': str(data['data']['task']['dueDate']),
           #'assignees':assignees,
           #'subtasks': str(data['data']['task']['subtasks']),
           #'priority':str(data['data']['task']['priority']),
           #'status':str(data['data']['task']['status']),
           #'tags':str(tags),
           'review':str(data['data']['task']['review']),
           #'permalink':str(data['data']['task']['permalink']),
           #'rewards':rewards,
           #'doneAt':str(data['data']['task']['doneAt']),
           #'comments':str(comments)}
         }
      return dic
def load_data(data):
    engine = create_engine("postgresql+psycopg2://postgres:Xw21872802?@localhost/wonders")
    df=pd.DataFrame.from_records([data])
    with engine.begin() as connection:
        df.to_sql('d', con=connection, if_exists='append')
    print('done')

def fetch_org_ids():
       get_all_organization_url='https://api.deworkxyz.com/graphql?op=GetPopularOrganizationsQuery'
       org_payload={
  "operationName": "GetPopularOrganizationsQuery",
  "variables": {},
  "query": "query GetPopularOrganizationsQuery {\n  organizations: getPopularOrganizations {\n    ...Organization\n    userCount\n    __typename\n  }\n}\n\nfragment Organization on Organization {\n  id\n  name\n  imageUrl\n  slug\n  tagline\n  description\n  permalink\n  nodeId\n  __typename\n}\n"
}
       x=requests.post(get_all_organization_url, json = {
  "operationName": "GetPopularOrganizationsQuery",
  "variables": {},
  "query": "query GetPopularOrganizationsQuery {\n  organizations: getPopularOrganizations {\n    ...Organization\n    userCount\n    __typename\n  }\n}\n\nfragment Organization on Organization {\n  id\n  name\n  imageUrl\n  slug\n  tagline\n  description\n  permalink\n  nodeId\n  __typename\n}\n"
},timeout=None)
       data=json.loads(x.text)
       ids= [i['id'] for i in data['data']['organizations']]
       return ids
task_id=[]
def load(data):
        return [i['id'] for i in json.loads(data.text)["data"]['organization']['tasks']]
def fetch_task_ids(id):
       get_task_url='https://api.deworkxyz.com/graphql?op=GetOrganizationTasksQuery'
       tasks_payload={
  "operationName": "GetOrganizationTasksQuery",
  "variables": {
    "organizationId": "{}".format(id)
  },
  "query": "query GetOrganizationTasksQuery($organizationId: UUID!, $filter: TaskFilterInput) {\n  organization: getOrganization(id: $organizationId) {\n    id\n    tasks(filter: $filter) {\n      ...TaskWithOrganization\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment TaskWithOrganization on Task {\n  ...Task\n  workspace {\n    ...Workspace\n    organization {\n      ...Organization\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Task on Task {\n  id\n  name\n  description\n  status\n  priority\n  sortKey\n  storyPoints\n  dueDate\n  createdAt\n  doneAt\n  deletedAt\n  template\n  templateTaskId\n  templateTask {\n    id\n    name\n    __typename\n  }\n  workspaceId\n  workspace {\n    ...Workspace\n    __typename\n  }\n  parentTaskId\n  parentTask {\n    id\n    name\n    __typename\n  }\n  sectionId\n  number\n  gating\n  openToBids\n  submissionCount\n  applicationCount\n  maxWinners\n  subtasks {\n    ...Subtask\n    __typename\n  }\n  tags {\n    ...TaskTag\n    __typename\n  }\n  skills {\n    ...Skill\n    __typename\n  }\n  assignees {\n    ...User\n    __typename\n  }\n  owners {\n    ...User\n    __typename\n  }\n  creator {\n    ...User\n    __typename\n  }\n  rewards {\n    ...TaskReward\n    __typename\n  }\n  review {\n    ...TaskReview\n    __typename\n  }\n  reactions {\n    ...TaskReaction\n    __typename\n  }\n  __typename\n}\n\nfragment TaskTag on TaskTag {\n  id\n  label\n  color\n  createdAt\n  deletedAt\n  workspaceId\n  __typename\n}\n\nfragment Skill on Skill {\n  id\n  name\n  emoji\n  imageUrl\n  __typename\n}\n\nfragment TaskReward on TaskReward {\n  id\n  amount\n  peggedToUsd\n  fundingSessionId\n  token {\n    ...PaymentToken\n    network {\n      ...PaymentNetwork\n      __typename\n    }\n    __typename\n  }\n  tokenId\n  payments {\n    id\n    amount\n    user {\n      ...User\n      __typename\n    }\n    payment {\n      ...Payment\n      __typename\n    }\n    __typename\n  }\n  count\n  type\n  __typename\n}\n\nfragment Payment on Payment {\n  id\n  status\n  data\n  createdAt\n  paymentMethod {\n    ...PaymentMethod\n    __typename\n  }\n  __typename\n}\n\nfragment PaymentMethod on PaymentMethod {\n  id\n  type\n  address\n  network {\n    ...PaymentNetwork\n    __typename\n  }\n  __typename\n}\n\nfragment PaymentNetwork on PaymentNetwork {\n  id\n  slug\n  name\n  type\n  config\n  sortKey\n  __typename\n}\n\nfragment PaymentToken on PaymentToken {\n  id\n  exp\n  type\n  name\n  symbol\n  address\n  identifier\n  usdPrice\n  networkId\n  visibility\n  imageUrl\n  __typename\n}\n\nfragment User on User {\n  id\n  username\n  imageUrl\n  permalink\n  nodeId\n  __typename\n}\n\nfragment Subtask on Task {\n  id\n  name\n  status\n  sortKey\n  __typename\n}\n\nfragment TaskReview on TaskReview {\n  id\n  message\n  rating\n  createdAt\n  __typename\n}\n\nfragment TaskReaction on TaskReaction {\n  id\n  userId\n  reaction\n  __typename\n}\n\nfragment Workspace on Workspace {\n  id\n  slug\n  name\n  icon\n  type\n  status\n  description\n  startAt\n  endAt\n  deletedAt\n  organizationId\n  permalink\n  sectionId\n  parentId\n  sortKey\n  roadmapSortKey\n  options {\n    showCommunitySuggestions\n    __typename\n  }\n  __typename\n}\n\nfragment Organization on Organization {\n  id\n  name\n  imageUrl\n  slug\n  tagline\n  description\n  permalink\n  nodeId\n  __typename\n}\n"
}
       try:x = requests.post(get_task_url, json =tasks_payload,timeout=30)
       except:pass
       else:
            try:
                return(load(x))
            except:
                pass 
     
                 
                        
                                             
       
def query_data(id):
    task_payload={
  "operationName": "GetTaskDetailsQuery",
  "variables": {
    "taskId": "{}".format(id)
  },
  "query": "query GetTaskDetailsQuery($taskId: UUID!) {\n  task: getTask(id: $taskId) {\n    ...TaskDetails\n    __typename\n  }\n}\n\nfragment TaskDetails on Task {\n  ...Task\n  featured\n  gitBranchName\n  applicationLink\n  applicationTemplate\n  submissionTemplate\n  permalink\n  maxWinners\n  workspace {\n    ...Workspace\n    organization {\n      ...Organization\n      __typename\n    }\n    __typename\n  }\n  parentTask {\n    id\n    name\n    __typename\n  }\n  owners {\n    ...User\n    __typename\n  }\n  creator {\n    ...User\n    __typename\n  }\n  githubPullRequests {\n    ...GithubPullRequest\n    __typename\n  }\n  githubBranches {\n    ...GithubBranch\n    __typename\n  }\n  githubIssue {\n    ...GithubIssue\n    __typename\n  }\n  notionPage {\n    permalink\n    __typename\n  }\n  applications {\n    ...TaskApplication\n    __typename\n  }\n  submissions {\n    ...TaskSubmission\n    __typename\n  }\n  nfts {\n    ...TaskNFT\n    __typename\n  }\n  rewards {\n    ...TaskReward\n    payments {\n      user {\n        ...User\n        __typename\n      }\n      payment {\n        ...Payment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  auditLog {\n    ...AuditLogEvent\n    __typename\n  }\n  thread {\n    ...Thread\n    __typename\n  }\n  __typename\n}\n\nfragment Task on Task {\n  id\n  name\n  description\n  status\n  priority\n  sortKey\n  storyPoints\n  dueDate\n  createdAt\n  doneAt\n  deletedAt\n  template\n  templateTaskId\n  templateTask {\n    id\n    name\n    __typename\n  }\n  workspaceId\n  workspace {\n    ...Workspace\n    __typename\n  }\n  parentTaskId\n  parentTask {\n    id\n    name\n    __typename\n  }\n  sectionId\n  number\n  gating\n  openToBids\n  submissionCount\n  applicationCount\n  maxWinners\n  subtasks {\n    ...Subtask\n    __typename\n  }\n  tags {\n    ...TaskTag\n    __typename\n  }\n  skills {\n    ...Skill\n    __typename\n  }\n  assignees {\n    ...User\n    __typename\n  }\n  owners {\n    ...User\n    __typename\n  }\n  creator {\n    ...User\n    __typename\n  }\n  rewards {\n    ...TaskReward\n    __typename\n  }\n  review {\n    ...TaskReview\n    __typename\n  }\n  reactions {\n    ...TaskReaction\n    __typename\n  }\n  __typename\n}\n\nfragment TaskTag on TaskTag {\n  id\n  label\n  color\n  createdAt\n  deletedAt\n  workspaceId\n  __typename\n}\n\nfragment Skill on Skill {\n  id\n  name\n  emoji\n  imageUrl\n  __typename\n}\n\nfragment TaskReward on TaskReward {\n  id\n  amount\n  peggedToUsd\n  fundingSessionId\n  token {\n    ...PaymentToken\n    network {\n      ...PaymentNetwork\n      __typename\n    }\n    __typename\n  }\n  tokenId\n  payments {\n    id\n    amount\n    user {\n      ...User\n      __typename\n    }\n    payment {\n      ...Payment\n      __typename\n    }\n    __typename\n  }\n  count\n  type\n  __typename\n}\n\nfragment Payment on Payment {\n  id\n  status\n  data\n  createdAt\n  paymentMethod {\n    ...PaymentMethod\n    __typename\n  }\n  __typename\n}\n\nfragment PaymentMethod on PaymentMethod {\n  id\n  type\n  address\n  network {\n    ...PaymentNetwork\n    __typename\n  }\n  __typename\n}\n\nfragment PaymentNetwork on PaymentNetwork {\n  id\n  slug\n  name\n  type\n  config\n  sortKey\n  __typename\n}\n\nfragment PaymentToken on PaymentToken {\n  id\n  exp\n  type\n  name\n  symbol\n  address\n  identifier\n  usdPrice\n  networkId\n  visibility\n  imageUrl\n  __typename\n}\n\nfragment User on User {\n  id\n  username\n  imageUrl\n  permalink\n  nodeId\n  __typename\n}\n\nfragment Subtask on Task {\n  id\n  name\n  status\n  sortKey\n  __typename\n}\n\nfragment TaskReview on TaskReview {\n  id\n  message\n  rating\n  createdAt\n  __typename\n}\n\nfragment TaskReaction on TaskReaction {\n  id\n  userId\n  reaction\n  __typename\n}\n\nfragment Workspace on Workspace {\n  id\n  slug\n  name\n  icon\n  type\n  status\n  description\n  startAt\n  endAt\n  deletedAt\n  organizationId\n  permalink\n  sectionId\n  parentId\n  sortKey\n  roadmapSortKey\n  options {\n    showCommunitySuggestions\n    __typename\n  }\n  __typename\n}\n\nfragment TaskNFT on TaskNFT {\n  id\n  tokenId\n  createdAt\n  contractAddress\n  explorerUrl\n  payment {\n    ...Payment\n    __typename\n  }\n  __typename\n}\n\nfragment Organization on Organization {\n  id\n  name\n  imageUrl\n  slug\n  tagline\n  description\n  permalink\n  nodeId\n  __typename\n}\n\nfragment GithubPullRequest on GithubPullRequest {\n  id\n  title\n  link\n  status\n  number\n  branchName\n  createdAt\n  updatedAt\n  __typename\n}\n\nfragment GithubBranch on GithubBranch {\n  id\n  name\n  link\n  repo\n  organization\n  createdAt\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment GithubIssue on GithubIssue {\n  id\n  number\n  link\n  __typename\n}\n\nfragment TaskApplication on TaskApplication {\n  id\n  message\n  startDate\n  endDate\n  createdAt\n  updatedAt\n  userId\n  discordThreadUrl\n  reward {\n    ...TaskReward\n    __typename\n  }\n  status\n  user {\n    ...User\n    details {\n      ...EntityDetail\n      __typename\n    }\n    __typename\n  }\n  thread {\n    ...Thread\n    __typename\n  }\n  __typename\n}\n\nfragment EntityDetail on EntityDetail {\n  id\n  type\n  value\n  __typename\n}\n\nfragment Thread on Thread {\n  id\n  createdAt\n  messages {\n    ...ThreadMessage\n    __typename\n  }\n  task {\n    id\n    workspaceId\n    __typename\n  }\n  workspace {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment ThreadMessage on ThreadMessage {\n  id\n  createdAt\n  content\n  threadId\n  senderId\n  sender {\n    ...User\n    __typename\n  }\n  __typename\n}\n\nfragment TaskSubmission on TaskSubmission {\n  id\n  content\n  createdAt\n  updatedAt\n  taskId\n  userId\n  status\n  reward {\n    ...TaskReward\n    __typename\n  }\n  user {\n    ...User\n    __typename\n  }\n  approver {\n    ...User\n    __typename\n  }\n  thread {\n    ...Thread\n    __typename\n  }\n  __typename\n}\n\nfragment AuditLogEvent on AuditLogEvent {\n  id\n  createdAt\n  user {\n    ...User\n    __typename\n  }\n  sessionId\n  diff\n  __typename\n}\n"
}
    try:x = requests.post('https://api.deworkxyz.com/graphql?op=GetTaskDetailsQuery', json=task_payload,timeout=30)
    except:pass
    else:return(json.loads(x.text))
  
           



if __name__ == '__main__':
    ids=fetch_org_ids()
    id_tasks=[]
    for id in ids:
         start_time = time.time()
         task_id=fetch_task_ids(id)
         if task_id!=None:
              id_tasks.extend(task_id)
              print('fetching {} ids takes {} seconds'.format(len(task_id),time.time() - start_time))
    print(len(id_tasks))
    pbar=tqdm(id_tasks)
    for i in pbar:
         try:
           data=get_data(query_data(i))
         except:
           print('error')
         else:
           load_data(data)
    

    