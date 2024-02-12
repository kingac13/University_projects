from tkinter import *
import requests
import tkinter
from tkinter import ttk
from bs4 import BeautifulSoup
import requests

def connected_to_internet(url='http://api.nbp.pl', timeout=5):
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.")
    return False

def rate(currency,mode):
    if connected_to_internet():
        #mode 0 - curency to PLN
        #mode 1 - PLN to currency
        url=f'http://api.nbp.pl/api/exchangerates/rates/A/{currency}/'
        data=requests.get(url)
        soup=BeautifulSoup(data.text,'lxml')
        data=soup.find("p").getText()
        print(data)
        exchange_rate=eval(data)["rates"][0]["mid"]

        
        if mode==0:
            return exchange_rate
        if mode == 1:
            return 1/exchange_rate
    else:
        f=open("plik_pomocniczy.txt",'r')
        lista=f.readlines() #robimy listę z linijek
        f.close
        st=''.join(lista) #robimy stringa z tej listy
        print(st)
        y=st.split(" ")#dzielimy stringa wzgledem spacji
        x=list(y) #robimy liste ze stringa
        print(x)
        

        currency_name=x.index('\n'+currency)
        #print(a)
        exchange_rate=x[currency_name+1] #indeks+1 bo bierzemy kurs a nie nazwe
        if mode==0:
            return float(exchange_rate)
        if mode == 1:
            return 1/float(exchange_rate)

            
def converter(input, output, amount):
    if input!="PLN" and output!="PLN":
        return round(amount*rate(input,0)*rate(output,1),2)
    if input=="PLN" and output=="PLN":
        return round(amount,2) 
    if input=="PLN":
        return round(amount*rate(output,1),2)
    if output=="PLN":
        return round(amount*rate(input,0),2)
          

waluty=["PLN", "THB", "USD", "AUD", "HKD", "CAD", "NZD", "SGD", "EUR", "HUF", "CHF", "GBP", "UAH", "JPY", "CZK", "DKK", "ISK", "NOK", "SEK", "HRK", "RON", "BGN", "TRY", "ILS", "CLP", "PHP", "MXN", "ZAR", "BRL", "MYR", "IDR", "INR", "KRW", "CNY", "XDR"]
waluty_1=sorted(waluty)
def main_function():
    global myLabel
    new_value=value.get()
    convert=converter(default1.get(), default2.get(), float(new_value))
    myLabel=tkinter.Label(root, text=convert)
    myLabel.grid(row=1,column=3,sticky=W)

    
   
def clear():
    value.delete(0, END)
    myLabel.grid_forget()


root=Tk()
root.title("Currency Converter")
root.geometry('500x200')
root.resizable(0,0) # usuwa przyciski zmieniania wielkosci 
root.config(bg='#CCCCFF')
root.resizable(width=False, height=False)

Label(root, text='Primary currency:',bg = "pink").grid(row=0,column=0,sticky=W)
Label(root, text='How much:',bg = "pink").grid(row=0,column=1,sticky=W)
Label(root, text='Final currency: ',bg = "pink").grid(row=0,column=2,sticky=W)
Label(root, text='After calculation:',bg = "pink").grid(row=0,column=3,sticky=W)

default1=tkinter.StringVar(root)
default1.set("PLN")
w = ttk.Combobox(root, textvariable=default1, values=tuple(waluty_1))
w.grid(row=1,column=0,sticky=W)
default2=tkinter.StringVar(root)
default2.set("PLN")
w2 = ttk.Combobox(root, textvariable=default2, values=tuple(waluty_1))
w2.grid(row=1,column=2,sticky=W)

value=tkinter.Entry(root)
value.grid(row=1,column=1,sticky=W)

value1=tkinter.Entry(root)
value1.grid(row=1,column=3,sticky=W)


button=tkinter.Button(root, text="Calculate",bg = "pink", command=main_function)
button.grid(row=2,column=2,sticky=W)


button_clear=tkinter.Button(root, text="Clear",bg = "pink", command=clear)
button_clear.grid(row=4,column=2,sticky=W)

exit_button=Button(root, text="End",bg = "pink", command=root.destroy)
exit_button.grid(row=5,column=2,sticky=W)


root.mainloop()
