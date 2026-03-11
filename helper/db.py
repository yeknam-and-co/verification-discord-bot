import sqlite3

def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS guilds (guild_id INTEGER PRIMARY KEY, channel_id INTEGER, role_id INTEGER, staff_channel_id INTEGER)''')
    conn.commit()
    conn.close()

def add_guild(guild_id, channel_id, role_id, staff_channel_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO guilds (guild_id, channel_id, role_id, staff_channel_id) VALUES (?, ?, ?, ?)', (guild_id, channel_id, role_id, staff_channel_id))
    conn.commit()
    conn.close()

def fetch_guild_role(guild_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT role_id FROM guilds WHERE guild_id = ?', (guild_id,))
    role_id = c.fetchone()
    conn.close()
    return role_id[0]

def fetch_guild_staff_channel(guild_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT staff_channel_id FROM guilds WHERE guild_id = ?', (guild_id,))
    staff_channel_id = c.fetchone()
    conn.close()
    return staff_channel_id[0]

def fetch_entire_guild(guild_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM guilds WHERE guild_id = ?', (guild_id,))
    guild = c.fetchone()
    conn.close()
    return guild