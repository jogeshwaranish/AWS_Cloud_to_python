#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Dynamo
import pandas as pd

import json 
from pprint import pprint
from urllib.request import urlopen

url = 'https://api.chess.com/pub/player/gmhikaruontwitch/games/2020/07'
json_url = urlopen(url)
text = json.loads(json_url.read())

dynamo_list = []
i = 0
while i < len(text['games']):
    
    for items in text:
        
        main_dic = {}
        main_dic['Pgn'] = text['games'][i]['pgn']
        dynamo_list.append(main_dic)
        i+=1





# In[4]:


s4 = []
for i in range(0,len(dynamo_list)):
    s4.append(dynamo_list[i]["Pgn"])


# In[5]:


s4


# In[6]:


## data schema 
player_side = []
result = []
first_move = []
legal_moves = ['1. e4','1. d4','1. c4','1. Nf3','1. Nc3','1. e3','1. d3','1. a3','1. b3','1. g3']
won_statements= ['GMHikaruOnTwitch won by checkmate','GMHikaruOnTwitch won by resignation','GMHikaruOnTwitch won on time']
side_statements = ['White "GMHikaruOnTwitch"','Black "GMHikaruOnTwitch"']
for i in s4:
    for a in legal_moves:
        if(i.find(a)>0):
            first_move.append(a[3:])
    for b in won_statements:
        if(i.find(b)>0):
            result.append("won")
        else:
            result.append("lost")
    for c in side_statements:
        if(i.find(c)>0):
            player_side.append(c[:5])
            
  
    


# In[7]:


legal_moves = ['1. e4','1. d4','1. c4','1. Nf3','1. Nc3','1. e3','1. d3','1. a3','1. b3','1. g3']
moves_played = []
for i in dynamo_list:
    for a in legal_moves:
        if(i.find(a)>0):
            first_move.append(a[3:])


# In[8]:


len(s4)


# In[9]:


import boto3
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('chessgames')
for i in range(1,len(s4)):
    table.put_item(Item= {"GameNum" :i,
                           "First_Move":first_move[i],
                          "Players":player_side[i],
                          "Result":result[i]
                         } )


# In[15]:





response = table.query(
    KeyConditionExpression=Key('Result').eq('won')
)


# In[ ]:


__TableName__  =  "chessgame"

Primary_Column_Name = 'game_num'
Primary_Key = 1
columns = ['pgn']


# In[ ]:


print(len(dynamo_list))


# In[ ]:


response = table.scan()

s1 = list(response["Items"])


# In[ ]:


pprint(s1)


# In[ ]:


pprint(s1[0]['game']["Pgn"])


# In[ ]:


s2 = []
for i in range(1,48):
    if s1[i]['game']["Pgn"].find('White "GMHikaruOnTwitch"') > 0:
        s2.append(s1[i]['game']['Pgn'])
won_statements= ['GMHikaruOnTwitch won by checkmate','GMHikaruOnTwitch won by resignation','GMHikaruOnTwitch won on time']      
game_won = []
for i in range(0,len(s2)):
    for a in won_statements:
        if(s2[i].find(a)>0):
            game_won.append(s2[i])


# In[ ]:


len(game_won)


# In[ ]:


legal_moves = ['1. e4','1. d4','1. c4','1. Nf3','1. Nc3','1. e3','1. d3','1. a3','1. b3','1. g3']
moves_played = []
for i in game_won:
    for a in legal_moves:
        if(i.find(a)>0):
            moves_played.append(a[3:])


# In[ ]:



unique = set(moves_played)
unique


# In[ ]:


moves_played.count('g3')


# In[1]:


from matplotlib import pyplot as plt

data3 = {'Nc3':6,'Nf3':8,'a3':1,'b3':3,'c4':2,'d4':17,'e3':1,'e4':18,'g3':2}
move2 = list(data3.keys())
num_games = list(data3.values())
fig = plt.figure(figsize = (4,10))
plt.bar(move2,num_games, color ='maroon', width = 0.4)
plt.xlabel('Moves')
plt.ylabel('# of games')
plt.title('Hikaru first moves')
plt.show()

