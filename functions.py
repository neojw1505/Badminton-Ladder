import os
import ast
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *
import datetime
from datetime import date
from collections import OrderedDict

#========================================= Load All Required Data ====================================#
# Total Players Data Structures
total_players_list = []
total_players_dict = {}
upcoming_match = {}
past_match = {}

def loadPlayers():
    # Load ladder.txt
    f = open("ladder.txt", "r")
    for line in f:
        total_players_list.append(line.strip())

    # Load upcoming_match.txt
    if os.path.getsize("upcoming_match.txt") > 0:
        um = open("upcoming_match.txt", "r")
        umcontents = um.read()
        global upcoming_match
        upcoming_match = ast.literal_eval(umcontents)
        um.close()

    # Load player_dict.txt
    if os.path.getsize("player_dict.txt") > 0:
        pd = open("player_dict.txt", "r")
        pdcontents = pd.read()
        global total_players_dict
        total_players_dict = ast.literal_eval(pdcontents)
        pd.close()

    # Load past_match.txt
    if os.path.getsize("past_match.txt") > 0:
        pm = open("past_match.txt", "r")
        pmcontents = pm.read()
        global past_match
        past_match = ast.literal_eval(pmcontents)
        pm.close()

    return total_players_list, total_players_dict, upcoming_match, past_match
loadPlayers()


#================================= Register A Player to Ladder ===============================#
def registerPlayerList():
    root = Tk()
    root.title("Register a player")
    root.geometry("300x400")
    label = Label(
        root, text="Current Players in Ladder", font=("Times New Roman bold", 10)
    )
    label.pack(pady=5)
    players_listbox = Listbox(root, width=40)
    players_listbox.pack(pady=5)
    for players in total_players_list:
        players_listbox.insert("end", players)

    # add to total_players_list
    def registerPlayer():
        root1 = Tk()
        root1.title("Register a player")
        e = Entry(root1, width="80")
        e.pack()

        def registerPlayerName():
            # Labels
            eLabel = Label(root1, text="Player: " + e.get() + " is registered!")
            eLabel.pack()
            player_to_register = e.get()

            # append new player to ladder.txt (list)
            f = open("ladder.txt", "a")
            f.write(str(player_to_register))
            f.write("\n")
            f.close()

            # Add to ladder.txt
            total_players_list.append(player_to_register)

            # Add to player_dict.txt
            total_players_dict[len(total_players_dict) + 1] = {
                "name": e.get(),
                "position": len(total_players_dict) + 1,
                "match_played": 0,
                "match_won": 0,
                "match_loss": 0,
            }

            f = open("player_dict.txt", "a")
            f.write(str(total_players_dict))
            f.write("\n")
            f.close()

            with open("player_dict.txt", "r") as fin:
                lines = fin.read().splitlines(True)
            if len(lines) > 1 and len(lines) != 1:
                with open("player_dict.txt", "w") as fout:
                    fout.writelines(lines[1:])

            # Add to data.txt
            f = open("data.txt", "a")
            f.write("+" + player_to_register + "/" + date.today().strftime("%d-%m-%Y"))
            f.write("\n")
            f.close()

            # Refresh Player ListBox
            players_listbox.delete(0, END)
            for players in total_players_list:
                players_listbox.insert("end", players)

        # Entry Buttons
        Register_plyr_name_btn = Button(
            root1, text="Enter Player to Register", command=registerPlayerName
        )
        Register_plyr_name_btn.pack(pady=10)

    # Button to direct to Entry
    Register_plyr_btn = Button(root, text="Click to Register", command=registerPlayer)
    Register_plyr_btn.pack(pady=10)

#================================= View All/Selected Players Match Information ============================#
def viewPlayerMatchInfo():

    #=========== Display Treeview ============#
    # Initialize Treeview
    ws = Tk()
    ws.title("All Player's Information")
    ws.geometry("600x350")
    global players_match_info_tree
    players_match_info_tree = ttk.Treeview(ws)
    players_match_info_tree.grid(row=1, column=0, padx=10, pady=10)

    # Define columns
    players_match_info_tree["columns"] = (
        "Name",
        "Position",
        "Match Played",
        "Won",
        "Loss",
        "WinRate(%)",
    )
    # Column Headings
    players_match_info_tree.heading("#0", text="", anchor=CENTER)
    players_match_info_tree.heading("Name", text="Name", anchor=W)
    players_match_info_tree.heading("Position", text="Position", anchor=W)
    players_match_info_tree.heading("Match Played", text="Match Played", anchor=W)
    players_match_info_tree.heading("Won", text="Won", anchor=CENTER)
    players_match_info_tree.heading("Loss", text="Loss", anchor=CENTER)
    players_match_info_tree.heading("WinRate(%)", text="WinRate(%)", anchor=CENTER)

    # Format columns
    players_match_info_tree.column("#0", width=0, stretch=NO)
    players_match_info_tree.column("Name", anchor=W, width=120)
    players_match_info_tree.column("Position", anchor=CENTER, width=80)
    players_match_info_tree.column("Match Played", anchor=CENTER, width=80)
    players_match_info_tree.column("Won", anchor=CENTER, width=40)
    players_match_info_tree.column("Loss", anchor=CENTER, width=40)
    players_match_info_tree.column("WinRate(%)", anchor=CENTER, width=80)
    
    # Selected Player
    def selectPlayer(event):
        curPlayer = players_match_info_tree.focus()
        global selected_player_name
        selected_player_name = players_match_info_tree.item(curPlayer)["values"][0]

    players_match_info_tree.bind("<<TreeviewSelect>>", selectPlayer)

    # Add Data
    if os.path.getsize("player_dict.txt") > 0:
        file = open("player_dict.txt", "r")
        contents = file.read()
        global total_players_dict
        total_players_dict = ast.literal_eval(contents)
        file.close()
    for p_info in total_players_dict.values():
        if p_info["match_played"] == 0:
            winRate = 0
        else:
            winRate = p_info["match_won"] / p_info["match_played"] * 100
        players_match_info_tree.insert(parent="",index="end",text="Parent",values=(p_info["name"],p_info["position"],p_info["match_played"],p_info["match_won"],p_info["match_loss"],"{:.2f}".format(winRate)))

    #========= Search Player By Name ========#
    def search():
        players_match_info_tree.focus_set()
        children = players_match_info_tree.get_children()
        if children:
            players_match_info_tree.focus(children[0])
            players_match_info_tree.selection_set(children[0])
            players_match_info_tree.focus()

        query = search_entry.get()
        selections = []
        if query == "":
            ws.lower()
            messagebox.showwarning("Input a Player Name","Search Entry Cannot Be Empty!")
            ws.focus_set()
            ws.tkraise()
        for child in children:
            if query in players_match_info_tree.item(child)['values']:
                selections.append(child)

        print('Search Completed')
        players_match_info_tree.selection_set(selections)

    search_Frame = Frame(ws)
    search_Frame.grid(row=0, column=0, columnspan=5)
    search_label = tk.Label(search_Frame, text="Search Player:")
    search_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    search_entry = tk.Entry(search_Frame, width=15)
    search_entry.grid(row=0, column=1, pady=10, sticky=tk.E, rowspan=1)
    search_btn = tk.Button(search_Frame, text="Search", width=10, command=search)
    search_btn.grid(row=0, column=2, padx=10, pady=10)

    #======== Filter Player Info ==========#
    # Drop-down Menu showing filter options
    filter_options = ["Highest Position","Lowest Position","Most Active","Least Active","Most Wins","Most Loss"]

    # Get the Selected Filter Option
    def getFilterOption(*args):
        global selected_option
        selected_option = filter_player_menu.get()
        
    filter_menu_label = Label(search_Frame, text="Filter By:")    
    filter_menu_label.grid(row=0, column=3, padx=10, pady=10, sticky=tk.W)   
    filter_player_menu = ttk.Combobox(search_Frame,values=filter_options)
    filter_player_menu.set("Select an option")
    filter_player_menu.grid(row=0, column=4, pady=10, sticky=tk.E, rowspan=1)
    filter_player_menu.bind("<<ComboboxSelected>>", getFilterOption)

    # Clear Treeview
    def clearPlayerinformation():
        players_match_info_tree.delete(*players_match_info_tree.get_children())

    # Populate Treeview
    def loadFilteredData():

        #======= Highest Position ======#
        try:
            if selected_option == "Highest Position":
                # clear the view
                clearPlayerinformation()
                highest_position_data = OrderedDict(sorted(total_players_dict.items(), key=lambda i: i[1]['position']))    
                # insert filtered data
                for p_info in highest_position_data.values():
                    players_match_info_tree.insert(parent='', index='end', values=(p_info["name"],p_info["position"],p_info["match_played"],p_info["match_won"],p_info["match_loss"],"{:.2f}".format(winRate)))

        #======= Lowest Position ======#
            if selected_option == "Lowest Position":
                # clear the view
                clearPlayerinformation()
                highest_position_data = OrderedDict(sorted(total_players_dict.items(), key=lambda i: i[1]['position']))    
                # insert filtered data
                for p_info in highest_position_data.values():
                    players_match_info_tree.insert(parent='', index='0', values=(p_info["name"],p_info["position"],p_info["match_played"],p_info["match_won"],p_info["match_loss"],"{:.2f}".format(winRate)))

        #======= Most Active ======#
            if selected_option == "Most Active":
                # clear the view
                clearPlayerinformation()
                most_active_data = OrderedDict(sorted(total_players_dict.items(), key=lambda i: i[1]['match_played']))    
                # insert filtered data
                for p_info in most_active_data.values():
                    players_match_info_tree.insert(parent='', index='0', values=(p_info["name"],p_info["position"],p_info["match_played"],p_info["match_won"],p_info["match_loss"],"{:.2f}".format(winRate)))

        #======= Least Active ======#
            if selected_option == "Least Active":
                # clear the view
                clearPlayerinformation()
                least_active_data = OrderedDict(sorted(total_players_dict.items(), key=lambda i: i[1]['match_played']))    
                # insert filtered data
                for p_info in least_active_data.values():
                    players_match_info_tree.insert(parent='', index='end', values=(p_info["name"],p_info["position"],p_info["match_played"],p_info["match_won"],p_info["match_loss"],"{:.2f}".format(winRate)))

        #======= Most Wins ======#
            if selected_option == "Most Wins":
                # clear the view
                clearPlayerinformation()
                most_wins_data = OrderedDict(sorted(total_players_dict.items(), key=lambda i: i[1]['match_won']))   
                # insert filtered data
                for p_info in most_wins_data.values():
                    players_match_info_tree.insert(parent='', index='0', values=(p_info["name"],p_info["position"],p_info["match_played"],p_info["match_won"],p_info["match_loss"],"{:.2f}".format(winRate)))

        #======= Least Wins ======#
            if selected_option == "Most Loss":
                # clear the view
                clearPlayerinformation()
                most_wins_data = OrderedDict(sorted(total_players_dict.items(), key=lambda i: i[1]['match_loss']))   
                # insert filtered data
                for p_info in most_wins_data.values():
                    players_match_info_tree.insert(parent='', index='0', values=(p_info["name"],p_info["position"],p_info["match_played"],p_info["match_won"],p_info["match_loss"],"{:.2f}".format(winRate)))
        except NameError:
            ws.lower()
            messagebox.showwarning("Select an Option","No Option Selected")
            ws.focus_set()
            ws.tkraise()
    # Filter Button
    btn_filter_players = Button(search_Frame, text="Filter", command=loadFilteredData)
    btn_filter_players.grid(row=0, column=5, padx=10)

    #========== View Selected Player Match History ==========#
    def viewSelectedPlayerMatches():

        # initialize Treeview
        try:
            root= Tk()
            root.title(selected_player_name + "'s Past Matches")

            root.geometry("600x300")
            selected_player_matches_tree = ttk.Treeview(root)
            selected_player_matches_tree.grid(row=1, column=0, pady=10)

            # Define columns
            selected_player_matches_tree['columns'] = ("MatchID", "Player1", "Player2", "Date", "Score")
            
            # Column headings
            selected_player_matches_tree.heading('#0', text='', anchor=CENTER)
            selected_player_matches_tree.heading("MatchID", text="MatchID", anchor=CENTER)
            selected_player_matches_tree.heading("Player1", text="Player1", anchor=CENTER)
            selected_player_matches_tree.heading("Player2", text="Player2", anchor=CENTER)
            selected_player_matches_tree.heading("Date", text="Date", anchor=CENTER)
            selected_player_matches_tree.heading("Score", text="Score", anchor=CENTER)
            
            # Format columns
            selected_player_matches_tree.column('#0', width=0, stretch=NO)
            selected_player_matches_tree.column("MatchID", width="60", anchor=CENTER)
            selected_player_matches_tree.column("Player1", width="120", anchor=CENTER)
            selected_player_matches_tree.column("Player2", width="120", anchor=CENTER)
            selected_player_matches_tree.column("Date", width="80", anchor=CENTER)
            selected_player_matches_tree.column("Score", width="120", anchor=CENTER)

            # Scrollbar
            selected_player_matches_scroll = Scrollbar(root)
            selected_player_matches_scroll.grid(column=2, row=1)
            selected_player_matches_tree.configure(yscrollcommand=selected_player_matches_scroll.set)
            selected_player_matches_scroll.configure(command=selected_player_matches_tree.yview)

            # Getting Selected Player Matches
            selected_player_matches = {}
            for past_matches in past_match.values():
                if past_matches['Player1'][:-2] == selected_player_name or past_matches['Player2'][:-2] == selected_player_name:
                    selected_player_matches[len(selected_player_matches)+1] = past_matches
            for k,v in selected_player_matches.items():
                selected_player_matches_tree.insert(parent='', index='end', text="Parent", values=(k,v['Player1'], v['Player2'], v['Date'], v['Score']))           
            
        except NameError:
            root.withdraw()
            ws.lower()
            messagebox.showwarning("No Player Selected", "No Player Selected!")
            ws.focus_set()
            ws.tkraise()
        
        # def filterFirstName(*args):
        #     print("Hello")
        #     ItemsOnTreeView = selected_player_matches_tree.get_children()
        #     search = root.search_ent_var.get().capitalize()
        #     print("Hello")
        #     for eachItem in ItemsOnTreeView:
        #         print(eachItem)
        #         if search in selected_player_matches_tree.item(eachItem)['values'][2]:
        #             search_var = selected_player_matches_tree.item(eachItem)['values']
        #             selected_player_matches_tree.delete(eachItem)
        #             selected_player_matches_tree.insert("",0,values=search_var)  

        #     for k,v in selected_player_matches.items():
        #         Wselected_player_matches_tree.insert(parent='', index='end', text="Parent", values=(k,v['Player1'], v['Player2'], v['Date'], v['Score']))

        # search_ent_var = root.search_ent_var= tk.StringVar(value='asdf')

        # search_by = ttk.Combobox(root, values = selected_player_matches_tree['columns'])
        # search_by.current(2)
        # search_by.grid(row =0, column=0)

        # search_ent = Entry(root, textvariable = search_ent_var)
        # search_ent.grid(row=0, column=1,padx=10)

        # search_ent_var.trace("w", filterFirstName)   
           
    # View Selected Player Matches Button
    btn_selected_player_matches = Button(ws, text="View Selected Player Matches", command=viewSelectedPlayerMatches)
    btn_selected_player_matches.grid(row=2, column=0, pady=10)    

#============================= Withdraw A Player From Ladder ==============================#
def withdrawPlayerList():
    
    # Initialize Listbox
    root = Tk()
    root.title("Remove a player")
    root.geometry("400x400")
    players_listbox = Listbox(root)
    players_listbox.pack(pady=5)
    for players in total_players_list:
        players_listbox.insert("end", players)

    # remove from total_players_list 
    def withdrawPlayer():
        player_to_remove = players_listbox.get(players_listbox.curselection())

        # Remove from ladder.txt
        with open("ladder.txt", "r") as f:
            lines = f.readlines()
        with open("ladder.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != player_to_remove:
                    f.write(line)
            f.close()

        # Remove from total_players_list[]
        total_players_list.remove(player_to_remove)

        # Remove from player_dict.txt{}
        for id, p_info in total_players_dict.copy().items():
            for key in p_info:
                if p_info[key] == player_to_remove:
                    idx = id
                    del total_players_dict[idx]
                    player_dict = open("player_dict.txt", "a")
                    player_dict.write(str(total_players_dict))
                    player_dict.write("\n")
                    player_dict.close()
                    break

        with open("player_dict.txt", "r") as fin:
            lines = fin.read().splitlines(True)
        if len(lines) > 1 and len(lines) != 1:
            with open("player_dict.txt", "w") as fout:
                fout.writelines(lines[1:])

        # Remove from Data.txt
        f = open("data.txt", "a")
        f.write("-" + player_to_remove + "/" + date.today().strftime("%d-%m-%Y"))
        f.write("\n")
        f.close()

        # Clear List Box
        players_listbox.delete(0, END)

        # Recreate List Box without removed player
        for players in total_players_list:
            players_listbox.insert("end", players)

    # Withdraw Button
    withdraw_plyr_btn = Button(root, text="Click to Withdraw", command=withdrawPlayer)
    withdraw_plyr_btn.pack(pady=10)


#============================= Issue Challenge to Another Player (Create Match) ==========================#
def issueChallenge():
    
    # Callbacks
    def selectPlayerOne(event):
        global selected_item_p1
        selected_item_p1 = playerOne_Tree.focus()
        selected_item_p1 = playerOne_Tree.item(selected_item_p1)["values"]

    def selectPlayerTwo(event):
        global selected_item_p2
        selected_item_p2 = playerTwo_Tree.focus()
        selected_item_p2 = playerTwo_Tree.item(selected_item_p2)["values"]

    # Initialize
    root = Tk()
    root.title("Create a Match")
    root.geometry("800x650")

    # Initialize Player One Tree
    player1_label = Label(root, text="PLAYER 1", font=("Times New Roman bold", 15))
    player1_label.grid(row=0, column=0)
    playerOne_Tree = ttk.Treeview(root)
    playerOne_Tree.grid(row=1, column=0, padx=15)

    playerOne_Tree["columns"] = ("Rank", "Player")

    playerOne_Tree.heading("#0", text="", anchor=CENTER)
    playerOne_Tree.heading("Rank", text="Rank", anchor=CENTER)
    playerOne_Tree.heading("Player", text="Player", anchor=CENTER)

    playerOne_Tree.column("#0", width=0, stretch=NO)
    playerOne_Tree.column("Rank", width="60", anchor=CENTER)
    playerOne_Tree.column("Player", width="120", anchor=CENTER)

    for rank, player in enumerate(total_players_list):
        playerOne_Tree.insert(parent="", index="end", values=(rank + 1, player))

    vslabel = Label(root, text="VS", font=("Times New Roman bold", 20))
    vslabel.grid(row=1, column=1)

    # Initalize Player Two tree
    player2_label = Label(root, text="PLAYER 2", font=("Times New Roman bold", 15))
    player2_label.grid(row=0, column=2)
    playerTwo_Tree = ttk.Treeview(root)
    playerTwo_Tree.grid(row=1, column=2, padx=15)

    playerTwo_Tree["columns"] = ("Rank", "Player")

    playerTwo_Tree.heading("#0", text="", anchor=CENTER)
    playerTwo_Tree.heading("Rank", text="Rank", anchor=CENTER)
    playerTwo_Tree.heading("Player", text="Player", anchor=CENTER)

    playerTwo_Tree.column("#0", width=0, stretch=NO)
    playerTwo_Tree.column("Rank", width="60", anchor=CENTER)
    playerTwo_Tree.column("Player", width="120", anchor=CENTER)

    for rank, player in enumerate(total_players_list):
        playerTwo_Tree.insert(
            parent="", index="end", text="Parent", values=(rank + 1, player)
        )

    # Detached Players goes here
    playerOne_Tree_detached_items = []
    playerTwo_Tree_detached_items = []

    #========== Player 1 Selection =========#
    def selectPlayer1():
        playerTwo_Tree_detached_items.sort(reverse=True)
        # Reattach players
        for i in playerTwo_Tree_detached_items:
            playerTwo_Tree.reattach(i, "", 0)
        playerTwo_Tree_detached_items.clear()

        # Detach Players more than 3 position higher
        for id, i in enumerate(playerTwo_Tree.get_children(), 1):
            if id <= selected_item_p1[0] - 4:
                plyr2 = "I00" + str(id)
                playerTwo_Tree.detach(plyr2)
                playerTwo_Tree_detached_items.append(plyr2)

        # Insert into Player1 textbox
        player1_Entry.configure(state="normal")
        player1_Entry.delete(0,END)
        player1_Entry.insert(0, selected_item_p1[1])
        player1_Entry.configure(state="disabled")

        return str(selected_item_p1[1]) + " " + str(selected_item_p1[0])

    playerOne_Tree.bind("<<TreeviewSelect>>", selectPlayerOne)

    #========== Player 2 Selection =========#
    def selectPlayer2():
        playerOne_Tree_detached_items.sort(reverse=True)

        # Reattach players
        for i in playerOne_Tree_detached_items:
            playerOne_Tree.reattach(i, "", 0)
        playerOne_Tree_detached_items.clear()

        # Detach Players more than 3 position higher
        for id, i in enumerate(playerOne_Tree.get_children(), 1):
            if id <= selected_item_p2[0] - 4:
                plyr1 = "I00" + str(id)
                playerOne_Tree.detach("I00" + str(id))
                playerOne_Tree_detached_items.append(plyr1)

        # Insert into Player2 textbox
        player2_Entry.configure(state="normal")
        player2_Entry.delete(0, END)
        player2_Entry.insert(0, selected_item_p2[1])
        player2_Entry.configure(state="disabled")

        return str(selected_item_p2[1]) + " " + str(selected_item_p2[0])
    playerTwo_Tree.bind("<<TreeviewSelect>>", selectPlayerTwo)

    #=============== DatePicker ===================#
    Date_frame = Frame(root, bg="grey")
    Date_frame.grid(row=5, column=2, sticky=NSEW)
    Date_label = Label(root, text="DATE OF MATCH", font=("Times New Roman bold", 15))
    Date_label.grid(row=4, column=2)
    cal = Calendar(Date_frame, selectmode="day", year=2021, month=5, day=22)
    cal.grid(row=6, column=2, columnspan=2, sticky=W)

    def grab_date():
        # Insert into Date textbox
        match_date_Entry.configure(state="normal")
        match_date_Entry.delete(0, END)
        match_date_Entry.insert(0, cal.get_date())
        match_date_Entry.configure(state="disabled")
        return cal.get_date()

    #============================ Create the Match ===============================#
    def createMatch():
        upcoming_match[len(upcoming_match) + 1] = {
            "Player1": selected_item_p1[1] + " " + str(selected_item_p1[0]),
            "VS": "VS",
            "Player2": selected_item_p2[1] + " " + str(selected_item_p2[0]),
            "Date": cal.get_date(),
        }

        f = open("upcoming_match.txt", "a")
        f.write(str(upcoming_match))
        f.write("\n")
        f.close()

        # Delete first line if there is more than 1 line
        with open("upcoming_match.txt", "r") as fin:
            lines = fin.read().splitlines(True)
        if len(lines) > 1 and len(lines) != 1:
            with open("upcoming_match.txt", "w") as fout:
                fout.writelines(lines[1:])

        cfm_match_label.config(text="Match Created!")

    # Date Button
    select_date_btn = Button(root, text="Select Date", command=grab_date)
    select_date_btn.grid(row=7, column=2, pady=10)

    # Player1 Button
    select_plyr_btn = Button(root, text="Select Player 1", command=selectPlayer1)
    select_plyr_btn.grid(row=3, column=0, pady=10)

    # Match Details
    player1_frame = Frame(
        root,
        bg="grey",
    )
    player1_frame.grid(row=4, column=0, rowspan=4, padx=20)
    match_detail = Label(
        player1_frame, text="Match Details", font=("Times New Roman bold", 13)
    )
    match_detail.grid(row=4, column=0, pady=10, padx=10)

    # Player1 TextBox
    player1_text_label = Label(
        player1_frame, text="Player 1: ", font=("Times New Roman bold", 10)
    )
    player1_text_label.grid(row=6, column=0)
    player1_Entry = Entry(player1_frame, text="")
    player1_Entry.grid(row=6, column=1, pady=10, padx=10)

    # Player2 Button
    select_plyr_btn = Button(root, text="Select Player 2", command=selectPlayer2)
    select_plyr_btn.grid(row=3, column=2, pady=10)

    # Player2 TextBox
    player2_text_label = Label(
        player1_frame, text="Player 2: ", font=("Times New Roman bold", 10)
    )
    player2_text_label.grid(row=7, column=0)
    player2_Entry = Entry(player1_frame, text="")
    player2_Entry.grid(row=7, column=1)

    # Match Date TextBox
    match_date_text_label = Label(
        player1_frame, text="Date: ", font=("Times New Roman bold", 10)
    )
    match_date_text_label.grid(row=8, column=0)
    match_date_Entry = Entry(player1_frame, text="")
    match_date_Entry.grid(row=8, column=1, pady=10)

    # Confirm Match Button
    cfm_match_btn = Button(
        root, text="Create Match", pady=10, padx=20, command=createMatch
    )
    cfm_match_btn.grid(row=8, column=1, pady=5)

    # Confirm Match Button
    cfm_match_label = Label(root, font=("Times New Roman bold", 13))
    cfm_match_label.grid(row=9, column=1, pady=5)
