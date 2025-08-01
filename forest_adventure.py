#!/usr/bin/env jython

# coding: utf-8

from __future__ import print_function

import random, os, sys, time



# ------------ helpers ------------

def cls():

    """Clear console on Windows, Linux, macOS, and Jython."""

    if os.system('cls') == 0:              # PowerShell / cmd

        return

    if os.system('clear') == 0:            # Unix-like shells

        return

    sys.stdout.write('\033[2J\033[H')      # ANSI fallback

    sys.stdout.flush()



def supports_emoji():

    enc = (sys.stdout.encoding or '').lower()

    return 'utf-8' in enc or 'utf8' in enc



# Icons & safe ASCII fallbacks

EMO = {

    'tree'  : "[Forest]",

    'lake'  : "[Lake]",

    'bag'   : "[Bag]",

    'heart' : "<3",

}



ANSI = {'reset': '\033[0m', 'green': '\033[32m', 'cyan': '\033[36m',

        'yellow': '\033[33m', 'magenta': '\033[35m', 'red': '\033[31m'}



def color(txt, fg='green'):

    return ANSI.get(fg, '') + txt + ANSI['reset']



def pause(sec=1.2):

    time.sleep(sec)



def inp(prompt):

    try:

        return raw_input(prompt)          # Jython / Python 2

    except NameError:

        return input(prompt)              # Python 3 (if using CPython)



# ------------ banners ------------

TITLE_TEMPLATE = r"""

                                    .     .  .      +     .      .          .

                   .       .      .     #     .           .                    .

                      .      .         ###            .      .      .

                    .      .   "#:. .:##"##:. .:#"  .      .

                        .      . "####"###"####"  .

                     .     "#:.    .:#"###"#:.    .:#"  .        .       .

                .             "#########"#########"        .        .

                      .    "#:.  "####"###"####"  .:#"   .       .

                   .     .  "#######""##"##""#######"                  .

                              ."##"#####"#####"##".       .       .

                  .   "#:. ...  .:##"###"###"##:.  ... .:#"     .

                    .     "#######"##"#####""#######"      .     .

                  .    .     "#####""#####"##""#####"

                          .     "      000      "    .     .

                      .         0000000  0000000      .          .

      [*]  F O R E S T   A D V E N T U R E   [*]          00000000000       .

                                                    0000000000000000

"""



GAME_OVER = r"""

+================================+

|   You have been defeated! </3  |

|  You lose the will to fight!   |

+================================+

"""



VICTORY = r"""

+================================+

|       *** V I C T O R Y ! ***  |

+================================+

"""



# ------------ data ------------

MONSTERS = [

    {"name": "Slime",  "hp": 3, "smarts": 0.2, "art": "( o.o )"},

    {"name": "Goblin", "hp": 4, "smarts": 0.4, "art": "( >:( )"},

    {"name": "Wolf",   "hp": 5, "smarts": 0.3, "art": "( ^.^ )"},

    {"name": "Pixie",  "hp": 2, "smarts": 0.7, "art": "( *o* )"},

]

TREASURES = ["Gold Coins [*]", "Silver Sword [/]", "Sparkly Compass [+]"]



FINAL_BOSS = {"name": "Shadow Serpent", "hp": 8, "smarts": 0.5,

              "art": "~( -.- )~"}



# ------------ classes ------------

class Player(object):

    def __init__(self, gender):

        self.gender = gender            # 'boy' or 'girl'

        self.max_hp = 10

        self.hp = 10

        self.inv = []

        self.defeated = 0               # regular monsters defeated

        self.boss_defeated = False



    @property

    def sword(self):

        return any("Sword" in i for i in self.inv)



    @property

    def compass(self):

        return any("Compass" in i for i in self.inv)



    def heal(self, amt):

        self.hp = min(self.max_hp, self.hp + amt)



# ------------ core gameplay ------------

def choose_player():

    cls()

    print(color(TITLE_TEMPLATE, 'cyan'))

    print("Are you a brave boy or a clever girl?")

    print(" 1) Boy  {}".format(EMO['tree']))

    print(" 2) Girl {}".format(EMO['lake']))

    while True:

        c = inp("> ").strip()

        if c == "1":

            return Player("boy")

        if c == "2":

            return Player("girl")



def main_menu():

    print("\n" + color("What will you do?", 'yellow'))

    print(" 1) Explore {}".format(EMO['tree']))

    print(" 2) Check inventory {}".format(EMO['bag']))

    print(" 3) Drink potion {}".format(EMO['heart']))

    print(" 4) Quit")

    return inp("> ").strip()



def explore(p):

    roll = random.randint(1, 100)

    if roll <= 25:

        chest(p)

    elif roll <= 45:

        potion(p)

    elif roll <= 70:

        monster_encounter(p)

    elif roll <= 90:

        print(color("A peaceful glade sways in the breeze... [flower]", 'green'))

    else:

        hidden_path(p)



def chest(p):

    print(color("\nYou find a sturdy treasure chest! [gem]", 'yellow'))

    loot = random.choice(TREASURES)

    p.inv.append(loot)

    print(color("Inside you discover: " + loot, 'cyan'))



def potion(p):

    print(color("\nYou spot a glowing vial of healing potion! [vial]", 'yellow'))

    p.inv.append("Healing Vial [vial]")



def monster_encounter(p):

    m = dict(random.choice(MONSTERS))

    print(color("\nA wild {} appears! {}".format(m['name'], m['art']), 'red'))

    while m['hp'] > 0:

        print("\n 1) Talk [chat]  2) Run [run]  3) Fight [sword]")

        choice = inp("> ").strip()

        if choice == "1":

            talk(p, m)

            if m['hp'] <= 0:

                break

        elif choice == "2":

            if run_away():

                print(color("You dash through the bushes and escape!", 'cyan'))

                return

            else:

                print(color("Couldn't shake it off!", 'red'))

        fight_round(p, m)

        if p.hp <= 0:

            death(p)

            return

    if m['hp'] <= 0:

        p.defeated += 1

        victory_loot(p)

        if p.defeated >= 2 and not p.boss_defeated:

            final_boss(p)



def talk(p, m):

    success = random.random() < m['smarts']

    if success:

        print(color("You strike up a friendly chat. The {} smiles!".format(m['name']), 'green'))

        if random.random() < 0.5:

            clue = "\"Seek the ancient oak.\" [tree]"

            print(color("It shares a clue: {}".format(clue), 'yellow'))

        else:

            gift = random.choice(TREASURES)

            p.inv.append(gift)

            print(color("It hands you a gift: {}".format(gift), 'cyan'))

        m['hp'] = 0

    else:

        print(color("It snarls back--no luck!", 'red'))



def run_away():

    return random.random() < 0.7



def fight_round(p, m):

    dmg_p = 1 + (1 if p.sword else 0)

    dmg_m = 1

    m['hp'] -= dmg_p

    print(color("You deal {} damage.".format(dmg_p), 'cyan'))

    if m['hp'] <= 0:

        print(color("The {} loses the will to fight...".format(m['name']), 'green'))

        return

    p.hp -= dmg_m

    print(color("The {} hits you for {}!".format(m['name'], dmg_m), 'red'))

    print(color("HP: {}/{}".format(p.hp, p.max_hp), 'yellow'))



def final_boss(p):

    print(color("\n[!]  FINAL BOSS ENCOUNTER! [!]", 'magenta'))

    boss = dict(FINAL_BOSS)  # copy so stats reset on replay

    print(color("{} emerges from the shadows! {}".format(boss['name'], boss['art']), 'red'))

    while boss['hp'] > 0:

        print("\n 1) Talk [chat]  2) Run [run]  3) Fight [sword]")

        choice = inp("> ").strip()

        if choice == "1":

            talk(p, boss)

            if boss['hp'] <= 0:

                break

        elif choice == "2":

            print(color("There's nowhere to run!", 'red'))

        fight_round(p, boss)

        if p.hp <= 0:

            death(p)

            return

    # Victory!

    p.boss_defeated = True

    cls()

    print(color(VICTORY, 'yellow'))

    print(color("You defeat the Shadow Serpent and save the princess of the forest! [flower][crown]", 'green'))

    replay = inp("\nPlay again? (y/n) ").lower().startswith('y')

    if replay:

        run_game()

    else:

        sys.exit()



def death(p):

    cls()

    print(color(GAME_OVER, 'magenta'))

    keep = random.choice(p.inv) if p.inv else None

    p.inv = [keep] if keep else []

    p.hp = p.max_hp

    p.defeated = 0

    inp(color("Press Enter to continue...", 'cyan'))

    cls()



def victory_loot(p):

    if random.random() < 0.5:

        loot = random.choice(TREASURES)

        p.inv.append(loot)

        print(color("You gained: {}".format(loot), 'cyan'))



def hidden_path(p):

    if not p.compass:

        print(color("You wander but find nothing unusual...", 'green'))

        return

    print(color("\nYour compass glows and a hidden path opens! [castle]", 'yellow'))

    final_boss(p)



def drink_potion(p):

    for i, item in enumerate(p.inv):

        if "Vial" in item:

            p.heal(2)

            del p.inv[i]

            print(color("You feel revitalized! HP: {}/{}".format(p.hp, p.max_hp), 'green'))

            return

    print(color("No potions left!", 'red'))



def show_inventory(p):

    print(color("\nInventory:", 'cyan'))

    if not p.inv:

        print("  (empty)")

    else:

        for it in p.inv:

            print("  - " + it)

    print(color("HP: {}/{}".format(p.hp, p.max_hp), 'yellow'))



# ------------ main ------------

def run_game():

    player = choose_player()

    cls()

    print(color("Welcome, brave hero! Your quest: save the princess of the forest!", 'green'))

    pause()

    while True:

        choice = main_menu()

        if choice == "1":

            explore(player)

        elif choice == "2":

            show_inventory(player)

        elif choice == "3":

            drink_potion(player)

        elif choice == "4":

            print(color("Farewell, brave adventurer!", 'cyan'))

            break

        else:

            print(color("Invalid choice.", 'red'))

        pause(0.8)



if __name__ == "__main__":

    run_game()

