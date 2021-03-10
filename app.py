from flask import Flask, Response
from slackeventsapi import SlackEventAdapter
import os
from threading import Thread
from slack_sdk import WebClient
from datetime import datetime
import psycopg2 as db
from random import randint

class Config:

    def __init__(self):
        self.config = {
            "postgres": {
                "user": "postgres",
                "password": "root",
                "host": "127.0.0.1",
                "port": "5432",
                "database": "Peter"
            }
        }

class Connection(Config):
    def __init__(self):
        Config.__init__(self)

        try:
            self.conn = db.connect(**self.config["postgres"])
            self.cur = self.conn.cursor()

        except Exception as e:
            print("Connection Error", e)
            exit(1)

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.commit()
        self.connection()

    @property
    def connection(self):
        return self.conn
    
    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

class Peter(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, rater, ratee, technical_score, social_score, month, year):

        try:
            sql = f"INSERT INTO ratings VALUES ('{rater}', '{ratee}', {technical_score}, {social_score}, '{month}', '{year}');"
            print(sql)
            self.execute(sql)
            self.commit()

        except Exception as e:

            print("Insertion error", e)
       

# This `app` represents your existing Flask app
app = Flask(__name__)

greetings = ["hi", "hello", "hello there", "hey", "olá", "oi"]

avaliar = ["1", "avaliar alguém", "avaliar alguem"]

people = ["john", "bia", "thais"]

infos = {
    "Avaliador": "",
    "Avaliado": "",
    "Pnota": None,
    "Snota": None,
    "Dia": "05/03/2021"
}

OnOff = {
    "gradeOnOff": "off"
}

OnAvaliar = {
    "avaliar": "off"
}

endGrades = {
    "end": False
}

grades = ["1", "2", "3", "4", "5"]

nota = []

ValidateGrades = "nota 1" or "nota 2" or "nota 3" or "nota 4" or "nota 5"

SLACK_SIGNING_SECRET = ''
slack_token = ''
VERIFICATION_TOKEN = ''

#instantiating slack client
slack_client = WebClient(token=slack_token)

# An example of one of your Flask app's routes
@app.route("/")
def event_hook(request):
    json_dict = json.loads(request.body.decode("utf-8"))
    if json_dict["token"] != VERIFICATION_TOKEN:
        return {"status": 403}

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict
    return {"status": 500}
    return


slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app
)  


@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    def send_reply(value):
        event_data = value
        message = event_data["event"]
        if message.get("subtype") is None:
            command = message.get("text")
            channel_id = message["channel"]
            if any(item in command.lower() for item in greetings):

                inicio = (
                    """
                    Olá <@%s> como posso ajuda-lo hoje ? :alien:\n 1: Avaliar alguém ?\n 2: ...\n 3: ...\n 4: ...
                    """
                    % message["user"]
                )
                slack_client.chat_postMessage(channel=channel_id, text=inicio)

                infos["Avaliador"] = "%s" % message["user"]

            elif any(item in command.lower() for item in grades):

                print("Salve", OnOff["gradeOnOff"])

                if OnOff["gradeOnOff"] == "off" and OnAvaliar["avaliar"] == "on":
                    avaliado = (
                        """
                        Show ! Qual nota vc quer dar para ele(a) ? :alien:\n\n ===================================================\n\n Primeira Pergunta ! :tada:\n\n 1: Qual nota você quer dar para o ele(a) no quesito "capacidade técnica para desenvolver as atividades" ?\n\n Notas disponiveis\n 1: Péssimo :white_frowning_face:\n 2: Ruim :slightly_frowning_face:\n 3: Regular :expressionless:\n 4: Bom :slightly_smiling_face:\n 5: Excelente :smiley:\n\n Exemplo de nota: 5\n\n Por favor siga o exemplo para não haver problemas ! Obrigado :spock-hand:
                        """
                    )
                    slack_client.chat_postMessage(channel=channel_id, text=avaliado)

                    Pavaliada = command

                    print(Pavaliada)

                    Pavaliada = Pavaliada.split("> ")

                    print(Pavaliada)

                    results = slack_client.users_list()
                    users = len(results["members"])

                    print("=" * 10)

                    # print(results)

                    for i in range(0, users):

                        print("3" * 10)

                        if (results["members"][i]["profile"]["real_name"] == Pavaliada[1]):

                            print("A" * 10)

                            avaliado = results["members"][i]["id"]

                            infos["Avaliado"] = avaliado

                            OnOff["gradeOnOff"] = "on"

                            OnAvaliar["avaliar"] = "off"

                            print(OnOff["gradeOnOff"])

                            print(endGrades["end"])

                            return OnOff["gradeOnOff"]

                elif any(item in command.lower() for item in avaliar)  and OnOff["gradeOnOff"] == "off":
                    task = (
                        """
                        Quem você quer avaliar ? :alien:
                        """
                    )
                    slack_client.chat_postMessage(channel=channel_id, text=task)

                    print(OnOff["gradeOnOff"])

                    OnAvaliar["avaliar"] = "on"

                    return OnAvaliar["avaliar"]

                elif any(item in command.lower() for item in grades) and OnOff["gradeOnOff"] == "on" and endGrades["end"] == False:
                    avaliado = (
                        """ 
                        Segunda Pergunta ! :tada:\n\n 2: Qual nota você quer dar para o ele(a) no quesito "cooperação com a equipe / nível de responsabilidade com o projeto" ?\n\n Notas disponiveis\n 1: Péssimo :white_frowning_face:\n 2: Ruim :slightly_frowning_face:\n 3: Regular :expressionless:\n 4: Bom :slightly_smiling_face:\n 5: Excelente :smiley:\n\n Exemplo de nota: 5\n\n Por favor siga o exemplo para não haver problemas ! Obrigado :spock-hand:
                        """ 
                    )
                    slack_client.chat_postMessage(channel=channel_id, text=avaliado)

                    pnota = command.lower()

                    pnota = pnota.split("> ")

                    infos["Pnota"] = int(pnota[1])

                    endGrades["end"] = True

                    print(endGrades["end"])

                    return endGrades["end"]

                elif any(item in command.lower() for item in grades) and OnOff["gradeOnOff"] == "on" and endGrades["end"] == True:

                    print("Safe")

                    snota = command.lower()

                    snota = snota.split("> ")

                    infos["Snota"] = int(snota[1])

                    infos["Dia"] = datetime.now()

                    print(infos)

                    peter = Peter()
                    peter.insert(infos["Avaliador"], infos["Avaliado"], infos["Pnota"], infos["Snota"], "03", "2021")

                    OnOff["gradeOnOff"] = "off"
                    OnAvaliar["avaliar"] = "off"

    thread = Thread(target=send_reply, kwargs={"value": event_data})
    thread.start()
    return Response(status=200)


# Start the server on port 3000
if __name__ == "__main__":
  app.run(port=3000)