from flask import Flask, jsonify
import datetime

# Création de l'application Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def accueil():
    """Endpoint racine qui retourne un message de bienvenue"""
    return jsonify({
        'message': 'Bienvenue sur notre service Web Flask!',
        'status': 'success',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/info', methods=['GET'])
def info():
    """Endpoint supplémentaire avec des informations sur l'API"""
    return jsonify({
        'version': '1.0',
        'description': 'Service Web de démonstration Flask',
        'endpoints': {
            '/': 'Message de bienvenue',
            '/info': 'Informations sur le service'
        }
    })

if __name__ == '__main__':
    # Configuration avec debug=True pour le développement
    app.run(host='0.0.0.0', port=5000, debug=True)