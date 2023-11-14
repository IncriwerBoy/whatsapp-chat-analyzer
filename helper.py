from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    #fetch number of messages
    num_messages = df.shape[0]
    words = []
    #number of words
    for msg in df['messages']:
        words.extend(msg.split())
    
    #fetch number of media msg
    num_media_messages = 0
    for msg in df['messages']:
        if msg == ' <Media omitted>\n':
            num_media_messages += 1
    
    #fetch num of links
    links = []
    for msg in df['messages']:
        links.extend(extract.find_urls(msg))
    
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_user(df):
    x = df['user'].value_counts()
    new_df = round((x/df.shape[0])*100,2).reset_index().rename(columns = {'index':'name', 'user':'percent'})
    return x, new_df

def create_wordcloud(selected_user, df):
    if 'Overall' != selected_user:
        df = df[df['user'] == selected_user]
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=' '))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    words = []
    for message in df['messages']:
        words.extend(message.split())
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def most_common_emoji(selected_user, df):
    emojis = []
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI_ALIAS_ENGLISH])
    
    df_emojis = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return df_emojis

def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['Year', 'Month', 'month_num']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + '-' + str(timeline['Year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    df['date_only'] = df['date'].dt.date
    timeline = df.groupby(['date_only']).count()['messages'].reset_index()
    return timeline

def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    df['day'] = df['date'].dt.day_name()
    return df['day'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['Month'].value_counts()