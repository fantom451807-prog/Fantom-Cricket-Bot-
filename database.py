import sqlite3
import random

def get_conn():
    # check_same_thread=False is essential for handling multiple users at once
    return sqlite3.connect("cricket.db", check_same_thread=False)

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    
    # 1. Players Table (Master list of all cricketers added by Admin)
    cursor.execute('''CREATE TABLE IF NOT EXISTS players 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT, 
                       rarity TEXT, 
                       file_id TEXT)''')
    
    # 2. Collection Table (Players owned by users)
    cursor.execute('''CREATE TABLE IF NOT EXISTS collections 
                      (user_id INTEGER, 
                       name TEXT, 
                       rarity TEXT)''')
    
    # 3. Users Table (Tracking bot users)
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, 
                       username TEXT)''')
    
    # 4. Banned Users Table (Fixes the ban.py ImportError)
    cursor.execute('''CREATE TABLE IF NOT EXISTS banned_users 
                      (user_id INTEGER PRIMARY KEY)''')

    # 5. Favorites Table (Stores the player photo for /fav)
    cursor.execute('''CREATE TABLE IF NOT EXISTS favorites 
                      (user_id INTEGER PRIMARY KEY, 
                       player_name TEXT, 
                       file_id TEXT)''')
    
    conn.commit()
    conn.close()
    print("✅ Database System Initialized Successfully!")

# --- Admin Functions ---
def add_player_to_db(name, rarity, file_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (name, rarity, file_id) VALUES (?, ?, ?)", 
                   (name, rarity, file_id))
    conn.commit()
    conn.close()

def get_random_player():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name, rarity, file_id FROM players")
    res = cursor.fetchall()
    conn.close()
    return random.choice(res) if res else None

# --- User & Collection Functions ---
def add_user(u_id, user_n):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?,?)", (u_id, user_n))
    conn.commit()
    conn.close()

def save_collected_player(u_id, p_n, p_r):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO collections VALUES (?,?,?)", (u_id, p_n, p_r))
    conn.commit()
    conn.close()

def get_user_collection(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT name, rarity FROM collections WHERE user_id = ?", (user_id,))
    res = cursor.fetchall()
    conn.close()
    return res

# --- Favorite System Functions ---
def set_fav(user_id, p_name, f_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO favorites VALUES (?, ?, ?)", (user_id, p_name, f_id))
    conn.commit()
    conn.close()

def get_fav(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, file_id FROM favorites WHERE user_id = ?", (user_id,))
    res = cursor.fetchone()
    conn.close()
    return res

# --- Ban System Functions ---
def ban_user(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO banned_users VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def unban_user(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def is_user_banned(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM banned_users WHERE user_id = ?", (user_id,))
    res = cursor.fetchone()
    conn.close()
    return res is not None

# Auto-initialize on import
init_db()