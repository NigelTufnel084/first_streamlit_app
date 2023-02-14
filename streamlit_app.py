
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')

streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Tange Egg')
streamlit.text('🥑 🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝 🍇')



my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

# Lets put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table 
streamlit.dataframe(fruits_to_show)

#Create function in Streamlit
def get_fruityvice_data (this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  
    return fruityvice_normalized;

# New section to display fruitvice api response 
streamlit.header('Fruityvice fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:    
    #take the JSON version of the response and normalize it
    back_from_function  = get_fruityvice_data(fruit_choice)
    #output it the screen as a table
    streamlit.dataframe(back_from_function)

streamlit.header("The fruit list contains:")   
#Snowflake-related functions
def get_fruit_load_list():
    with my_cur = my_cnx.cursor()
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = my_cur.fetchall()
    streamlit.dataframe(my_data_rows)


except URLError as e:
    streamlit.error()
    
#LEGACY CODE
#streamlit.header('Fruityvice fruit Advice!')
#fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
#streamlit.write('The user entered', fruit_choice)
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#take the JSON version of the response and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it the screen as a table
#streamlit.dataframe(fruityvice_normalized)


#don't run....troubleshooting

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to  add?')
streamlit.write('Thanks for adding', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')" )
