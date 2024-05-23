from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Pet:
    def __init__(self, nome, idade, peso):
        self.nome = nome
        self.idade = idade
        self.peso = peso

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):

        if isinstance(nome, str) and nome.strip():
            self._nome = nome
        else:
            raise ValueError("O nome não deve ser vazio e deve ser uma string.")

    @property
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, idade):

        if isinstance(idade, int) and idade >= 0:
            self._idade = idade
        else:
            raise ValueError("Idade deve ser um número inteiro e maior ou igual a 0.")

    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, peso):

        if isinstance(peso, (int, float)) and peso > 0:
            self._peso = float(peso)
        else:
            raise ValueError("O peso deve ser um número flutuante e maior que 0")


    def to_dic(self):
        return {
            "nome": self.nome,
            "idade": self.idade,
            "peso": self.peso
        }

pets = []

@app.route("/")
def home():
    return "API de Pets está funcionando!"

@app.route("/pets", methods=["POST"])
def create_pet():

    data = request.json
    try:
        pet = Pet(data["nome"], data["idade"], data["peso"])
        pets.append(pet)
        return jsonify(pet.to_dic()), 201

    except ValueError as e:
        return jsonify({"error:": str(e)}), 400

@app.route("/pets", methods=["GET"])
def get_pets():
    return jsonify([pet.to_dic() for pet in pets])

@app.route("/pets/<string:nome>", methods=["GET"])
def get_pet(nome):
    for pet in pets:
        if pet.nome == nome:
            return jsonify(pet.to_dic())
    return jsonify({"error": "Pet not found"}), 404

@app.route("/pets/<string:nome>", methods=["DELETE"])
def delete_pet(nome):
    global pets
    pets = [pet for pet in pets if pet.nome != nome]
    return '', 204

if __name__ == "__main__":

    app.run(debug=True)





