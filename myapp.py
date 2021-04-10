
from functions import *
#====Initialize====#
window = tk.Tk()
window.geometry("1000x800")
window.title("Mini Project: A Badminton Ladder")

#=======Title=======#
title = tk.Label(text="A Badminton Ladder",  font=("Times New Roman", 30))
title.grid(pady=5)

#=======Ladder Ranking=======#
Ladder_label = tk.Label(text="Ranking", font=("Times New Roman", 20))
Ladder_label.grid(column=6, row=1, pady=5)
Ladder = ttk.Treeview(window)
Ladder.grid(column=6, row=2, padx=20)

Ladder['columns'] = ("Rank", "Name")

Ladder.heading('#0', text='', anchor=CENTER)
Ladder.heading("Rank", text="Rank", anchor=CENTER)
Ladder.heading("Name", text="Name", anchor=CENTER)

Ladder.column('#0', width=0, stretch=NO)
Ladder.column("Rank", width="60", anchor=CENTER)
Ladder.column("Name", width="120", anchor=CENTER)

#=======Upcoming Matches=======#
upcoming_match_tree_label = tk.Label(text="Upcoming Matches", font=("Times New Roman", 20))
upcoming_match_tree_label.grid(column=0, row=1, pady=5)
upcoming_match_tree = ttk.Treeview(window)
upcoming_match_tree.grid(column=0, row=2, columnspan=5)

upcoming_match_tree['columns'] = ("ID", "Player1", "VS", "Player2", "Date")

upcoming_match_tree.heading('#0', text='', anchor=CENTER)
upcoming_match_tree.heading("ID", text="ID", anchor=CENTER)
upcoming_match_tree.heading("Player1", text="Player1", anchor=CENTER)
upcoming_match_tree.heading("VS", text="VS", anchor=CENTER)
upcoming_match_tree.heading("Player2", text="Player2", anchor=CENTER)
upcoming_match_tree.heading("Date", text="Date", anchor=CENTER)

upcoming_match_tree.column('#0', width=0, stretch=NO)
upcoming_match_tree.column("ID", width="60", anchor=CENTER)
upcoming_match_tree.column("Player1", width="120", anchor=CENTER)
upcoming_match_tree.column("VS", width="120", anchor=CENTER)
upcoming_match_tree.column("Player2", width="120", anchor=CENTER)
upcoming_match_tree.column("Date", width="80", anchor=CENTER)

upcoming_match_scroll = Scrollbar(window)
upcoming_match_scroll.grid(column=5, row=2)
upcoming_match_tree.configure(yscrollcommand=upcoming_match_scroll.set)
upcoming_match_scroll.configure(command=upcoming_match_tree.yview)

#=======Buttons=======#
btn_frame = Frame(window, width=1000, height=60, bg="grey")
btn_frame.grid(row=3, column=0,sticky=NSEW)

button1 = tk.Button(btn_frame,text="Register", bg="green", command=registerPlayerList)
button1.grid(row=2, column=1, padx=5) 

button2 = tk.Button(btn_frame,text="Withdraw", bg="red", command=withdrawPlayerList)
button2.grid(row=2, column=2, padx=5)

button3 = tk.Button(btn_frame,text="Issue Challenge", bg="yellow", command=issueChallenge)
button3.grid(row=2, column=3, padx=5)


window.mainloop()
