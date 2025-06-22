# FlipkartAssistant
Flipkart is leading e-commerce business with number of product. for user it's difficult to find and filter prodcuts. So introducing FlipkartAssistant.

# 🛍️ Flipkart Shopping Assistant (AI + MongoDB + Streamlit)

An AI-powered product assistant built with **Streamlit**, **LangChain**, **Gemini (Google Generative AI)**, and **MongoDB**. This app converts **natural language product queries** into MongoDB queries and displays the top matching products (from a historical dataset scraped from Flipkart via Kaggle).

> ⚠️ **Note**: This app is for **educational purposes**. The product data is outdated and taken from open-source Kaggle datasets.
---

> Click to see Demo Video

[![Demo Video](https://drive.google.com/uc?export=view&id=1cH_GE-BypxjS2RCOx7Z1Roa7BesQsm_-)](https://drive.google.com/file/d/1OlrF2UwoAkgo7zDtGoFy03CWaEBekv3N/view)
---


## 🚀 Features

- 🔍 Natural language to MongoDB query conversion
- 🧠 Powered by Google Gemini (`gemini-1.5-flash`)
- 💬 LangChain prompt templates for query generation
- 🧾 Connects to MongoDB and fetches real product details
- 📦 Displays product info like name, price, discount, description
- 🌐 Hosted via **pyngrok** for public access (local tunneling)
- ⚙️ Custom HTML/CSS cards in Streamlit

---

## 🧠 How it Works

1. **User enters** a query like: `Show me women's shorts under ₹500`
2. The query is passed to **Gemini** using **LangChain**
3. Gemini returns a **MongoDB filter object**
4. The app queries MongoDB and renders the result as product cards

---

## 🛠️ Tech Stack

| Component        | Technology |
|------------------|------------|
| Frontend         | Streamlit  |
| Backend/Logic    | Python, LangChain, Gemini API |
| LLM             | Google Gemini 1.5 Flash |
| Database         | MongoDB (Cloud or Local) |
| Tunneling        | pyngrok    |

---

## 📂 File Structure

├── app.py

├── tunnel.py

├── requirements.txt

├── .env

├── flipkartlogo.png

---

## 🔐 .env Format

Create a `.env` file in the root directory with the following keys:

```env
GOOGLE_API_KEY=your_google_generative_ai_key
MONGO_URI=your_mongodb_connection_uri
NGROK_TOKEN=your_ngrok_token
```

---

## 🧪 Setup Instructions


Clone the repo
```
git clone https://github.com/AryanJNayak/FlipkartAssistant.git
cd FlipkartAssistant
```

Install dependencies
```
pip install -r requirements.txt
```

Run the app
```
python tunnel.py
```
This will start Streamlit and create a public URL using ngrok.

---

## 🧠 Example Queries
```
Show me cycling shorts for women below 500

I want crystal paper weights

Show Alisha brand products

I am Indian women, Find something which i wear in traditional festival.
```

---


## 📌 Dataset Source
Products were scraped from Flipkart and are available on Kaggle [Flipkart Products](https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products).

---

## 🙋‍♂️ Author
Aryan Nayak
