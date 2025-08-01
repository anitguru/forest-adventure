# 🌲 **Forest Adventure – Early-Beta Design Plan** 🌲
*(Simple 1-player text game for Everett or Corinne, ages 9+)*

---

### 1. File Layout (for now)

| File                                    | Purpose                                                                                                                       |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **`forest_adventure.py`**               | Main game script you’ll run with `jython forest_adventure.py`. All logic lives here for this first cut.                       |
| *(optional later)* `assets/banners.txt` | Store big ASCII/emoji banners so they don’t clutter the code. We’ll inline them today and break them out once the list grows. |

---

### 2. Game Flow

1. **Title banner** → Ask “Who’s playing?”

   ```
   1) Everett 🧑
   2) Corinne 👧
   ```

   Your choice sets:

   * Main character name & pronouns
   * Rescue target: **princess** (if Everett) or **prince** (if Corinne)

2. **Intro scene**

   * Short forest description with green-tinted ANSI text (works in most Windows 11 terminals, Jython included).

3. **Main loop** (simple menu each turn)

   ```
   What now?
   1) Explore 🌳
   2) Check inventory 🎒
   3) Drink potion ❤️
   4) Quit
   ```

4. **Explore outcome** (weighted random):

   | Event              | Details                                                                   |
   | ------------------ | ------------------------------------------------------------------------- |
   | Treasure chest 💰  | Contains gold, a shiny sword 🗡️, or a compass 🧭 (never harmful).        |
   | Healing vial 🧪    | +2 HP (max 10).                                                           |
   | Monster appears 👹 | Slime / Goblin / Wolf / Mischievous Pixie (each with “smarts” stat).      |
   | Quiet clearing 🌼  | Flavor text, no effect (keeps tempo comfy).                               |
   | Hidden path 🏰     | Shows up once you possess the compass ⇒ leads to final showdown & rescue. |

5. **Monster Encounter menu**

   ```
   A Wild Slime squelches in your path!
   1) Talk 💬
   2) Run 🏃
   3) Fight ⚔️
   ```

   * **Talk** → Success % = monster\_smarts × 60 %.  Success rewards clue or item; fail drops you into combat.
   * **Run** → 70 % success; fail means combat round (but you always get a second menu after each round).
   * **Fight** → Very simple math: player attack = 1 (+1 if sword). Monster attack = 1. First to 0 HP “loses the will to fight…”

     * **Player defeat** ⇒ “GAME OVER” 80-style banner, HP resets, inventory keeps **one** random item (kid-friendly).
     * **Monster defeat** ⇒ random loot or passage opens.

6. **Goal & Ending**

   * Reach castle path, beat or befriend the castle guardian.
   * Show victory banner with rescued **princess** / **prince**, credits roll.
   * Offer “Play again?” prompt.

---

### 3. Technical Notes

* **Python version**: Stick to Python 2.7-compatible syntax so Jython 2.7.4 runs happily (`print()` from `__future__` for cleanliness).
* **Randomness**: use `random.choice` / `random.randint`.
* **ANSI colors**: Simple helper `color(text, fg='green')` that injects `\033[32m…\033[0m`. Windows 10+ terminal honors this by default.
* **Data structures**:

  ```python
  monsters = [
      {"name": "Slime", "hp": 3, "smarts": 0.2, "art": "( ooze )"},
      ...
  ]
  items = ["Gold Coins", "Silver Sword", "Sparkly Compass"]
  ```
* **No external libraries** (so users don’t need to `pip install`).

---

### 4. Next Steps After Approval

1. Generate **`forest_adventure.py`** with:

   * Title/banner constants
   * Utility `cls()` to clear console for cleaner screens
   * `Player` class (hp, inventory, has\_compass, is\_corinne flag)
   * Functions: `intro()`, `main_menu()`, `explore()`, `encounter_monster()`, `fight()`, `talk()`, `run_away()`, `victory()`
2. You copy-paste into a file anywhere on disk and run `jython forest_adventure.py`.
3. Iterate: add sound cues, ASCII maps, multi-file structure, save/load, etc.

