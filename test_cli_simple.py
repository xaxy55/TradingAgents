#!/usr/bin/env python
import sys
print("1. Starting imports")
sys.stdout.flush()

print("2. Importing typing")
from typing import Optional
sys.stdout.flush()

print("3. Importing typer")
import typer
sys.stdout.flush()

print("4. Importing tradingagents")
from tradingagents.graph.trading_graph import TradingAgentsGraph
sys.stdout.flush()

print("5. Creating app")
app = typer.Typer()
sys.stdout.flush()

print("6. Defining command")
@app.command()
def analyze(ticker: Optional[str] = typer.Option(None)):
    print(f"Analyzing {ticker}")

print("7. Done with setup")
sys.stdout.flush()

if __name__ == "__main__":
    print("8. Running app")
    sys.stdout.flush()
    app()
