from flask import Flask,jsonify,request
from flask_mysqldb import MySQL

app = Flask (__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'universitas'
mysql=MySQL(app)

@app.route('/')
def root():
    return 'Selamat datang di tugas restful API'

@app.route('/person')
def person():
    return jsonify({'name': 'alfi',
                    'address': 'bandung'})

@app.route('/dosen', methods=['GET', 'POST'])
def dosen():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM DOSEN")
        
        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        return jsonify(data)
        cursor.close()
    
    elif request.method == 'POST':
        nama = request.json['nama']
        univ = request.json['univ']
        jurusan = request.json['jurusan']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO DOSEN (nama, univ, jurusan) VALUES (%s, %s, %s)"
        val = (nama, univ, jurusan)
        cursor.execute(sql,val)
        
        mysql.connection.commit()

        return jsonify({'message': 'data added successfully!'})
        cursor.close()

@app.route('/detaildosen')
def detaildosen():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM dosen WHERE dosenid = %s"
        val = (request.args['id'],)
        cursor.execute(sql,val)

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        return jsonify(data)
        cursor.close()

@app.route('/deletedosen', methods=['DELETE'])
def deletedosen():
        if 'id' in request.args:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM dosen WHERE dosenid = %s"
            val = (request.args['id'],)
            cursor.execute(sql,val)
            
            mysql.connection.commit()

            return jsonify({'message': 'data deleted successfully!'})
            cursor.close()

@app.route('/editdosen', methods=['PUT'])
def editdosen():
    if 'id' in request.args:
        data= request.get_json()
        cursor=mysql.connection.cursor()
        sql="UPDATE dosen SET nama=%s, univ=%s, jurusan=%s WHERE dosenid=%s "
        val= (data['nama'], data['univ'], data['jurusan'], request.args['id'])
        cursor.execute(sql,val)

        mysql.connection.commit()

        return jsonify({'message': 'data updated successfully'})
        cursor.close()
    # else:
    #     return jsonify({"error": "Pengguna tidak ditemukan"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)