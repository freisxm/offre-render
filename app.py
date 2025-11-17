from flask import Flask, render_template, request, redirect, url_for, session
import os, csv
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecret")
ACCESS_CODE = os.getenv("ACCESS_CODE", "azur2025")

offer_data = {
    "Offre": "1",
    "Actif à vendre": "Droits sociaux",
    "Classement": "5 étoiles",
    "Localisation globale": "Côte d'Azur",
    "Nombre de clés": "43",
    "CA en K€ (2024)":"5600k€",
    "EBITDA en % (2024)": "32.1%",
    "RMC en € (2024)": "254€HT",
    "Prix en k€": "20150k€",
    "Marque": "Affiliation",
    "Date limite de réception des LOI": "31/03/2026",
    "Présentation de l'établissement": "Hôtel Côte d'Azur 5 étoiles",
    "Description": (
        "L'hôtel mis en vente est un établissement emblématique de la région."
        "Il propose à sa clientèle de tourisme un restaurant étoilé, un restaurant de plage et un piano-bar. "
        "Chambres avec vue mer imprenable et plage privative. "
        "Un espace MICE accueille jusqu'à 600 personnes. "
        "L'hôtel est moderne et ne nécessite pas de rénovation lourde."
    )
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form.get('access_code')
        if code == ACCESS_CODE:
            session['authenticated'] = True
            return redirect(url_for('offre'))
        else:
            return render_template('login.html', error='Code incorrect.')
    return render_template('login.html')

@app.route('/offre', methods=['GET', 'POST'])
def offre():
    if not session.get('authenticated'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        contact = request.form.get('contact')
        if contact:
            with open('responses.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([datetime.now().isoformat(), request.remote_addr, contact])
            return render_template('confirmation.html', contact=contact)

    return render_template('offre.html', offer=offer_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
