from flask import Flask, jsonify, request, abort
import json
import sqlite3

#David De La Cruz

app = Flask(__name__)

#Holds data to be returned as JSON
thread = [{"id": 0, "thread": None}]
message = [{"threadId": 0, "messagedId": 0, "message": None}]

#Creates database
con = sqlite3.connect('db/forum.db')
con.execute('''CREATE TABLE IF NOT EXISTS THREAD(Id INT PRIMARY KEY, Name TEXT);''')
con.execute('''CREATE TABLE IF NOT EXISTS MESSAGE(MessageId INT PRIMARY KEY, ThreadId INT NOT NULL, Message TEXT);''')
con.commit()
con.close()


@app.route('/')
def index():
    output = "Assignment 7: Flask forum <br/> David De La Cruz<br/><br/><br/><br/>RESTFUL API takes JSON and returns results"
    return output


@app.route('/thread', methods=['GET'])
def get_all_threads():
    with sqlite3.connect('db/forum.db') as db:
        cursor = db.execute("SELECT * FROM THREAD")
        rows = cursor.fetchall()
        if len(rows) == 0:
            return "Store things in database table THREAD, its currently empty!"
        else:
            threads = []
            for row in rows:
                k, v = row
                output = "id: {}, thread: {}".format(k, v)
                threads.append(output)
            return jsonify({'threads': threads})


@app.route('/thread/<int:thread_id>', methods=['GET'])
def get_thread(thread_id):
    with sqlite3.connect('db/forum.db') as db:
        cursor = db.execute("SELECT * FROM THREAD WHERE Id = ?", str(thread_id))
        rows = cursor.fetchall()
        if len(rows) == 0:
            abort(404)
        for row in rows:
            thread[0]['id'] = row[0]
            thread[0]['thread'] = row[1]
        return jsonify({'thread': thread[0]})


@app.route('/thread/<int:thread_id>/message', methods=['GET'])
def get_all_thread_messages(thread_id):
    with sqlite3.connect('db/forum.db') as db:
        cursor = db.execute("SELECT * FROM MESSAGE WHERE ThreadId = ?", str(thread_id))
        rows = cursor.fetchall()
        if len(rows) == 0:
            abort(404)
        messages = []
        for row in rows:
            mid, tid, mess = row
            output = "threadId: {}, messagedId: {}, message: {}".format(tid, mid, mess)
            messages.append(output)
        return jsonify({'messages': messages})


@app.route('/thread/<int:thread_id>/message/<int:message_id>', methods=['GET'])
def get_specific_message(thread_id, message_id):
    with sqlite3.connect('db/forum.db') as db:
        cursor = db.execute("SELECT * FROM MESSAGE WHERE ThreadId = ? AND MessageId = ?", (str(thread_id), str(message_id)))
        rows = cursor.fetchall()
        if len(rows) == 0:
            abort(404)
        message.clear()
        message.append({})
        for row in rows:
            message[0]['MessageId'], message[0]['ThreadId'], message[0]['Message'] = row
        return jsonify({'message': message})


@app.route('/thread/<int:thread_id>/message', methods=['POST'])
def create_message(thread_id):
    with sqlite3.connect('db/forum.db') as db:
        id = 0

        if not request.json or not 'message' in request.json:
            abort(400)

        cursorid = db.execute("SELECT * from MESSAGE ORDER BY MessageId DESC LIMIT 1")

        for ID in cursorid:
            id = ID[0]

        db.execute("INSERT OR IGNORE INTO MESSAGE(MessageId,ThreadId,Message) VALUES (?,?,?)", (id + 1, str(thread_id), request.json['message']))
        cursor = db.execute("SELECT * FROM MESSAGE WHERE MessageId = ?", str(id + 1))
        rows = cursor.fetchall()
        message.clear()
        message.append({})
        for row in rows:
            message[0]['MessageId'], message[0]['ThreadId'], message[0]['Message'] = row
        db.commit()
        return jsonify({'message': message}), 201


@app.route('/thread', methods=['POST'])
def create_thread():
    with sqlite3.connect('db/forum.db') as db:
        id = 0

        if not request.json or not 'thread' in request.json:
            abort(400)

        cursorid = db.execute("SELECT * from THREAD ORDER BY Id DESC LIMIT 1")

        for ID in cursorid:
            id = ID[0]

        db.execute("INSERT OR IGNORE INTO THREAD(Id,Name) VALUES (?,?)", (id + 1, request.json['thread']))
        db.commit()
        cursor = db.execute("SELECT * FROM THREAD WHERE Id = ?", str(id + 1))
        for row in cursor:
            thread[0]['id'], thread[0]['thread'] = row
        return jsonify({'thread': thread}), 201


@app.route('/thread/<int:thread_id>/message/<int:message_id>', methods=['DELETE'])
def delete_message(thread_id, message_id):
    with sqlite3.connect('db/forum.db') as db:
        db.execute("DELETE FROM MESSAGE WHERE ThreadId = ? AND MessageId = ?", (str(thread_id), str(message_id)))
        return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)