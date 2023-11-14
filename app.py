import streamlit as st
import preprocessor
import helper
from matplotlib import pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    
    if st.sidebar.button("Show Analysis"):
        
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total Words")
            st.title(num_words)
        
        with col3:
            st.header("Total Media Messages")
            st.title(num_media_messages)
        
        with col4:
            st.header("links Shared")
            st.title(num_links)
        
        
        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #daily timeline
        st.title("Monthly Timeline")
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['date_only'], timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)
        
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            st.pyplot(fig)
        
        #fetch most busy users
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
        
        #WordCloud
        st.title("WordCloud")
        temp = preprocessor.advance(df)
        df_wc = helper.create_wordcloud(selected_user, temp)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        #most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, temp)
        fig, ax = plt.subplots()
        ax.bar(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        #most common emoji
        st.title("Most Common Emoji")
        df_emojis = helper.most_common_emoji(selected_user, df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_emojis)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(df_emojis[1].head(5), labels= df_emojis[0].head(5), autopct = '%0.2f')
            st.pyplot(fig)
