from flask import Flask, jsonify, render_template,session,request
from dotenv import load_dotenv
from db import get_connection,execute_query
import click
import os
import time

load_dotenv()

def crear_app():
    app = Flask(__name__)
    app.config.from_mapping( 
        SECRET_KEY=os.environ.get('SECRET_KEY'),        
    )

    needsUpdate = True

    @app.route('/',methods=('POST','GET'))
    def index():
        return render_template('form.html')

    @app.route('/checkExecutionStatus')
    def checkExecutionStatus():
        executionStatus = get_execution_status()  # Retrieve status from storage
        return jsonify({
            'createDBExecuted': executionStatus['createDBExecuted'],
            'insertIRExecuted': executionStatus['insertIRExecuted']
        })

    @app.route('/createDB', methods=['GET'])
    def createDB():
        query = 'CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY,folio INT,client VARCHAR(255),d DATE,flet boolean,isr boolean,p1prod VARCHAR(255),p1mad VARCHAR(255),p1med VARCHAR(255),p1u VARCHAR(255),p1c VARCHAR(255),p1t VARCHAR(255),p2prod VARCHAR(255),p2mad VARCHAR(255),p2med VARCHAR(255),p2u VARCHAR(255),p2c VARCHAR(255),p2t VARCHAR(255),p3prod VARCHAR(255),p3mad VARCHAR(255),p3med VARCHAR(255),p3u VARCHAR(255),p3c VARCHAR(255),p3t VARCHAR(255),p4prod VARCHAR(255),p4mad VARCHAR(255),p4med VARCHAR(255),p4u VARCHAR(255),p4c VARCHAR(255),p4t VARCHAR(255),p5prod VARCHAR(255),p5mad VARCHAR(255),p5med VARCHAR(255),p5u VARCHAR(255),p5c VARCHAR(255),p5t VARCHAR(255),p6prod VARCHAR(255),p6mad VARCHAR(255),p6med VARCHAR(255),p6u VARCHAR(255),p6c VARCHAR(255),p6t VARCHAR(255),unotas TEXT);'
        results = execute_query(get_connection(), query)

        # Update execution status
        update_execution_status(createDBExecuted=True)

        return jsonify(results)

    @app.route('/insertIR', methods=['GET'])
    def insertIR():
        query = """INSERT INTO users (folio, client, d, flet, isr, p1prod, p1mad, p1med, p1u, p1c, p1t, p2prod, p2mad, p2med, p2u, p2c, p2t, p3prod, p3mad, p3med, p3u, p3c, p3t, p4prod, p4mad, p4med, p4u, p4c, p4t, p5prod, p5mad, p5med, p5u, p5c, p5t, p6prod, p6mad, p6med, p6u, p6c, p6t, unotas)
        VALUES (0, '', NULL, FALSE, FALSE, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);"""
        results = execute_query(get_connection(), query)

        # Update execution status
        update_execution_status(insertIRExecuted=True)

        return jsonify(results)

    @app.route('/getdata', methods=['GET'])
    def getdata():
        query = 'SELECT * FROM users'
        results = execute_query(get_connection(), query)
        return jsonify(results)

    @app.route('/getfolio/<folio>', methods=['GET'])
    def getfolio(folio):
        query = f"SELECT * FROM users WHERE folio = {folio}"
        results = execute_query(get_connection(), query)
        return jsonify(results)


    @app.route('/db', methods=['POST'])
    def db():
        folio = request.form['folio']
        client = request.form['client']
        d = request.form['d']
        iva = request.form['iva'] == 'true'
        flet = request.form['flet'] == 'true'
        if flet:
            fshell = request.form['fshell']
        isr = request.form['isr'] == 'true'
        p1prod = request.form['p1prod']
        p1mad = request.form['p1mad']
        p1med = request.form['p1med']
        p1u = request.form['p1u']
        p1c = request.form['p1c']
        p1t = request.form['p1t']
        p2prod = request.form['p2prod']
        p2mad = request.form['p2mad']
        p2med = request.form['p2med']
        p2u = request.form['p2u']
        p2c = request.form['p2c']
        p2t = request.form['p2t']
        p3prod = request.form['p3prod']
        p3mad = request.form['p3mad']
        p3med = request.form['p3med']
        p3u = request.form['p3u']
        p3c = request.form['p3c']
        p3t = request.form['p3t']
        p4prod = request.form['p4prod']
        p4mad = request.form['p4mad']
        p4med = request.form['p4med']
        p4u = request.form['p4u']
        p4c = request.form['p4c']
        p4t = request.form['p4t']
        p5prod = request.form['p5prod']
        p5mad = request.form['p5mad']
        p5med = request.form['p5med']
        p5u = request.form['p5u']
        p5c = request.form['p5c']
        p5t = request.form['p5t']
        p6prod = request.form['p6prod']
        p6mad = request.form['p6mad']
        p6med = request.form['p6med']
        p6u = request.form['p6u']
        p6c = request.form['p6c']
        p6t = request.form['p6t']
        unotas = request.form['unotas']
        # First, check if a record with this folio already exists
        check_query = 'SELECT * FROM users WHERE folio = %s'
        check_results = execute_query(get_connection(), check_query, (folio,))
        if check_results:
        # If a record exists, update it
            if flet:
                query = '''UPDATE users SET client=%s, d=%s, iva=%s, flet=%s, fshell=%s, isr=%s, p1prod=%s, p1mad=%s, p1med=%s, p1u=%s, p1c=%s, p1t=%s, 
                p2prod=%s, p2mad=%s, p2med=%s, p2u=%s, p2c=%s, p2t=%s, p3prod=%s, p3mad=%s, p3med=%s, p3u=%s, p3c=%s, p3t=%s, p4prod=%s, p4mad=%s, p4med=%s, 
                p4u=%s, p4c=%s, p4t=%s, p5prod=%s, p5mad=%s, p5med=%s, p5u=%s, p5c=%s, p5t=%s, p6prod=%s, p6mad=%s, p6med=%s, p6u=%s, p6c=%s, p6t=%s, unotas=%s
                WHERE folio=%s'''
                params = (client, d, iva, flet, fshell, isr, p1prod, p1mad, p1med, p1u, p1c, p1t, p2prod, p2mad, p2med, p2u, p2c, p2t, p3prod, p3mad, p3med, p3u, p3c, p3t, p4prod, p4mad, p4med, p4u, p4c, p4t, p5prod, p5mad, p5med, p5u, p5c, p5t, p6prod, p6mad, p6med, p6u, p6c, p6t, unotas, folio)
                needsUpdate = False
                operation = 'update'
            else:
                query = '''UPDATE users SET client=%s, d=%s, iva=%s, flet=%s,isr=%s, p1prod=%s, p1mad=%s, p1med=%s, p1u=%s, p1c=%s, p1t=%s, 
                p2prod=%s, p2mad=%s, p2med=%s, p2u=%s, p2c=%s, p2t=%s, p3prod=%s, p3mad=%s, p3med=%s, p3u=%s, p3c=%s, p3t=%s, p4prod=%s, p4mad=%s, p4med=%s, 
                p4u=%s, p4c=%s, p4t=%s, p5prod=%s, p5mad=%s, p5med=%s, p5u=%s, p5c=%s, p5t=%s, p6prod=%s, p6mad=%s, p6med=%s, p6u=%s, p6c=%s, p6t=%s, unotas=%s
                WHERE folio=%s'''
                params = (client, d, iva, flet, isr, p1prod, p1mad, p1med, p1u, p1c, p1t, p2prod, p2mad, p2med, p2u, p2c, p2t, p3prod, p3mad, p3med, p3u, p3c, p3t, p4prod, p4mad, p4med, p4u, p4c, p4t, p5prod, p5mad, p5med, p5u, p5c, p5t, p6prod, p6mad, p6med, p6u, p6c, p6t, unotas, folio)
                needsUpdate = False
                operation = 'update'
        else:
            # If no record exists, insert a new one
            if flet:
                query = 'INSERT INTO users (folio, client, d, iva, flet, fshell, isr, p1prod, p1mad, p1med, p1u, p1c, p1t, p2prod, p2mad, p2med, p2u, p2c, p2t, p3prod, p3mad, p3med, p3u, p3c, p3t, p4prod, p4mad, p4med, p4u, p4c, p4t, p5prod, p5mad, p5med, p5u, p5c, p5t, p6prod, p6mad, p6med, p6u, p6c, p6t, unotas) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                params = (folio, client, d, iva, flet, fshell, isr, p1prod, p1mad, p1med, p1u, p1c, p1t, p2prod, p2mad, p2med, p2u, p2c, p2t, p3prod, p3mad, p3med, p3u, p3c, p3t, p4prod, p4mad, p4med, p4u, p4c, p4t, p5prod, p5mad, p5med, p5u, p5c, p5t, p6prod, p6mad, p6med, p6u, p6c, p6t, unotas)
                needsUpdate = True
                operation = 'insert'
            else:
                query = 'INSERT INTO users (folio, client, d, iva, flet, isr, p1prod, p1mad, p1med, p1u, p1c, p1t, p2prod, p2mad, p2med, p2u, p2c, p2t, p3prod, p3mad, p3med, p3u, p3c, p3t, p4prod, p4mad, p4med, p4u, p4c, p4t, p5prod, p5mad, p5med, p5u, p5c, p5t, p6prod, p6mad, p6med, p6u, p6c, p6t, unotas) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                params = (folio, client, d, iva, flet, isr, p1prod, p1mad, p1med, p1u, p1c, p1t, p2prod, p2mad, p2med, p2u, p2c, p2t, p3prod, p3mad, p3med, p3u, p3c, p3t, p4prod, p4mad, p4med, p4u, p4c, p4t, p5prod, p5mad, p5med, p5u, p5c, p5t, p6prod, p6mad, p6med, p6u, p6c, p6t, unotas)
                needsUpdate = True
                operation = 'insert'
        results = execute_query(get_connection(), query, params)
            
        return jsonify({'operation':operation, 'results':check_results, 'flet':flet})

    @app.route('/update', methods=['PUT'])
    def update():
        if needsUpdate == True:
            data = request.get_json()
            folio = data['folio']

            # Open the 'METAcounter' file in write mode
            with open('static/METAcounter.txt', 'w') as file:
                # Write the new folio number to the file
                file.write(str(folio))

            return jsonify(success=True), 200
        else:
            return jsonify(success=True), 200

    return app

app = crear_app()
