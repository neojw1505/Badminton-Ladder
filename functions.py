import os
import ast
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import *

# Total Players Data Structures
total_players_list = []
total_players_dict = {}
upcoming_match = {}

def loadPlayers():
    #  open ladder.txt in read mode
    f = open('ladder.txt', 'r')
    # load list data
    for line in f:
        total_players_list.append(line.strip())
    return total_players_list    

loadPlayers()
    
def registerPlayerList():
    root = Tk()
    root.title("Register a player")
    root.geometry("300x400")
    label = Label(root,text="Current Players in Ladder", font=("Times New Roman bold", 10))
    label.pack(pady=5)
    players_listbox = Listbox(root, width=40)
    players_listbox.pack(pady=5)
    for players in total_players_list:
        players_listbox.insert("end", players)
    # add to total_players_list 
    def registerPlayer():
        root1 = Tk()
        root1.title("Register a player")
        e = Entry(root1, width='80')
        e.pack()

        def registerPlayerName():
            # Labels
            eLabel = Label(root1, text="Player: " + e.get() + " is registered!")
            eLabel.pack()
            player_to_register = e.get()

            # append new player to ladder.txt (list)
            f = open("ladder.txt", 'a')
            f.write(str(player_to_register))
            f.write("\n")
            f.close()

            # Add to ladder.txt
            total_players_list.append(player_to_register)

            # Add to player_dict.txt
            total_players_dict[len(total_players_dict) + 1] = {'name': e.get(), 'position': len(total_players_dict) + 1,"match_played": 0, "match_won": 0, "match_loss": 0}
            
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

            # Refresh Player ListBox
            players_listbox.delete(0, END)
            for players in total_players_list:
                players_listbox.insert("end", players)
        # Entry Buttons
        Register_plyr_name_btn = Button(
            root1, text="Enter Player to Register", command=registerPlayerName)
        Register_plyr_name_btn.pack(pady=10)
    # Button to direct to Entry
    Register_plyr_btn = Button(
        root, text="Click to Register", command=registerPlayer)
    Register_plyr_btn.pack(pady=10)


def viewPlayerStats():
    # Display Player Treeview
    ws = Tk()
    ws.title('All Player\'s Information')
    ws.geometry('600x300')
    players_tree = ttk.Treeview(ws)

    # Define columns
    players_tree['columns'] = (
        "Name", "Position", "Match Played", "Won", "Loss", "WinRate(%)")

    # Column Headings
    players_tree.heading('#0', text='', anchor=CENTER)
    players_tree.heading("Name", text="Name", anchor=W)
    players_tree.heading("Position", text="Position", anchor=W)
    players_tree.heading("Match Played", text="Match Played", anchor=W)
    players_tree.heading("Won", text="Won", anchor=CENTER)
    players_tree.heading("Loss", text="Loss", anchor=CENTER)
    players_tree.heading("WinRate(%)", text="WinRate(%)", anchor=CENTER)

    # Format columns
    players_tree.column('#0', width=0, stretch=NO)
    players_tree.column("Name", anchor=W, width=120)
    players_tree.column("Position", anchor=CENTER, width=80)
    players_tree.column("Match Played", anchor=CENTER, width=80)
    players_tree.column("Won", anchor=CENTER, width=40)
    players_tree.column("Loss", anchor=CENTER, width=40)
    players_tree.column("WinRate(%)", anchor=CENTER, width=80)

    # Add Data
    if os.path.getsize("player_dict.txt") > 0:
        file = open("player_dict.txt", "r")
        contents = file.read()
        total_players_dict = ast.literal_eval(contents)
        file.close()
    for p_info in total_players_dict.values():
        if p_info['match_played'] == 0:
            winRate = 0
        else:
            winRate = p_info['match_won']/p_info['match_played']*100
        players_tree.insert(parent='', index='end', text="Parent", values=(
            p_info['name'], p_info['position'], p_info['match_played'], p_info['match_won'], p_info['match_loss'],winRate))
        players_tree.pack()

def withdrawPlayerList():
    root = Tk()
    root.title("Remove a player")
    root.geometry("400x400")
    players_listbox = Listbox(root)
    players_listbox.pack(pady=5)
    for players in total_players_list:
        players_listbox.insert("end", players)

    # remove from total_players_list list
    def withdrawPlayer():
        player_to_remove = players_listbox.get(players_listbox.curselection())

        # remove player from OG txt file and output new file without removed player
        with open("ladder.txt", "r") as f:
            lines = f.readlines()
        with open("ladder.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != player_to_remove:
                    f.write(line)
            f.close()
        # Remove from ladder.txt
        total_players_list.remove(player_to_remove)

        # Remove from player_dict.txt
        for id, p_info in total_players_dict.copy().items():
            for key in p_info:
                if p_info[key] == player_to_remove:
                    idx = id
                    del total_players_dict[idx]
                    player_dict = open("player_dict.txt", 'a')
                    player_dict.write(str(total_players_dict))
                    player_dict.write("\n")
                    player_dict.close()
                    break

        # Clear List Box
        players_listbox.delete(0, END)
        # Recreate List Box without removed player
        for players in total_players_list:
            players_listbox.insert("end", players)

    withdraw_plyr_btn = Button(
        root, text="Click to Withdraw", command=withdrawPlayer)
    withdraw_plyr_btn.pack(pady=10)

def issueChallenge():

    def selectPlayerOne(event):
        global selected_item_p1
        selected_item_p1 = playerOne_Tree.focus()
        selected_item_p1 = playerOne_Tree.item(selected_item_p1)['values']

    def selectPlayerTwo(event):
        global selected_item_p2
        selected_item_p2 = playerTwo_Tree.focus()
        selected_item_p2 = playerTwo_Tree.item(selected_item_p2)['values']
    
    root = Tk()
    root.title('Create a Match')
    root.geometry("800x650")

    # Player One Tree
    player1_label = Label(root, text="PLAYER 1",font=("Times New Roman bold",15))
    player1_label.grid(row=0, column=0)
    playerOne_Tree = ttk.Treeview(root)
    playerOne_Tree.grid(row=1, column=0, padx=15)

    playerOne_Tree['columns'] = ("Rank", "Player")

    playerOne_Tree.heading('#0', text='', anchor=CENTER)
    playerOne_Tree.heading("Rank", text="Rank", anchor=CENTER)
    playerOne_Tree.heading("Player", text="Player", anchor=CENTER)

    playerOne_Tree.column('#0', width=0, stretch=NO)
    playerOne_Tree.column("Rank", width="60", anchor=CENTER)
    playerOne_Tree.column("Player", width="120", anchor=CENTER)

    for rank,player in enumerate(total_players_list):
        playerOne_Tree.insert(parent='', index='end', values=(rank+1,player))

    vslabel = Label(root, text="VS", font=("Times New Roman bold",20))
    vslabel.grid(row=1, column=1)

    # Player Two tree
    player2_label = Label(root, text="PLAYER 2",font=("Times New Roman bold",15))
    player2_label.grid(row=0, column=2)
    playerTwo_Tree = ttk.Treeview(root)
    playerTwo_Tree.grid(row=1, column=2, padx=15)

    playerTwo_Tree['columns'] = ("Rank", "Player")

    playerTwo_Tree.heading('#0', text='', anchor=CENTER)
    playerTwo_Tree.heading("Rank", text="Rank", anchor=CENTER)
    playerTwo_Tree.heading("Player", text="Player", anchor=CENTER)

    playerTwo_Tree.column('#0', width=0, stretch=NO)
    playerTwo_Tree.column("Rank", width="60", anchor=CENTER)
    playerTwo_Tree.column("Player", width="120", anchor=CENTER)

    for rank,player in enumerate(total_players_list):
        playerTwo_Tree.insert(parent='', index='end', text="Parent", values=(rank+1,player))  

    # Detached Players goes here 
    playerOne_Tree_detached_items = []
    playerTwo_Tree_detached_items = []

    def selectPlayer1():
        # id_map = {'10': 'A','11': 'B','12': 'C','13': 'D','14': 'E','15': 'F'}
        playerTwo_Tree_detached_items.sort(reverse=True)

        # Reattach players
        for i in playerTwo_Tree_detached_items:
            playerTwo_Tree.reattach(i,'',0)
        playerTwo_Tree_detached_items.clear()

        # Detach Players more than 3 position higher
        for id,i in enumerate(playerTwo_Tree.get_children(),1):
            if id <= selected_item_p1[0]-4:
                plyr2 = 'I00' + str(id)
                playerTwo_Tree.detach(plyr2)
                playerTwo_Tree_detached_items.append(plyr2)

        # Insert into Player1 textbox 
        player1_Entry.configure(state="normal")
        player1_Entry.insert(0,selected_item_p1)   
        player1_Entry.configure(state='disabled')

        return selected_item_p1
    playerOne_Tree.bind('<<TreeviewSelect>>', selectPlayerOne)
    
    def selectPlayer2():
        playerOne_Tree_detached_items.sort(reverse=True)

        # Reattach players
        for i in playerOne_Tree_detached_items:
            playerOne_Tree.reattach(i,'',0)
        playerOne_Tree_detached_items.clear()

        # Detach Players more than 3 position higher
        for id,i in enumerate(playerOne_Tree.get_children(),1):
            if id <= selected_item_p2[0]-4:
                plyr1 = 'I00' + str(id)
                playerOne_Tree.detach('I00' + str(id))
                playerOne_Tree_detached_items.append(plyr1)

        # Insert into Player2 textbox 
        player2_Entry.configure(state="normal")
        player2_Entry.insert(0,selected_item_p2)   
        player2_Entry.configure(state='disabled') 

        return selected_item_p2

    playerTwo_Tree.bind('<<TreeviewSelect>>', selectPlayerTwo)

    # Datepicker
    Date_frame = Frame(root, bg="grey")
    Date_frame.grid(row=5, column=2, sticky=NSEW) 
    Date_label = Label(root, text="DATE OF MATCH",font=("Times New Roman bold",15))
    Date_label.grid(row=4, column=2)
    cal = Calendar(Date_frame, selectmode="day", year=2021, month=5, day=22)
    cal.grid(row=6, column=2, columnspan=2, sticky=W)
    
    def grab_date():
        # Insert into Date textbox 
        match_date_Entry.configure(state="normal")
        match_date_Entry.insert(0,cal.get_date())
        match_date_Entry.configure(state="disabled")
        return cal.get_date()

    # Date Button
    select_date_btn = Button(
        root, text="Select Date", command=grab_date)
    select_date_btn.grid(row=7, column=2, pady=10)

    def createMatch():
        upcoming_match[len(upcoming_match) + 1] = {'Player1': selectPlayer1(), "VS": 'VS', 'Player2': selectPlayer2(), "Date": cal.get_date()}
        
        f = open("upcoming_match.txt", 'a')
        f.write(str(upcoming_match))
        f.write("\n")
        f.close()

        # Delete first line if there is more than 1 line
        with open('upcoming_match.txt', 'r') as fin:
            lines = fin.read().splitlines(True)
        if len(lines) > 1 and len(lines) != 1:
            with open('upcoming_match.txt', 'w') as fout:
                fout.writelines(lines[1:])

    # Player1 Button
    select_plyr_btn = Button(
        root, text="Select Player 1", command=selectPlayer1)
    select_plyr_btn.grid(row=3, column=0, pady=10)

    # Match Details 
    player1_frame = Frame(root,bg="grey",)
    player1_frame.grid(row=4,column=0, rowspan=4, padx=20)
    match_detail = Label(player1_frame, text="Match Details", font=("Times New Roman bold", 13))
    match_detail.grid(row=4, column=0, pady=10, padx=10)

    # Player1 TextBox 
    player1_text_label = Label(player1_frame, text="Player 1: ", font=("Times New Roman bold", 10)) 
    player1_text_label.grid(row=6, column=0)
    player1_Entry = Entry(player1_frame, text="")
    player1_Entry.grid(row=6,column=1, pady=10, padx=10)

    # Player2 Button
    select_plyr_btn = Button(
        root, text="Select Player 2", command=selectPlayer2)
    select_plyr_btn.grid(row=3, column=2,pady=10)

    # Player2 TextBox 
    player2_text_label = Label(player1_frame, text="Player 2: ", font=("Times New Roman bold", 10)) 
    player2_text_label.grid(row=7, column=0)
    player2_Entry = Entry(player1_frame, text="")
    player2_Entry.grid(row=7,column=1)

    # Match Date TextBox 
    match_date_text_label = Label(player1_frame, text="Date: ",font=("Times New Roman bold", 10)) 
    match_date_text_label.grid(row=8, column=0)
    match_date_Entry = Entry(player1_frame, text="")
    match_date_Entry.grid(row=8,column=1, pady=10)

    # Confirm Match Button
    cfm_match_btn = Button(root, text="Create Match", pady=10, padx=20, command=createMatch)
    cfm_match_btn.grid(row=8, column=1, pady=5)

