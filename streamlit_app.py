import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🍓Build Your Own Fruit Smoothie🥝🍇')
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick Some Fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#import requests
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
#streamlit.text(fruityvice_response.json()) #just writes the data to the screen

# New Section to display fruitvice api response
streamlit.header('Fruityvice Fruit Advice!')

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
if not fruit_choice:
  streamlit.error("Please select a Fruit to get Information.")
else:
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  # takes the json version of the response and normalize it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  # Output to the screen as table
  streamlit.dataframe(fruityvice_normalized)
  
except URLError as e:  
  streamlit.error()
  #streamlit.write('The user entered ', fruit_choice)

# Dont run anything past here while we troubleshoot
streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
# my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit Load List:")
# streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

#Allow the end user to add a fruit to list

add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for Adding  ', add_my_fruit)

#Adding insert query in code
my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('from streamlit')")
