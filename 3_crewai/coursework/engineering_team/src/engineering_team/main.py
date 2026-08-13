#!/usr/bin/env python
import sys
import warnings
from datetime import datetime


from engineering_team.crew import EngineeringTeam
from .tools.sandbox_tools import reset_sandbox

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

requirements = """
Un semplice sistema di gestione dei conti per una piattaforma di simulazione del trading.

Il sistema deve consentire agli utenti di creare un account, depositare fondi e prelevare denaro.

Il sistema deve consentire agli utenti di registrare l'acquisto o la vendita di azioni,
specificando la quantità.

Il sistema deve calcolare il valore totale del portafoglio dell'utente e il profitto o la perdita
rispetto al deposito iniziale.

Il sistema deve essere in grado di fornire la situazione delle partecipazioni dell'utente
in qualsiasi momento.

Il sistema deve essere in grado di fornire il profitto o la perdita dell'utente
in qualsiasi momento.

Il sistema deve essere in grado di elencare le transazioni effettuate dall'utente nel corso del tempo.

Il sistema deve impedire all'utente:
- di prelevare fondi in modo tale da portare il saldo a un valore negativo;
- di acquistare un numero di azioni superiore a quello che può permettersi;
- di vendere azioni che non possiede.

Il sistema ha accesso a una funzione get_share_price(symbol) che restituisce il prezzo corrente
di un'azione e include un'implementazione di test che restituisce prezzi fissi per AAPL, TSLA e GOOGL.
"""


def run():
    """
    Run the crew.
    """
    inputs = {
        'requirements': requirements,
    }

    try:
        reset_sandbox()
        EngineeringTeam().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        EngineeringTeam().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        EngineeringTeam().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        EngineeringTeam().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = EngineeringTeam().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
