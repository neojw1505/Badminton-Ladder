import tkinter
from tkinter import *
from tkinter import ttk

data = {
    1:{'passport':"38123122",'Fullname':"Allahu AKhbra", "DOb":'10-mar-1984'},
    2:{'passport':"1175312",'Fullname':"JOHN AKhbra", "DOb":'10-mar-1984'},
    3:{'passport':"523123122",'Fullname':"BAKAR AKhbra", "DOb":'10-mar-1984'},
    4:{'passport':"86723122",'Fullname':"MATE AKhbra", "DOb":'10-mar-1984'},
    5:{'passport':"33223122",'Fullname':"SUAC AKhbra", "DOb":'10-mar-1984'},
    6:{'passport':"86724122",'Fullname':"EKSI AKhbra", "DOb":'10-mar-1984'},
    7:{'passport':"1412122",'Fullname':"LOBA AKhbra", "DOb":'10-mar-1984'},
    8:{'passport':"7634122",'Fullname':"TOTO AKhbra", "DOb":'10-mar-1984'},
    9:{'passport':"41233122",'Fullname':"SHINA AKhbra", "DOb":'10-mar-1984'},
}
root = Tk()
root.geometry("600x500")

column = ['passport','Fullname',"DOb"]

tree_Frame = Frame(root)
tree_Frame.place(x=10,y=50, width =500, height=300)
myTree = ttk.Treeview(tree_Frame,)
myTree["columns"] = column

for i in column:
    myTree.column(i, width=80)
    myTree.heading(i, text=i.capitalize())
myTree['show'] = "headings"       
myTree.pack() 

for k,v in data.items():
    myTree.insert(parent="",index=END, values=(k,v['passport'],v['Fullname'],v['DOb']))

def filterFirstName(*args):
    ItemsOnTreeView = myTree.get_children()
    search = search_ent_var.get().capitalize()
    for eachItem in ItemsOnTreeView:
        print(eachItem)
        if search in myTree.item(eachItem)['values'][2]:
            search_var = myTree.item(eachItem)['values']
            myTree.delete(eachItem)
            myTree.insert("",0,values=search_var)    

search_ent_var = StringVar()

search_by = ttk.Combobox(root, values = column)
search_by.current(2)
search_by.grid(row =0, column=0)

search_ent = Entry(root, textvariable = search_ent_var)
search_ent.grid(row=0, column=1,padx=10)

search_ent_var.trace("w", filterFirstName)

root.mainloop()    
