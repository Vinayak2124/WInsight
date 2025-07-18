import streamlit as st
import preprocessor ,helper
import matplotlib.pyplot as plt
import plotly.express as px 
import numpy as np
import matplotlib.cm as cm
import seaborn as sns


st.markdown(
    """
    <style>
    .stApp {
        background-color: zinc;
        color: gray;
    }

    .stMarkdown p, .stTitle, .stHeader, .stSubheader,{
        color: yellow !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.set_page_config(
    page_title="WInsight - WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.sidebar.title('WInsight - Whatsapp Chat Analyzer')
st.markdown("<h1 style='text-align: center; color: yellow;'>📈 WInsight</h1>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("choose a file")




if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    # fetching the unique user from the df
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        st.header("Top Statistics")
        col1, col2,col3,col4 = st.columns(4)
       
        num_messages, words,num_media_message,num_links = helper.fetchStats(selected_user, df)
        with col1:
            st.subheader("Total Message")
            st.title(num_messages)
        with col2:
            st.subheader("Total Words")
            st.title(words)
        with col3:
            st.subheader("Media Shared")
            st.title(num_media_message)

        with col4:
            st.subheader("Link Shared")
            st.title(num_links)    


        # chats monthly timeline
        st.header("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        # fig,ax = plt.subplots(figsize=(20, 5))
        # ax.plot(timeline['time'],timeline['message'],color="green")
        # plt.xticks(rotation='vertical')

        fig = px.line(timeline, x='time', y='message', title='Monthly Message Timeline', markers=True)
        fig.update_traces(line=dict(color='green'))
        fig.update_layout(
        width=1000,  # set width in pixels
        height=700,
        xaxis_title='Time',
        yaxis_title='Messages',
        xaxis=dict(rangeslider_visible=True),
        template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.header("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most Active day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="brown")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.subheader("Most Active Month")
            busy_month = helper.monthly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="red")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

                # 24 hours heatmap
        st.header("Hourly Activity Map")
        user_heatmap= helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # finding the busiest users in the group (Group Level)
        if selected_user == 'Overall':
            st.header('Most Active Users')

            x, new_df = helper.fetch_Active_users(df)
            fig, ax = plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.header("Word Cloud")
        df_wc=helper.create_wordCloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_df = helper.fetch_most_frequently_used(selected_user,df)
        # st.dataframe(most_common_df)
        st.header("Most Frequently used Words")

        fig,ax = plt.subplots()
        colors = cm.get_cmap('tab20')(np.linspace(0, 1, len(most_common_df)))
        ax.barh(most_common_df[0],most_common_df[1],color=colors)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # emojis analysis
        emoji_df = helper.most_emoji_used(selected_user,df)
        st.header("Emoji Analysis")

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots(figsize=(10,5))
            ax.pie(emoji_df[1].head(10), labels = emoji_df[0].head(10),autopct = "%.2f")
            st.pyplot(fig)


        


        

        
