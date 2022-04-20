import sqlite3
import json
from models import Entry, Mood, EntryTag, Tag


def get_all_entries():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id,
            m.label
        FROM Entry e
        JOIN Mood m
            ON e.mood_id = m.id
        """)

        entries = []
        dataset = db_cursor.fetchall()
       
        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['date'], row['mood_id'])
            mood = Mood(row['mood_id'], row['label'])
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
            
            db_cursor.execute("""
            SELECT
                t.id,
                t.name
            FROM Tag t
            JOIN EntryTag et
                ON t.id = et.tag_id AND et.entry_id = ?
            """, (row['id'],))
            tags = []
            tag_dataset = db_cursor.fetchall()
            for tag_row in tag_dataset:
                tag = Tag(tag_row['id'], tag_row['name'])
                tags.append(tag.__dict__)
            entry.tags = tags
            entries.append(entry.__dict__)
    return json.dumps(entries)


def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id
        FROM Entry e
        WHERE e.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'], data['concept'],
                      data['entry'], data['date'], data['mood_id'])

        return json.dumps(entry.__dict__)


def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entry
        WHERE id = ?
        """, (id, ))


def get_entry_by_search(entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id
        FROM Entry e
        WHERE e.entry LIKE ?
        """, (f"%{entry}%", ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['date'], row['mood_id'])
            entries.append(entry.__dict__)
    return json.dumps(entries)


def create_journal_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO Entry
            (concept, entry, date, mood_id )
        VALUES
            (?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['moodId']))
        id = db_cursor.lastrowid
        new_entry['id'] = id
        for tag in new_entry['tag']:
            db_cursor.execute("""
            INSERT INTO EntryTag
                (tag_id, entry_id)
            VALUES
                (?, ?);
            """, (tag, id,) )
    return json.dumps(new_entry)


def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                concept = ?,
                entry = ?,
                date = ?,
                mood_id = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['date'], new_entry['moodId'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
