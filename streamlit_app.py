import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError 
streamlit.title('My Parent New Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & bloobery oatmeal')
streamlit.text('🥗 Kale, Spinach, Rocket Smoothie')
streamlit.text('🐔 Hard boiled free range egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.dataframe(my_fruit_list)

my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
# Display the table on the page.
#streamlit.dataframe(my_fruit_list)
##streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))


fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")

#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)
try:
fruit_choice = streamlit.text_input('What fruit would you like information about?')
if not fruit_choice:
streamlit.error("Please select a fruit to get information") 
else 
#streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruityvice_response.json())
# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)
except URLError as e:
streamlit.error() 

# dont run anything past here
#streamlit.stop

import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
#streamlit.text("The Fruitload Container")
streamlit.header("The Fruitload Container")
#streamlit.text(my_data_row)
streamlit.dataframe(my_data_rows)

## adding new table and showing what user has selected in text

streamlit.header("Fruityvice Fruit Advice!")
add_my_fruit = streamlit.text_input('What fruit would you like add')
streamlit.write('The user entered ')

## inserting values from streamlite
streamlit.write('Thanks for adding ', add_my_fruit)
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list Values('from streamlit')")



