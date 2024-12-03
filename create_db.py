import sqlite3
    

def create_predictions_db():
    connection = sqlite3.connect('predictions.db')
    cursor = connection.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS tournaments (
trn_id INTEGER PRIMARY KEY,
trn_name TEXT NOT NULL,
trn_status TEXT NOT NULL,
UNIQUE ("trn_name") ON CONFLICT IGNORE
)
''')
    cursor.execute('INSERT INTO tournaments (trn_name, trn_status) VALUES (?, ?)', ('Perfect World Shanghai Major 2024 Opening Stage', 'Upcoming'))
    cursor.execute('INSERT INTO tournaments (trn_name, trn_status) VALUES (?, ?)', ('Perfect World Shanghai Major 2024', 'Upcoming'))


    cursor.execute('''
CREATE TABLE IF NOT EXISTS matches (
match_id INTEGER PRIMARY KEY,
trn_name TEXT NOT NULL,
team_a TEXT NOT NULL,
team_b TEXT NOT NULL,
match_time TEXT NOT NULL,
match_type TEXT NOT NULL,
match_status TEXT NOT NULL,
team_a_win INTEGER,
team_b_win INTEGER,
team_a_score INTEGER,
team_b_score INTEGER,
prediction_points INTEGER
)
''')
    cursor.execute('INSERT INTO matches (trn_name, team_a, team_b, match_time, match_type, match_status, team_a_score, team_b_score, prediction_points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  ('Perfect World Shanghai Major 2024 Opening Stage', 'Furia', 'GamerLegion', '6:00 (MSK)', 'BO1', 'Upcoming', 0, 0, 100))
    cursor.execute('INSERT INTO matches (trn_name, team_a, team_b, match_time, match_type, match_status, team_a_score, team_b_score, prediction_points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  ('Perfect World Shanghai Major 2024 Opening Stage', 'Virtus.pro', 'MIBR', '6:00 (MSK)', 'BO1', 'Upcoming', 0, 0, 100))
    cursor.execute('INSERT INTO matches (trn_name, team_a, team_b, match_time, match_type, match_status, team_a_score, team_b_score, prediction_points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  ('Perfect World Shanghai Major 2024 Opening Stage', 'Liquid', 'Cloud9', '7:00 (MSK)', 'BO1', 'Upcoming', 0, 0, 100))
    cursor.execute('INSERT INTO matches (trn_name, team_a, team_b, match_time, match_type, match_status, team_a_score, team_b_score, prediction_points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  ('Perfect World Shanghai Major 2024 Opening Stage', 'Complexity', 'FlyQuest', '7:00 (MSK)', 'BO1', 'Upcoming', 0, 0, 100))
    cursor.execute('INSERT INTO matches (trn_name, team_a, team_b, match_time, match_type, match_status, team_a_score, team_b_score, prediction_points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  ('Perfect World Shanghai Major 2024 Opening Stage', 'BIG', 'Passion UA', '8:00 (MSK)', 'BO1', 'Upcoming', 0, 0, 100))
    cursor.execute('INSERT INTO matches (trn_name, team_a, team_b, match_time, match_type, match_status, team_a_score, team_b_score, prediction_points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  ('Perfect World Shanghai Major 2024 Opening Stage', 'fnatic', 'Wildcard', '8:00 (MSK)', 'BO1', 'Upcoming', 0, 0, 100))
    cursor.execute('INSERT INTO matches (trn_name, team_a, team_b, match_time, match_type, match_status, team_a_score, team_b_score, prediction_points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  ('Perfect World Shanghai Major 2024 Opening Stage', 'The MongolZ', 'Rare Atom', '9:00 (MSK)', 'BO1', 'Upcoming', 0, 0, 100))
    cursor.execute('INSERT INTO matches (trn_name, team_a, team_b, match_time, match_type, match_status, team_a_score, team_b_score, prediction_points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                  ('Perfect World Shanghai Major 2024 Opening Stage', 'paiN', 'Imperial', '9:00 (MSK)', 'BO1', 'Upcoming', 0, 0, 100))

    cursor.execute('''
CREATE TABLE IF NOT EXISTS predicts (
tid INTEGER,
match_id INTEGER,
predict INTEGER
)
''')

    connection.commit()
    connection.close()