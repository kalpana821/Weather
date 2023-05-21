# this line is for import and move to next template and take request form
from flask import Flask, render_template, request
import requests, json
# this is for datetime with this we can get date time
from datetime import datetime
# in another file we can create database, table, insert that we can call
from db_connect_1 import * 

import mysql.connector as conn
import pymongo 
# client = pymongo.MongoClient("mongodb+srv://kalpanap821:kallu821@cluster0.gr1htc2.mongodb.net/?retryWrites=true&w=majority")
# db = client.test
# database_name=client['weather']
# collection_name=database_name['weather_report']
# Creating connection object

# we can give details of sql
mydb = conn.connect(host = "127.0.0.1",user = "root",password = "kallu821", database='weather_1')
print(mydb)

#Creating a cursor object using the cursor() method
cursor = mydb.cursor()

dataBaseName = "weather_1"
tb_name = "Report"

# create_db(cursor,dataBaseName)
# create_table(cursor,tb_name)
app = Flask(__name__)
# The route() function of the Flask class is a decorator, which tells the application which URL should call the associated function
@app.route('/', methods=['POST','GET'])  
def index():
      # it will return first page  
      return render_template("weather.html")  



# this line is for next for request 
@app.route("/review", methods=['POST','GET'])
def results():
    #    return render_template("results_1.html")
        if request.method == "POST":
            try: 
                api_key = "15ff3213dcf1f610b5739e1803d48de1"
                base_url = "http://api.openweathermap.org/data/2.5/weather?"
                city_name = request.form["content"]
                complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                # print("complete_url")
                response = requests.get(complete_url)

                # t = response.json()['data']['timelines'][0]['intervals'][0]['values']['temperature']
                x = response.json()
                reviews=[]
                if x["cod"] != "city":
                   
                    try:
                       y = x["main"]
                       current_temperature = y["temp"]
                    except:
                        print("temparature not found")
                    try:
                        Celsius = (y["temp"] - 273.15)
                    except:
                        print("celsius not found")
                    try:

                       current_pressure = y["pressure"]
                    except:
                        print("pressure not found")
                    try:
                        current_humidity = y["humidity"]
                    except:
                        print("humidity not found")
                    try:
                        date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
                    except:
                        print("date time not found")
                    try:
                        z = x["weather"]
                        weather_description = z[0]["description"]
                    except:
                        print("weather desc not found")
 
                    # print("Temperature (in kelvin unit) = " +
                    #           str(current_temperature) +
                    #      "\n tempaparature in celsius = " +
                    #           str(Celsius)+
                    #      "\n atmospheric pressure (in hPa unit) = " +
                    #           str(current_pressure) +
                    #      "\n humidity (in percentage) = " +
                    #           str(current_humidity) +
                    #      "\n date_time = " +
                    #          str(date_time) +
                    #      "\n description = " +
                    #          str(weather_description))
                    
                    mydict = {"current_temperature":current_temperature,'Celsius':Celsius,"current_pressure":current_pressure,"current_humidity":current_humidity,"date_time":date_time,"weather_description":weather_description}
                    reviews.append(mydict)
                insert_query   = f"INSERT INTO {tb_name}(current_temperature, Celsius, current_pressure, current_humidity, date_time, weather_description) VALUES (%(current_temperature)s, %(Celsius)s, %(current_pressure)s, %(current_humidity)s, %(date_time)s, %(weather_description)s);"
                print(cursor.executemany(insert_query, reviews))
                mydb.commit()
                # collection_name.insert_many(reviews) 
                
                return render_template('results_1.html', reviews=reviews[0:2])
            except:
              pass
            return render_template("results_1.html")
        else:
            print("not found")
if __name__ == '__main__':  
   app.run(debug=True)