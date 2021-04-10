import tkinter as tk
from tkinter import ttk
from tkinter import *

import turtle
import os
import ast
import tkinter as tk
from tkinter import *
from tkinter import ttk

# Total Players in the ladder
total_players_list = []
total_players_dict = {}
upcoming_match = {}


def loadPlayers():
    #  open ladder.txt in read mode
    f = open('ladder.txt', 'r')
    # load list data
    for line in f:
        total_players_list.append(line.strip())


loadPlayers()


def registerPlayerList():
    root = Tk()
    root.title("Register a player")
    root.geometry("400x400")
    players_listbox = Listbox(root)
    players_listbox.pack(pady=5)
    for players in total_players_list:
        players_listbox.insert("end", players)
    # add to total_players_list list

    def registerPlayer():
        root1 = Tk()
        e = Entry(root1, width='80')
        e.pack()

        def registerPlayerName():
            # Labels
            eLabel = Label(root1, text="Player: " +
                           e.get() + " is registered!")
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
            total_players_dict[len(total_players_dict) + 1] = {'name': e.get(), 'position': len(total_players_dict) + 1,
                                                               "match_played": 0, "match_won": 0, "match_loss": 0}
            # save dictionary to text file
            os.remove("player_dict.txt")
            player_dict = open("player_dict.txt", 'a')
            player_dict.write(str(total_players_dict))
            player_dict.write("\n")
            player_dict.close()

            # Clear List Box
            players_listbox.delete(0, END)
            # Recreate List Box without removed player
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


def viewAllPlayers():
    # Display Player Treeview
    ws = Tk()
    ws.title('PythonGuides')
    ws.geometry('400x300')
    players_tree = ttk.Treeview(ws)

    # Define columns
    players_tree['columns'] = (
        "Name", "Position", "Match Played", "Won", "Loss")

    # Column Headings
    players_tree.heading('#0', text='', anchor=CENTER)
    players_tree.heading("Name", text="Name", anchor=W)
    players_tree.heading("Position", text="Position", anchor=W)
    players_tree.heading("Match Played", text="Match Played", anchor=W)
    players_tree.heading("Won", text="Won", anchor=CENTER)
    players_tree.heading("Loss", text="Loss", anchor=CENTER)

    # Format columns
    players_tree.column('#0', width=0, stretch=NO)
    players_tree.column("Name", anchor=W, width=120)
    players_tree.column("Position", anchor=CENTER, width=80)
    players_tree.column("Match Played", anchor=CENTER, width=80)
    players_tree.column("Won", anchor=CENTER, width=40)
    players_tree.column("Loss", anchor=CENTER, width=40)

    # Add Data
    if os.path.getsize("player_dict.txt") > 0:
        file = open("player_dict.txt", "r")
        contents = file.read()
        total_players_dict = ast.literal_eval(contents)
        file.close()
    for p_info in total_players_dict.values():
        players_tree.insert(parent='', index='end', text="Parent", values=(
            p_info['name'], p_info['position'], p_info['match_played'], p_info['match_won'], p_info['match_loss']))
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
                    # Recreate player_dict.txt
                    os.remove("player_dict.txt")
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


def populatePlayersInListBox():
    root = Tk()
    root.title('Player1 VS Player2')
    root.geometry("400x400")
    players_listbox = Listbox(root)
    players_listbox.grid(row=0, column=300)

    player1_label = Label(root, text="Player 1")
    player1_label.grid(row=1, column=1, pady=2)
    player1 = Label(root, text="")
    player1.grid(row=2, column=1, pady=2)
    versus_label = Label(root, text="VS")
    versus_label.grid(row=1, column=2, pady=2)
    player2_label = Label(root, text="Player 2")
    player2_label.grid(row=1, column=3, pady=2)
    player2 = Label(root, text="")
    player2.grid(row=2, column=3, pady=2)
    for players in total_players_list:
        players_listbox.insert("end", players)

    def selectPlayer1():
        sel_player1 = players_listbox.curselection()
        player1.config(text=players_listbox.get(sel_player1))

    def selectPlayer2():
        sel_player2 = players_listbox.curselection()
        player2.config(text=players_listbox.get(sel_player2))

    def createMatch():
        upcoming_match[len(
            upcoming_match) + 1] = {'Player1': player1.config(text=players_listbox.get(sel_player1)), "VS": 'VS', 'Player2': player2.config(text=players_listbox.get(sel_player2)), "Date": 0}
        f = open("upcoming_match.txt", 'a')
        f.write(str(upcoming_match))
        f.write("\n")
        f.close()

        # save dictionary to text file
        # os.remove("upcoming_match.txt")
        # f = open("upcoming_match.txt", 'a')
        # f.write(str(upcoming_match))
        # f.write("\n")
        # f.close()

    # select P1
    select_plyr_btn = Button(
        root, text="Select Player 1", command=selectPlayer1)
    select_plyr_btn.grid(row=200, column=200)

    # select P2
    select_plyr_btn = Button(
        root, text="Select Player 2", command=selectPlayer2)
    select_plyr_btn.grid(row=200, column=400)

    # Confirm Match
    cfm_match_btn = Button(
        root, text="Create Match", command=createMatch)
    cfm_match_btn.grid(row=300, column=300)