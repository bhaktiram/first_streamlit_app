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


#create repeatable code block call function
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#create new section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
        streamlit.error()
        
#without function process

#streamlit.header("Fruityvice Fruit Advice!")

#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)

#try:
#    fruit_choice = streamlit.text_input('What fruit would you like information about')
#    if not fruit_choice:
#      streamlit.error("Please select a fruit to get information")
#    else: 
#      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#      streamlit.dataframe(fruityvice_normalized)
#except URLError as e:
#      streamlit.error() 
        
# dont run anything past here
   #streamlit.stop

#normal code without button
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
##my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
##my_data_row = my_cur.fetchone()
#my_data_rows = my_cur.fetchall()
##streamlit.text("The Fruitload Container")
#streamlit.header("The Fruitload Container")
##streamlit.text(my_data_row)
#streamlit.dataframe(my_data_rows)

#using button
streamlit.header("The Fruitload list Container")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
         return my_cur.fetchall()
    
#add a button to fruit load list
if streamlit.button('Get the Fruit Load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#add insert function withbutton    
def insert_row_snowflake(new_fruit):    
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into pc_rivery_db.public.fruit_load_list Values('" + new_fruit +"')")
         return 'Thanks for adding ' + new_fruit 
    
    
add_my_fruit = streamlit.text_input('What fruit would you like add')
if streamlit.button('add a fruit to list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

# adding new table and showing what user has selected in text
#streamlit.header("Fruityvice Fruit Advice!")
#add_my_fruit = streamlit.text_input('What fruit would you like add')
#streamlit.write('The user entered ')

# inserting values from streamlite
#streamlit.write('Thanks for adding ', add_my_fruit)
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list Values('from streamlit')")
