from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
from collections import Counter
import emoji
import pandas as pd
print(extract.find_urls("Visit https://openai.com or http://example.com"))
def fetchStats(selected_user, df):
    if selected_user != 'Overall':
        df= df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_media_messages= df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages,len(words),num_media_messages,len(links)       


    # if selected_user == 'Overall':
    #     num_messages = df.shape[0]
    #     words = []
    #     for message in df['message']:
    #         words.extend(message.split())

    #     return num_messages,len(words)
    # else:
    #     new_df= df[df['user'] == selected_user]
    #     num_messages = new_df.shape[0]
    #     words = []
    #     for message in new_df['message']:
    #         words.extend(message.split())
    #     return num_messages,len(words)

def fetch_Active_users(df):
    df =  df[df['user'] != 'group_notification']
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0])* 100,2).reset_index().rename(columns={'index':'name','user':'percent'})

    return x,df

def create_wordCloud(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    temp =  df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def fetch_most_frequently_used(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    temp =  df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(25))
    return return_df


def most_emoji_used(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emoji_list = emoji.distinct_emoji_list(message)
        emojis.extend(emoji_list)
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-" + str(timeline['year'][i]))  
    timeline['time'] = time
    return timeline

def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user']== selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != "Overall":
        df= df[df['user']==selected_user]

    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap