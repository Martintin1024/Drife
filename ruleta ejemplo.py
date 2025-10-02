import time
import random
from rich.console import Console

console = Console()

opciones = ["Nada", "Meditar", "Música", "Comer", "Mona", "Sol", "Baño"]

def animar_ruleta(opciones):
    giros = random.randint(15, 30)  # cantidad de pasos que va a girar
    elegido = None

    for i in range(giros):
        elegido = random.choice(opciones)
        console.print(f"[bold magenta]🎰 {elegido}[/bold magenta]", end="\r")
        time.sleep(0.05 + i*0.02)  # arranca rápido y se va frenando

    console.print(f"\n✅ Resultado final: [green]{elegido}[/green]")

# Probar
animar_ruleta(opciones)
