# 💬 WInsight – WhatsApp Chat Analyzer

**WInsight** is a Streamlit-powered web app designed to analyze and visualize WhatsApp chat data. It offers insights into message counts, user activity, emoji usage, timelines, word frequency, and more — all from your exported `.txt` WhatsApp chat file.

---

## 🚀 Features

- 📈 **Monthly & Daily Timelines** – Track chat activity over time.
- 🧑‍🤝‍🧑 **Most Active Users** – Discover who participates the most in the group.
- 🧾 **Message Statistics** – Get total messages, media shared, links, and words.
- 🔤 **Most Common Words** – Visualize frequently used terms.
- 😂 **Emoji Analysis** – See which emojis are used most.
- 📊 **Dynamic Visualizations** – Interactive plots with `matplotlib`, `seaborn`, and `plotly`.
- 🌙 **Dark Mode Friendly** (via custom CSS styling).
- 📁 **Support for individual or group chats**.

---

## 📂 How to Use

### 1. Export WhatsApp Chat

- Open your WhatsApp chat (group or individual)
- Click **More > Export Chat**
- Select **Without Media**
- A `.txt` file will be generated

### 2. Run the App

#### Option A: Run Locally

cd winsight-chat-analyzer
pip install -r requirements.txt
streamlit run app.py
