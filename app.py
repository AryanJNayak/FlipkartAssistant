import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import re
import json
import pymongo

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
MONGO_URI = os.getenv('MONGO_URI')
# print(MONGO_URI, '\n',GOOGLE_API_KEY)

# For llm '{ ' => '{{' (to use single curley bracs append one more)
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')
database_schema = """
  "_id": {{
      "tyep":"object",
      "description":"mongodb db object id - uniquely identify rows"
  }},
  "uniq_id":{{
      "type":"string",
      "description":"product unique id from flipkart"
  }},
  "crawl_timestamp":{{
      "type":"string",
      "description":"scraped time when this product is scrapped"
  }},
  "product_url":{{
      "type":"string",
      "description":"link of the product"
  }},
  "product_name":{{
      "type":"string",
      "description":"name of the product"
  }},
  "product_category_tree":{{
      "type":"string",
      "description":"category of product."
  }},
  "pid":{{
      "type":"string",
      "description":"product id"
  }},
  "retail_price":{{
      "type":"string",
      "description":"price/cost of product"
  }},
  "discounted_price":{{
      "type":"string",
      "description":"discounted price"
  }},
  "image(link)":{{
      "type":"string",
      "description":"image link of product"
  }},
  "is_FK_Advantage_product":{{
      "type":"string",
      "description":"describe the advantage of product"
  }},
  "description":{{
      "type":"string",
      "description":"the details description of product"
  }},
  "product_rating":{{
      "type":"string",
      "description":"rating of product"
  }},
  "overall_rating":{{
      "type":"string",
      "description":"overall rating including price, reviwes etc."
  }},
  "brand":{{
      "type":"string",
      "description":"brand's name"
  }},
  "product_specifications":{{
      "type":"string",
      "description":"other details"
  }},
"""

example_rows = """
{{
	_id : 68540b195bc9aac1c51405e8,
	uniq_id : bc940ea42ee6bef5ac7cea3fb5cfbee7,
	crawl_timestamp : 2016-03-25 22:59:23 +0000,
	product_url : http://www.flipkart.com/sicons-all-purpose-arnica-dog-shampoo/p/itmeh3zyw2vhgsp5?pid=PSOEH3ZYDMSYARJ5,
	product_name : Sicons All Purpose Arnica Dog Shampoo,
	product_category_tree : ["Pet Supplies >> Grooming >> Skin & Coat Care >> Shampoo >> Sicons All Purpose Arnica Dog Shampoo (500 ml)"],
	pid : PSOEH3ZYDMSYARJ5,
	retail_price : 220.0,
	discounted_price : 210.0,
	image : ["http://img5a.flixcart.com/image/pet-shampoo/r/j/5/sh-df-14-sicons-500-1100x1100-imaeh3hfvav85tva.jpeg", "http://img5a.flixcart.com/image/pet-shampoo/r/j/5/sh-df-14-sicons-500-original-imaeh3hfvav85tva.jpeg"],
	is_FK_Advantage_product : False,
	description : Specifications of Sicons All Purpose Arnica Dog Shampoo (500 ml) General Pet Type Dog Brand Sicons Quantity 500 ml Model Number SH.DF-14 Type All Purpose Fragrance Arnica Form Factor Liquid In the Box Sales Package ,Shampoo Sicons Dog Fashion Arnica,
	product_rating : No rating available,
	overall_rating : No rating available,
	brand : Sicons,
	product_specifications :
    {{
      "product_specification"=>
      [
        {{"key"=>"Pet Type", "value"=>"Dog"}},
        {{"key"=>"Brand", "value"=>"Sicons"}},
        {{"key"=>"Quantity", "value"=>"500 ml"}},
        {{"key"=>"Model Number", "value"=>"SH.DF-14"}},
        {{"key"=>"Type", "value"=>"All Purpose"}},
        {{"key"=>"Fragrance", "value"=>"Arnica"}},
        {{"key"=>"Form Factor", "value"=>"Liquid"}},
        {{"key"=>"Sales Package", "value"=>"Shampoo Sicons Dog Fashion Arnica"}}
      ]
    }}
}}
,
{{
	_id : 68540b195bc9aac1c51405e9,
	uniq_id : c2a17313954882c1dba461863e98adf2,
	crawl_timestamp : 2016-03-25 22:59:23 +0000,
	product_url : http://www.flipkart.com/eternal-gandhi-super-series-crystal-paper-weights-silver-finish/p/itmeb7h2hrfgutxb?pid=PWTEB7H2E4KCYUE3,
	product_name : Eternal Gandhi Super Series Crystal Paper Weights  with Silver Finish,
	product_category_tree : ["Eternal Gandhi Super Series Crystal Paper Weight..."],
	pid : PWTEB7H2E4KCYUE3,
	retail_price : 430.0,
	discounted_price : 430.0,
	image : ["http://img5a.flixcart.com/image/paper-weight/u/e/3/eternal-gandhi-gandhi-paper-weight-mark-v-1100x1100-imaeb8adyf3xmqhf.jpeg", "http://img5a.flixcart.com/image/paper-weight/u/e/3/eternal-gandhi-gandhi-paper-weight-mark-v-original-imaeb8adyf3xmqhf.jpeg"],
	is_FK_Advantage_product : False,
	description : Key Features of Eternal Gandhi Super Series Crystal Paper Weights  with Silver Finish Crystal  paper weight Product Dimensions :   8cm x  8cm x 5cm A beautiful product Material: Crystal,Eternal Gandhi Super Series Crystal Paper Weights  with Silver Finish (Set Of 1, Clear) Price: Rs. 430 Your office desk will sparkle and shine when you accent tables with this elegant crystal paper weight. The multifaceted crystal features Gandhiji’s bust and his timeless message – “My life is my message – M.K. Gandhi”. A beautiful product to gift to your near and dear ones in family and Business.,Specifications of Eternal Gandhi Super Series Crystal Paper Weights  with Silver Finish (Set Of 1, Clear) General Model Name Gandhi Paper Weight Mark V Dimensions Weight 323 g In the Box Paper Weight Paper Weight Features Paper Weight Material Crystal Paper Weight Finish Silver Finish,
	product_rating : No rating available,
	overall_rating : No rating available,
	brand : Eternal Gandhi,
	product_specifications :
  {{
    "product_specification"=>
    [
      {{"key"=>"Model Name", "value"=>"Gandhi Paper Weight Mark V"}},
      {{"key"=>"Weight", "value"=>"323 g"}},
      {{"value"=>"Paper Weight"}},
      {{"key"=>"Paper Weight Material", "value"=>"Crystal"}},
      {{"key"=>"Paper Weight Finish", "value"=>"Silver Finish"}}
    ]
  }}
}}
,
{{
	_id : 68540b195bc9aac1c51405ea
	uniq_id : ce5a6818f7707e2cb61fdcdbba61f5ad,
	crawl_timestamp : 2016-03-25 22:59:23 +0000,
	product_url : http://www.flipkart.com/alisha-solid-women-s-cycling-shorts/p/itmeh2ftwkzykhcg?pid=SRTEH2FVVKRBAXHB,
	product_name : Alisha Solid Women's Cycling Shorts,
	product_category_tree : ["Clothing >> Women's Clothing >> Lingerie, Sleep & Swimwear >> Shorts >> Alisha Shorts >> Alisha Solid Women's Cycling Shorts"],
	pid : SRTEH2FVVKRBAXHB,
	retail_price : 1199.0,
	discounted_price : 479.0,
	image : ["http://img6a.flixcart.com/image/short/p/j/z/altght4p-26-alisha-38-original-imaeh2d5cqtxe5gt.jpeg", "http://img5a.flixcart.com/image/short/z/j/7/altght-7-alisha-38-original-imaeh2d5jsz2ghd6.jpeg", "http://img5a.flixcart.com/image/short/p/j/z/altght4p-26-alisha-38-original-imaeh2d5kbufss6n.jpeg", "http://img5a.flixcart.com/image/short/p/j/z/altght4p-26-alisha-38-original-imaeh2d5npdybzyt.jpeg", "http://img6a.flixcart.com/image/short/x/5/f/altght-2-alisha-36-original-imaeh2d5xnueazgz.jpeg"],
	is_FK_Advantage_product : False,
	description : Key Features of Alisha Solid Women's Cycling Shorts Cotton Lycra Navy, Red, White, Red,Specifications of Alisha Solid Women's Cycling Shorts Shorts Details Number of Contents in Sales Package Pack of 4 Fabric Cotton Lycra Type Cycling Shorts General Details Pattern Solid Ideal For Women's In the Box 4 shorts Additional Details Style Code ALTGHT4P_26 Fabric Care Gentle Machine Wash in Lukewarm Water, Do Not Bleach,
	product_rating : No rating available,
	overall_rating : No rating available,
	brand : Alisha,
	product_specifications :
  {{
    "product_specification"=>
    [
      {{"key"=>"Number of Contents in Sales Package", "value"=>"Pack of 4"}},
      {{"key"=>"Fabric", "value"=>"Cotton Lycra"}},
      {{"key"=>"Type", "value"=>"Cycling Shorts"}},
      {{"key"=>"Pattern", "value"=>"Solid"}},
      {{"key"=>"Ideal For", "value"=>"Women's"}},
      {{"value"=>"4 shorts"}},
      {{"key"=>"Style Code", "value"=>"ALTGHT4P_26"}},
      {{"value"=>"Gentle Machine Wash in Lukewarm Water, Do Not Bleach"}}
      ]
    }}
}}
"""

prompt =f"""
You are goot at writing mongodb query.
Your task is to convert the user query into mongodb querey.
Give ONLY JSON object.
Respond only with raw JSON markdown.
Do NOT wrap output in triple backticks or any markdown.

Schema of product
{database_schema}

EXAMPLE ROWS of product:
{example_rows}

RULES:
  - rating of product is in string not in the form of number.
  - use and operator for combine both field
  - dont use $sort()
  - don't add find(). only give JSON object
"""


Messages = [
        ("system", prompt),
        ("human","{input}")
]

prompt_template = ChatPromptTemplate.from_messages(Messages)

st.title("Flipkart shopping assistant")
st.image("flipkartlogo.png", caption="Flipkart")
st.warning('This is app is build for education purpose. The products data store from kaggle(open-source). The product may not avialable because the data is old and redundent.', icon="⚠️")
user = st.text_input("What You want to buy: ")
if user:
  with st.spinner("Answering..."):

    prompt = prompt_template.invoke({"input":user})
    response = llm.invoke(prompt)
    raw = response.content
    print(raw)

    match = re.search(r'```json\s*(\{[\s\S]*?\})\s*```', raw)
    if not match:
      st.error("Give clear input")

    json_text = match.group(1)

    # Optional: fix double backslashes
    json_text = json_text.replace("\\\\", "\\")

    # 3. Load JSON into dict
    query = json.loads(json_text)
    print(query)

    try:
      client = pymongo.MongoClient(MONGO_URI)
      db = client["GenAI"]
      collection = db['products']
    except:
      st.error("Error while connected with Data Base")

    try:
      output = collection.find(query).limit(5)
      st.success('We found something')
    except:
      st.write("We Couldn't found something")

    cards = []
    for row in output:
      card = {
        "_id" : row['_id'],
        "product_url" : row['product_url'],
        "product_name" : row['product_name'],
        "retail_price" : row['retail_price'],
        "discounted_price" : row['discounted_price'],
        "description" : row['description'],
        "brand" : row['brand'],
      }
      cards.append(card)

    for x in cards:
      print(x)
      st.html(
      f"""
      <div class='card' style='
              width: 100%;
              margin: 0px auto;
              border: 2px solid white;
              text-align: center;
              display: flex;
              justify-content: center;
              align-items: center;
              flex-flow: column;
              border-radius: 20px;
              border-radius: 20px;
              padding: 13px;
            '>

          <div style='
              display: flex;
              width: 100%;
              font-weight: 900;
              align-items: center;
              justify-content: space-around;
            '>

              <div>
                  <p>
                      <span style='
                          margin-right: 26px;
                          font-weight: 900;
                          font-size: 30px;' class='brand'
                        >
                          {x['brand']}
                      </span>
                  </p>
              </div>

              <div style='
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
              '>
                  <p>
                      {x['product_name']}
                  </p>

                  <div style='
                      display: flex;
                      justify-content: space-around;
                      width: 111%;
                      justify-content: space-around;'
                  >
                      <p><span style='text-decoration: line-through;' class='price'>Rs.{x['retail_price']}</span></p>
                      <p><span style='' class='discount'>Rs.{x['discounted_price']}</span></p>
                      <p style=
                          " border: 2px solid;
                            width: 80px;
                            background-color:#2a55e5;">
                          <a style=
                              "text-decoration: none;
                                color: yellow;"
                                class="btn"
                                href="{x['product_url']}"
                                target='_blank'>
                              Flipkart
                          </a>
                      </p>
                  </div>
              </div>

          </div>

          <div style=' border-top: 2px solid white;' >
              <span style='
                    width: 60%;'>
                  <span class='desc'>{x['description']}</span>
              </span>
          </div>


      </div>
      """
      )