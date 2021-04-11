
from functions import *

#====Initialize====#
window = tk.Tk()
window.geometry("1000x800")
window.title("Mini Project: A Badminton Ladder")

#=======Refresh Buttons=======#
def refreshUpcomingMatch():
    if os.path.getsize("upcoming_match.txt") > 0:
        file = open("upcoming_match.txt", "r")
        contents = file.read()
        upcoming_match = ast.literal_eval(contents)
        file.close()
    upcoming_match_tree.delete(*upcoming_match_tree.get_children())
    for id,match in upcoming_match.items():
        upcoming_match_tree.insert(parent='', index='end', text="Parent", values=(id,match['Player1'], match['VS'], match['Player2'], match['Date']))

def refreshLadder():
    Ladder.delete(*Ladder.get_children())
    for rank,player in enumerate(total_players_list):
        Ladder.insert(parent='', index='end', text="Parent", values=(rank+1,player))

#=======Title=======#
title = tk.Label(text="A Badminton Ladder",  font=("Times New Roman", 30))
title.grid(pady=5)

#=======Ladder Ranking=======#
Ladder_label = tk.Label(text="Ranking", font=("Times New Roman", 20))
Ladder_label.grid(column=6, row=1, pady=5)
Ladder = ttk.Treeview(window)
Ladder.grid(column=6, row=2, padx=100)

Ladder['columns'] = ("Rank", "Name")

Ladder.heading('#0', text='', anchor=CENTER)
Ladder.heading("Rank", text="Rank", anchor=CENTER)
Ladder.heading("Name", text="Name", anchor=CENTER)

Ladder.column('#0', width=0, stretch=NO)
Ladder.column("Rank", width="60", anchor=CENTER)
Ladder.column("Name", width="120", anchor=CENTER)

for rank,player in enumerate(total_players_list):
    Ladder.insert(parent='', index='end', text="Parent", values=(rank+1,player))

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

if os.path.getsize("upcoming_match.txt") > 0:
        file = open("upcoming_match.txt", "r")
        contents = file.read()
        upcoming_match = ast.literal_eval(contents)
        file.close()

for id,match in upcoming_match.items():
    upcoming_match_tree.insert(parent='', index='end', text="Parent", values=(id,match['Player1'], match['VS'], match['Player2'], match['Date']))
upcoming_match_tree.grid(column=0, row=2, columnspan=5)

#=======Past Matches=======#
past_match_tree_label = tk.Label(text="Past Matches", font=("Times New Roman", 20))
past_match_tree_label.grid(column=0, row=5, pady=5)
past_match_tree = ttk.Treeview(window)
past_match_tree.grid(column=0, row=6, columnspan=5)

past_match_tree['columns'] = ("ID", "Player1", "VS", "Player2", "Date")

past_match_tree.heading('#0', text='', anchor=CENTER)
past_match_tree.heading("ID", text="ID", anchor=CENTER)
past_match_tree.heading("Player1", text="Player1", anchor=CENTER)
past_match_tree.heading("VS", text="VS", anchor=CENTER)
past_match_tree.heading("Player2", text="Player2", anchor=CENTER)
past_match_tree.heading("Date", text="Date", anchor=CENTER)

past_match_tree.column('#0', width=0, stretch=NO)
past_match_tree.column("ID", width="60", anchor=CENTER)
past_match_tree.column("Player1", width="120", anchor=CENTER)
past_match_tree.column("VS", width="120", anchor=CENTER)
past_match_tree.column("Player2", width="120", anchor=CENTER)
past_match_tree.column("Date", width="80", anchor=CENTER)

past_match_scroll = Scrollbar(window)
past_match_scroll.grid(column=5, row=6)
past_match_tree.configure(yscrollcommand=past_match_scroll.set)
past_match_scroll.configure(command=past_match_tree.yview)

#=======Buttons=======#
btn_refresh_upcoming_match = tk.Button(window,text="Refresh Match", bg="white", command=refreshUpcomingMatch)
btn_refresh_upcoming_match.grid(row=3, column=0, pady=5) 

btn_refresh_ladder = tk.Button(window,text="Refresh Ladder", bg="white", command=refreshLadder)
btn_refresh_ladder.grid(row=3, column=6, pady=5) 

btn_frame = Frame(window, width=1000, height=60, bg="grey")
btn_frame.grid(row=4, column=0,sticky=NSEW)

btn_register = tk.Button(btn_frame,text="Register", bg="green", command=registerPlayerList)
btn_register.grid(row=4, column=1, padx=5) 

btn_withdraw = tk.Button(btn_frame,text="Withdraw", bg="red", command=withdrawPlayerList)
btn_withdraw.grid(row=4, column=2, padx=5)

btn_challenge = tk.Button(btn_frame,text="Issue Challenge", bg="yellow", command=issueChallenge)
btn_challenge.grid(row=4, column=3, padx=5)

btn_view = tk.Button(btn_frame,text="View Players", bg="light blue", command=viewPlayerStats)
btn_view.grid(row=4, column=4, padx=5)

window.mainloop()
