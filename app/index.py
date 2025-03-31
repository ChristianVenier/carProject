from flask import Flask, render_template_string, url_for
import matplotlib
matplotlib.use('Agg')  # Usa il backend Agg per salvare il grafico senza GUI
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

# Crea la cartella static se non esiste
if not os.path.exists('static'):
    os.makedirs('static')

# Funzione per generare il grafico
def generate_graph():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, label='Seno')
    plt.title('Grafico di esempio')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.savefig('static/graph.png')  # Salva il grafico nella cartella static
    plt.close()

# Dati per la tabella
table_data = [
    ['Id', 'Macchina', 'Tempo di viaggio', 'Partenza', 'Arrivo'],
    [1, "Ford", 20, 30, 50],
    [2, "Audi", 50, 60, 80]
]

@app.route('/')
def home():
    return "home"

@app.route('/vehicles')
def veicles():
    # Genera il grafico
    generate_graph()

    # Template HTML
    html = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Homepage</title>
    <style>
        table {
            border-collapse: collapse;
            width: 80%;
            margin: 20px auto;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #f2f2f2;
        }
        .graph-container {
            text-align: center;
            margin: 20px;
        }
    </style>
</head>
<body>
    <h1>Benvenuto nella Homepage</h1>

    <h2>Tabella dei Dati</h2>
    <table>
        <tr>
            {% for header in table_data[0] %}
                <th>{{ header }}</th>
            {% endfor %}
        </tr>
        {% for row in table_data[1:] %}
            <tr>
                {% for cell in row %}
                    <td>{{ cell }}</td>
                {% endfor %}
            </tr>
        {% endfor %}
    </table>

    <h2>Grafico</h2>
    <div class="graph-container">
        <img src="{{ url_for('static', filename='graph.png') }}" alt="Grafico di esempio">
    </div>
</body>
</html>"""
    # Passa i dati al template
    return render_template_string(html, table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)