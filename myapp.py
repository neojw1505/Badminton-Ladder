from functions import *

#====Initialize====#
window = tk.Tk()
window.geometry("1000x800")
# window.config(bg="cyan")
window.title("Mini Project: A Badminton Ladder")

# print(total_players_list) 
# print(total_players_dict) 
# print(upcoming_match) 
# print(past_match) 

#=======Refresh Functions=======#
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

# ======= Title ======= #
title = tk.Label(text="A Badminton Ladder",  font=("Times New Roman", 30))
title.grid(pady=5)

# ================================= Ladder Ranking =========================================== #
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

# =================================== Upcoming Matches ======================================== #
upcoming_match_tree_label = tk.Label(text="Upcoming Matches", font=("Times New Roman", 20))
upcoming_match_tree_label.grid(column=0, row=1, pady=5)
upcoming_match_tree = ttk.Treeview(window)
upcoming_match_tree.grid(column=0, row=2,columnspan=4)

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
upcoming_match_scroll.grid(column=4, row=2)
upcoming_match_tree.configure(yscrollcommand=upcoming_match_scroll.set)
upcoming_match_scroll.configure(command=upcoming_match_tree.yview)

if os.path.getsize("upcoming_match.txt") > 0:
        file = open("upcoming_match.txt", "r")
        contents = file.read()
        upcoming_match = ast.literal_eval(contents)
        file.close()

for id,match in upcoming_match.items():
    upcoming_match_tree.insert(parent='', index='end', text="Parent", values=(id,match['Player1'], match['VS'], match['Player2'], match['Date']))

def selectMatchInUpcomingMatch(event):
    global match
    match = upcoming_match_tree.focus()
    match = upcoming_match_tree.item(match)['values']
    
    global match_id
    match_id = match[0]

    global Player_1
    Player_1 = match[1]

    global Player_2
    Player_2 = match[3]

    global match_date
    match_date = match[4]

upcoming_match_tree.bind("<<TreeviewSelect>>",selectMatchInUpcomingMatch)

def addScore():
    try:
        root = Tk()  
        root.title("Save Match Result")
        root.geometry("600x600")
        # Header
        header_label = tk.Label(root,text="MATCH RESULTS", font=("Times New Roman", 30))
        header_label.grid(column=1, row=0, pady=5)

        # Date Label
        frame = Frame(root, bg="grey")
        frame.grid(column=1, row=1, pady=5)
        date = datetime.datetime.strptime(match_date, '%j/%d/%y')
        date = date.strftime('%b %d, %Y')
        date_label = tk.Label(frame,text=date, font=("Times New Roman", 30))
        date_label.grid(column=1, row=1, pady=5)

        # Players Label
        player_1_label = tk.Label(root,text=Player_1, font=("Times New Roman", 15))
        player_1_label.grid(column=0, row=3, pady=5)

        player_2_label = tk.Label(root,text=Player_2, font=("Times New Roman", 15))
        player_2_label.grid(column=2, row=3, pady=5)

        player_1_label = tk.Label(root,text=Player_1, font=("Times New Roman", 15))
        player_1_label.grid(column=0, row=5, pady=5)

        player_2_label = tk.Label(root,text=Player_2, font=("Times New Roman", 15))
        player_2_label.grid(column=2, row=5, pady=5)

        player_1_label = tk.Label(root,text=Player_1, font=("Times New Roman", 15))
        player_1_label.grid(column=0, row=7, pady=5)

        player_2_label = tk.Label(root,text=Player_2, font=("Times New Roman", 15))
        player_2_label.grid(column=2, row=7, pady=5)

        # Match Labels
        match1_label = tk.Label(root,text="Match 1", font=("Times New Roman", 20))
        match1_label.grid(column=1, row=2, pady=5)
        
        match2_label = tk.Label(root,text="Match 2", font=("Times New Roman", 20))
        match2_label.grid(column=1, row=4, pady=5)

        match3_label = tk.Label(root,text="Match 3", font=("Times New Roman", 20))
        match3_label.grid(column=1, row=6, pady=5)

        # Match Entry
        global match1_Entry
        match1_Entry = Entry(root, text="")
        match1_Entry.grid(row=3,column=1, pady=10, padx=10)

        global match2_Entry
        match2_Entry = Entry(root, text="")
        match2_Entry.grid(row=5,column=1, pady=10, padx=10)
        
        global match3_Entry
        match3_Entry = Entry(root, text="")
        match3_Entry.grid(row=7,column=1, pady=10, padx=10)
    except NameError:
        root.withdraw()
        messagebox.showwarning("Select Upcoming Match","No Upcoming Match Selected")

    # Save Result Button
    global save_result_label
    btn_save_result = tk.Button(root,text="Save Results", pady=10, padx=20, command=saveMatchResults)
    btn_save_result.grid(row=8, column=1, pady=10) 
    save_result_label = tk.Label(root,font=("Times New Roman", 20))
    save_result_label.grid(column=1, row=9, pady=10)

def saveMatchResults():
    save_result_label.config(text="Results Saved!", font =("Times New Roman bold", 13))
    global match_date
    date = datetime.datetime.strptime(match_date, '%j/%d/%y')
    date = date.strftime('%d-%m-%Y')

    # Add to data.txt Match Record
    scores = str(match1_Entry.get()) + " " + str(match2_Entry.get()) + " " + str(match3_Entry.get())
    scores = scores.rstrip()

    # ==== Check Which Player Won ==== #
    player1_match_won = 0
    player2_match_won = 0
    player1_won = False
    player2_won = False

    # Match 1 Results 
    if len(match1_Entry.get()) != 0:
        match_1_result = match1_Entry.get().split('-')
        player1_m1_result = match_1_result[0]
        player2_m1_result = match_1_result[1]

    # Match 2 Results 
    if len(match2_Entry.get()) != 0:
        match_2_result = match2_Entry.get().split('-')
        player1_m2_result = match_2_result[0]
        player2_m2_result = match_2_result[1]

    # Match 3 Results 
    # if match3_entry is not empty, then assign player results
    if len(match3_Entry.get()) != 0:
        match_3_result = match3_Entry.get().split('-')
        player1_m3_result = match_3_result[0]
        player2_m3_result = match_3_result[1]

    if len(match1_Entry.get()) != 0:
        if player1_m1_result > player2_m1_result:
            player1_match_won += 1
        else:
            player2_match_won += 1

    if len(match2_Entry.get()) != 0:
        if player1_m2_result > player2_m2_result:
            player1_match_won += 1
        else:
            player2_match_won += 1   

    if len(match3_Entry.get()) != 0:
        if player1_m3_result > player2_m3_result:
            player1_match_won += 1
        else:
            player2_match_won += 1     

    if player1_match_won >= 2:
        player1_won = True
    if player2_match_won >= 2:
        player2_won = True

    f = open("data.txt", 'a')
    f.write(str(Player_1 + "/" + str(Player_2) + "/" + str(date) + "/" + scores))
    f.write("\n")
    f.close()

    # Add to Past Matches{}
    past_match_tree.insert(parent='', index='end', text="Parent", values=(match_id, Player_1, Player_2, date, scores))

    # Add to past_match.txt 
    past_match[len(past_match) + 1] = {'ID': match_id, "Player1": Player_1, 'Player2': Player_2, "Date": date, "Score": scores}
            
    f = open("past_match.txt", 'a')
    f.write(str(past_match))
    f.write("\n")
    f.close()

    # Delete first line if there is more than 1 line
    with open('past_match.txt', 'r') as fin:
        lines = fin.read().splitlines(True)
    if len(lines) > 1 and len(lines) != 1:
        with open('past_match.txt', 'w') as fout:
            fout.writelines(lines[1:])
    
    # Remove from Upcoming Matches View
    for record in upcoming_match_tree.get_children():
        if upcoming_match_tree.item(record)['values'][0] == match[0]:
            upcoming_match_tree.delete(record)
            break

    # Remove from upcoming_match.txt
    for k,v in upcoming_match.copy().items():
        if k == match[0]:
            del upcoming_match[k]

    f = open("upcoming_match.txt", 'w')
    f.write(str(upcoming_match))
    f.write("\n")
    f.close()

    # Update Ladder Ranking 
    def ranking(arr, sourceRank, targetRank):
        for v in arr:
            if sourceRank == arr[v]['position']:
                arr[v]['position'] = targetRank
            elif int(targetRank) <= int(arr[v]['position']) < int(sourceRank):
                arr[v]['position'] = int(arr[v]['position']) + int(1)

    # Update Player Information in total_players_dict and player_dict.txt
    for rank, info in total_players_dict.items():
        if info['name'] == Player_1[:-2] or info['name'] == Player_2[:-2]:
            info['match_played'] += 1
            if player1_won == True and player2_won == False:
                if info['name'] == Player_1[:-2]:
                    info['match_won'] += 1
                    global Player_1_pos
                    Player_1_pos = info['position']
                if info['name'] == Player_2[:-2]:
                    info['match_loss'] += 1 
                    global Player_2_pos
                    Player_2_pos = info['position']
            if player1_won == False and player2_won == True:
                if info['name'] == Player_1[:-2]:
                    info['match_loss'] += 1 
                    # Player 1 position 
                if info['name'] == Player_2[:-2]:
                    info['match_won'] += 1 
                    # Player 2 position 

    ranking(total_players_dict, Player_1_pos, Player_2_pos)  

    f = open("player_dict.txt", 'a')
    f.write(str(total_players_dict))
    f.write("\n")
    f.close()
    
    # Delete first line if there is more than 1 line
    with open('player_dict.txt', 'r') as fin:
        lines = fin.read().splitlines(True)
        if len(lines) > 1 and len(lines) != 1:
            with open('player_dict.txt', 'w') as fout:
                fout.writelines(lines[1:])

    # Update ladder.txt
    tuple_name_rank = [( v['name'], v['position']) for k, v in total_players_dict.items()]
    print(tuple_name_rank)
    sorted_by_rank = sorted(tuple_name_rank, key=lambda tup: tup[1])
    print(sorted_by_rank)
    ladder_ranking = [player[0] for player in sorted_by_rank]
    print(ladder_ranking)

    file = open("ladder.txt","r+")
    file.truncate(0)
    file.close()

    file = open("ladder.txt","a")
    file.writelines(["%s\n" % item  for item in ladder_ranking])
    file.close()

    refreshLadder()
    

# ==================================== Past Matches ====================================== #

# initialize Treeview
past_match_tree_label = tk.Label(text="Past Matches", font=("Times New Roman", 20))
past_match_tree_label.grid(column=0, row=5, pady=5)
past_match_tree = ttk.Treeview(window)
past_match_tree.grid(column=0, row=6, columnspan=4)

# Define Columns
past_match_tree['columns'] = ("ID", "Player1", "Player2", "Date", "Score")

# Column headings
past_match_tree.heading('#0', text='', anchor=CENTER)
past_match_tree.heading("ID", text="ID", anchor=CENTER)
past_match_tree.heading("Player1", text="Player1", anchor=CENTER)
past_match_tree.heading("Player2", text="Player2", anchor=CENTER)
past_match_tree.heading("Date", text="Date", anchor=CENTER)
past_match_tree.heading("Score", text="Score", anchor=CENTER)

# Format columns
past_match_tree.column('#0', width=0, stretch=NO)
past_match_tree.column("ID", width="60", anchor=CENTER)
past_match_tree.column("Player1", width="120", anchor=CENTER)
past_match_tree.column("Player2", width="120", anchor=CENTER)
past_match_tree.column("Date", width="80", anchor=CENTER)
past_match_tree.column("Score", width="120", anchor=CENTER)

# Scrollbar
past_match_scroll = Scrollbar(window)
past_match_scroll.grid(column=4, row=6)
past_match_tree.configure(yscrollcommand=past_match_scroll.set)
past_match_scroll.configure(command=past_match_tree.yview)

if os.path.getsize("past_match.txt") > 0:
    file = open("past_match.txt", "r")
    contents = file.read()
    past_match = ast.literal_eval(contents)
    file.close()

for id,match in past_match.items():
    past_match_tree.insert(parent='', index='end', text="Parent", values=(id,match['Player1'], match['Player2'], match['Date'], match['Score']))

# Refresh Button
btn_refresh_upcoming_match = tk.Button(window,text="Refresh Match", command=refreshUpcomingMatch)
btn_refresh_upcoming_match.grid(row=3, column=0) 

btn_refresh_ladder = tk.Button(window,text="Refresh Ladder", command=refreshLadder)
btn_refresh_ladder.grid(row=3, column=6, pady=5) 

# Add Score Button
btn_add_score_upcoming_match = tk.Button(window, text="Add Score", command=addScore)
btn_add_score_upcoming_match.grid(row=3, column=1) 

btn_frame = Frame(window)
btn_frame.grid(row=4, column=0, sticky=NSEW)

# Register Button
btn_register = tk.Button(btn_frame,text="Register", bg="green", command=registerPlayerList)
btn_register.grid(row=4, column=1, padx=5) 

# Withdraw Button
btn_withdraw = tk.Button(btn_frame,text="Withdraw", bg="red", command=withdrawPlayerList)
btn_withdraw.grid(row=4, column=2, padx=5)

# Issue Challenge Button
btn_challenge = tk.Button(btn_frame,text="Issue Challenge", bg="yellow", command=issueChallenge)
btn_challenge.grid(row=4, column=3, padx=5)

# View Players Button
btn_view = tk.Button(btn_frame,text="View Players", bg="light blue", command=viewPlayerMatchInfo)
btn_view.grid(row=4, column=4, padx=5)


window.mainloop()
