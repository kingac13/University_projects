from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

#interfejs
root=Tk()
root.title("Figures")
root.geometry("400x250")
#root.resizable(0,0)


def buttom(item):
    """Funkcja przyjmująca stringa, która dodaje go na koniec expression field"""
    function_field.insert('end',item)

def clear():
    """Funkcja czyszcząca wszystkie okna w które wpisujemy dane oraz wykresy """
    equation.set("")
    x_min_val.delete(0, END)
    x_max_val.delete(0, END)
    y_min_val.delete(0, END)
    y_max_val.delete(0, END)

equation=StringVar()
legend_value = IntVar()

#okna do wpisywania wartości
l0 = Label(root, text='Function: ').grid(row=6, column=20)
function_field = Entry(root, textvariable=equation)
function_field.grid(column=21, row=6)
x_min_label=Label(root, text='x_min:').grid(column=20,row=7)
x_min_val=Entry(root,width=13)
x_min_val.grid(column=21, row=7, sticky=W, columnspan=2)
x_max_label=Label(root, text='x_max:').grid(column=20, row=8)
x_max_val=Entry(root, width=13)
x_max_val.grid(column=21,row=8, sticky=W, columnspan=2)
y_min_label=Label(root, text='y_min:').grid(column=20, row=9)
y_min_val=Entry(root, width=13)
y_min_val.grid(column=21, row=9, sticky=W, columnspan=2)
y_max_label=Label(root, text='y_max:').grid(column=20, row=10)
y_max_val=Entry(root, width=13)
y_max_val.grid(column=21, row=10, sticky=W, columnspan=2)

#przyciski funkcyjne
plot=Button(root, text='Plot', command=lambda: [function_plotting()]).grid(row=11, column=16)
clear_button = Button(root, text='Clear', command=clear).grid(row=12, column=16)
quit_button=Button(root, text="End", command=quit).grid(column=16, row=13)
legend_button = Checkbutton(root, text='legenda', variable= legend_value, onvalue=1, offvalue=0).grid(column=16, row=14, columnspan=2)

#przyciski matematyczne
addition=Button(root, text='+', height=1, width=7, command=lambda:buttom('+'), bg = "#CC99FF").grid(row=6, column=2)
subtraction=Button(root, text='-', height=1, width=7, command=lambda:buttom('-'), bg = "#CC99FF").grid(row=6, column=3)
multiplication=Button(root, text='*', height=1, width=7, command=lambda:buttom('*'), bg = "#CC99FF").grid(row=6, column=4)
division=Button(root, text='/', height=1, width=7, command=lambda:buttom('/'), bg = "#CC99FF").grid(row=7, column=2)
sinus=Button(root, text='sin', height=1, width=7, command=lambda:buttom('sin'), bg = "#CC99FF").grid(row=8, column=4)
cosinus=Button(root, text='cos', height=1, width=7, command=lambda:buttom('cos'), bg = "#CC99FF").grid(row=9, column=2)
logartym=Button(root, text='ln', height=1, width=7, command=lambda:buttom('ln'), bg = "#CC99FF").grid(row=8, column=2)
exponenta=Button(root, text='e', height=1, width=7, command=lambda:buttom('e'), bg = "#CC99FF").grid(row=8, column=3)
left_parenthesis=Button(root, text='(', height=1, width=7, command=lambda:buttom('('), bg = "#CC99FF").grid(row=7, column=3)
right_parenthesis=Button(root, text=')', height=1, width=7, command=lambda:buttom(')'), bg = "#CC99FF").grid(row=7, column=4)
x_1=Button(root, text='x', height=1, width=7, command=lambda:buttom('x'), bg = "#CC99FF").grid(row=9, column=3)
power=Button(root, text='^', height=1, width=7, command=lambda:buttom('^'), bg = "#CC99FF").grid(row=9, column=4)
power=Button(root, text='\u03C0', height=1, width=7, command=lambda:buttom('\u03C0'), bg = "#CC99FF").grid(row=10, column=2)

zero=Button(root, text='0', height=1, width=7, command=lambda:buttom('0'), bg = "#FF99FF").grid(row=11, column=2)
one=Button(root, text='1', height=1, width=7, command=lambda:buttom('1'), bg = "#FF99FF").grid(row=11, column=3)
two=Button(root, text='2', height=1, width=7, command=lambda:buttom('2'), bg = "#FF99FF").grid(row=11, column=4)
three=Button(root, text='3', height=1, width=7, command=lambda:buttom('3'), bg = "#FF99FF").grid(row=12, column=2)
four=Button(root, text='4', height=1, width=7, command=lambda:buttom('4'), bg = "#FF99FF").grid(row=12, column=3)
five=Button(root, text='5', height=1, width=7, command=lambda:buttom('5'), bg = "#FF99FF").grid(row=12, column=4)
six=Button(root, text='6', height=1, width=7, command=lambda:buttom('6'), bg = "#FF99FF").grid(row=13, column=2)
seven=Button(root, text='7', height=1, width=7, command=lambda:buttom('7'), bg = "#FF99FF").grid(row=13, column=3)
eight=Button(root, text='8', height=1, width=7, command=lambda:buttom('8'), bg = "#FF99FF").grid(row=13, column=4)
nine=Button(root, text='9', height=1, width=7, command=lambda:buttom('9'), bg = "#FF99FF").grid(row=14, column=2)
semicolon=Button(root, text=';', height=1, width=7, command=lambda:buttom(';'), bg="#9999FF").grid(row=14, column=3)


symbols_math = {'\u03C0': 'np.pi', 'e': 'np.e', 'ln' : 'np.log', '^' : '**', 'sin' : 'np.sin', 'cos' : 'np.cos', 'ctg' : '1/np.tan', 'tg' : 'np.tan'}



def function_plotting():
    """Funkcja odpowiednio przetwarza stringa ze wzorem funkcji na funkcje 
    zrozumiałe dla komputera (np. np.sin), liczy wartości funkcji na wskazanej dziedzienie,
    rysyje wykresy nqa płotnie oraz sprawdza czy odawać legendę na wykres sprawdza
    czy na wykresie ma znajdować się legenda"""
    try:
        new=function_field.get()
        for key, value in symbols_math.items():
                new = new.replace(key, value)
        functions=new.split(';')
        xmin = int(x_min_val.get())
        xmax = int(x_max_val.get())
        ymin = int(y_min_val.get())
        ymax = int(y_max_val.get())
        fr_plot = Frame(root)
        fr_plot.grid(row=3, column=8, sticky=N+S, rowspan=20)
        figure1 = plt.figure(figsize=(5,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        plt.axis([xmin,xmax,ymin,ymax])
        canvas = FigureCanvasTkAgg(figure1, fr_plot)
        canvas.get_tk_widget().pack(side=LEFT, fill=BOTH)
        for function in functions:
            xs = np.linspace(xmin, xmax, (xmax-xmin)*10)
            ys = [eval(function) for x in xs]
            ax1.plot(xs,ys, label=f'{function}')
        plt.xlabel('x')
        plt.ylabel('y')
        if legend_value.get() == 1:
            plt.legend()
    except:
        messagebox.showwarning("Warning!","Invalid function formula")



root.mainloop()


