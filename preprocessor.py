import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'date':dates})
    df['date'] = pd.to_datetime(df['date'], format='%y/%m/%d, %H:%M - ')


    users = []
    messages = []

    for row in df['user_message']:
        if re.search(":", row):
            user = re.split(":", row)[0]
            msg = row.split(":", maxsplit = 1)[1]
        else:
            user = 'group_notification'
            msg = row
        users.append(user)
        messages.append(msg)

    df['user'] = users
    df['messages'] = messages
    df.drop(columns = ['user_message'], inplace = True)

    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month_name()
    df['Day'] = df['date'].dt.day
    df['Hour'] = df['date'].dt.hour
    df['Minute'] = df['date'].dt.minute
    
    return df

def advance(df):
    #remove grp msg
    new_df = df[df['user'] != 'group_notification']
    
    #remove ommited media
    new_df = new_df[new_df['messages'] != ' <Media omitted>\n']
    
    #remove stopwords
    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()
    for msg in new_df['messages']:
        for word in stopwords:
            msg = msg.lower().replace(word, "")
    return new_df

