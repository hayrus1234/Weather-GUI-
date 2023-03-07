from flask import Flask
import tkinter
import requests
from tkinter import *
from PIL import ImageTk,Image
from io import BytesIO
app = Flask(__name__)
@app.route('/')
def index():
    root = tkinter.Tk()
    root.title("Weather Forecast")
    root.geometry("400x400")
    root.resizable(0,0)

    sky_color="#76c3ef"
    grass_color="#aad207"
    output_color="#dcf0fb"
    input_color="#ecf2ae"
    large_font=('SimSun',14)
    small_font=('SimSun',11)

    #define functions
    '''{"coord":{"lon":78.1667,"lat":11.65},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"base":"stations",
    "main":{"temp":299.79,"feels_like":299.79,"temp_min":299.79,"temp_max":299.79,"pressure":1013,"humidity":39,"sea_level":1013,
    "grnd_level":981},"visibility":10000,"wind":{"speed":2.59,"deg":77,"gust":2.72},"clouds":{"all":1},"dt":1677248228,
    "sys":{"country":"IN","sunrise":1677200725,"sunset":1677243373},"timezone":19800,"id":1257629,"name":"Salem","cod":200}'''    
    def get_weather():
        city_name=response['name']
        city_lat=str(response['coord']['lat'])
        city_lon=str(response['coord']['lon'])

        main_weather=response['weather'][0]['main']
        desc=response['weather'][0]['description']

        temp=str(response['main']['temp'])
        feels_like=str(response['main']['feels_like'])
        temp_min=str(response['main']['temp_min'])
        temp_max=str(response['main']['temp_max'])
        humidity=str(response['main']['humidity'])
    
    #updtae output labels

        city_l.config(text=city_name +"("+city_lat +","+city_lon + ")",font=large_font,bg=output_color)
        weather_l.config(text="Weather:"+main_weather+", "+desc,font=small_font,bg=output_color)
        temp_l.config(text="Temprature:"+temp+" C",font=small_font,bg=output_color)
        feels_l.config(text="Feels Like:"+feels_like+" C",font=small_font,bg=output_color)
        tempmax_l.config(text="Temp Max:"+temp_max+" C",font=small_font,bg=output_color)
        tempmin_l.config(text="Temp Min:"+temp_min+" C",font=small_font,bg=output_color)
        humidity_l.config(text="Humidity:"+humidity,font=small_font,bg=output_color)
    

    def search():
        global response
        #url and my api key
        url='https://api.openweathermap.org/data/2.5/weather'
        api_key='5713131624d4c551043718f4793607b7'
    
        if search_method.get()==1:
            query={'q':city_entry.get(),'appid':api_key,'units':'metric'}
        elif search_method.get()==2:
            query={'zip':city_entry.get(),'appid':api_key,'units':'metric'}

     #call API
        response=requests.request("GET",url,params=query)
        response=response.json()
        get_weather()
        get_icon()
    def get_icon():
        global img
        icon_id=response['weather'][0]['icon']
        url='https://openweathermap.org/img/wn/{icon}.png'.format(icon=icon_id)
        icon_response=requests.get(url,stream=True)
        img_data=icon_response.content
        img=ImageTk.PhotoImage(Image.open(BytesIO(img_data)))


        #update label
        photolabel_l.config(image=img)

    sky_frame=tkinter.Frame(root,bg=sky_color,height=230)
    sky_frame.pack(fill="both",expand=True)
    grass_frame=tkinter.Frame(root,bg=grass_color)
    grass_frame.pack(fill="both",expand=True)
    output_frame=tkinter.LabelFrame(sky_frame,bg=output_color,height=225,width=325)
    output_frame.pack(pady=30)
    output_frame.pack_propagate(0)
    input_frame=tkinter.LabelFrame(grass_frame,bg=input_color,width=325)
    input_frame.pack(pady=15)
    input_frame.pack_propagate(0)

    #output widget 
    city_l=tkinter.Label(output_frame,bg=output_color)
    weather_l=tkinter.Label(output_frame,bg=output_color)
    temp_l=tkinter.Label(output_frame,bg=output_color)
    feels_l=tkinter.Label(output_frame,bg=output_color)
    tempmax_l=tkinter.Label(output_frame,bg=output_color)
    tempmin_l=tkinter.Label(output_frame,bg=output_color)
    humidity_l=tkinter.Label(output_frame,bg=output_color)
    photolabel_l=tkinter.Label(output_frame,bg=output_color)

    city_l.pack()
    weather_l.pack()
    temp_l.pack()
    feels_l.pack()
    tempmax_l.pack()
    tempmin_l.pack()
    humidity_l.pack()
    photolabel_l.pack()
    #apikey=5713131624d4c551043718f4793607b7
    #input_widget
    city_entry=tkinter.Entry(input_frame,width=25,font=small_font)
    city_entry.grid(row=0,column=0,padx=10,pady=10)
    submit_but=tkinter.Button(input_frame,font=large_font,text='Submit',command=search)
    submit_but.grid(row=0,column=1,padx=2,pady=10)
    search_method=IntVar()
    search_method.set(1)
    r1=tkinter.Radiobutton(input_frame,font=small_font,text='Search by city name',variable=search_method,value=1)
    r2=tkinter.Radiobutton(input_frame,font=small_font,text='Search by zipcode',variable=search_method,value=2)
    r1.grid(row=1,column=0,padx=5,pady=(2,10))
    r2.grid(row=1,column=1,padx=0,pady=(2,10))
    root.mainloop()
if __name__ == '__main__':
    app.run()

