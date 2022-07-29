
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
    # Implement the default Matplotlib key bindings.
from matplotlib.figure import Figure


if __name__ == "__main__":
    def _quit1():
        results.quit()     
    
    def _quit2():
        graph.quit()    
        graph.destroy()
        results.destroy()

    infile=open('Results.txt', 'r')
    resultados = infile.readlines()
    infile.close()

    results = tkinter.Tk()
    results.title("Drone Performance")

    for i in range(len(resultados)):
        greeting = tkinter.Label(text=resultados[i], font=('Helvetica bold',15))
        greeting.pack()

    button1 = tkinter.Button(master=results, text="Show graph", command = _quit1)
    button1.pack(side=tkinter.BOTTOM)

    tkinter.mainloop()

    ##################
    infile=open('outputs.txt', 'r')                     ##These commands open
    f=infile.readlines()                                  ##the file where
    c=f[0]                                                ##the waypoint
    y=c.split(",")                                    ##locations were stored
    infile.close()

    vel = []
    for i in range (1,len(y)-1):
        vel.append(float(y[i]))

    time=np.arange(0,len(vel),1)

    graph = tkinter.Tk()
    graph.title("Graph")

    fig = Figure(figsize=(9, 6), dpi=100)
    grafico = fig.add_subplot(111)
    grafico.plot(time,vel)
    grafico.set_title('Instantaneous Speed')
    grafico.set_xlabel('Time (s)')
    grafico.set_ylabel('Speed (m/s)')
    grafico.grid()

    canvas = FigureCanvasTkAgg(fig, master=graph)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, graph)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    button2 = tkinter.Button(master=graph, text="Quit", command=_quit2)
    button2.pack(side=tkinter.BOTTOM)

    tkinter.mainloop()


