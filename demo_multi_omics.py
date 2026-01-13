
import httpx
import asyncio
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

API_URL = "http://localhost:8000/api/v1/omics/predict_risk"

async def check_risk(profile_name: str, genes: float, stress: float, age: int):
    """
    Query the Multi-omics Cortex for a risk assessment.
    """
    payload = {
        "genetic_risk_score": genes,
        "current_stress_level": stress,
        "age": age,
        "lifestyle_factor": 0.5 
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, json=payload, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"HTTP {response.status_code}")
    except Exception as e:
        # Fallback to local simulation (Cortex Edge Mode)
        # Mimics MultiOmicsService._predict_heuristic
        score = (genes * 40) + (stress * 0.4) + (age * 0.2)
        prob = min(max(score / 100, 0), 1)
        
        level = "Low"
        if prob > 0.7: level = "High"
        elif prob > 0.3: level = "Moderate"
        
        return {
            "mode": "heuristic (edge-fallback)",
            "risk_probability": prob,
            "risk_level": level,
            "contributing_factors": {
                "genetic_load": genes * 40,
                "stress_load": stress * 0.4
            }
        }

async def run_demo():
    console.print(Panel.fit("[bold magenta]Multi-omics Cortex Demo (Bio-OS)[/bold magenta]\n[dim]Fusing Genotype + Phenotype Data...[/dim]"))

    # Define Profiles
    profiles = [
        {
            "name": "Lucky Larry",
            "desc": "Good Genes (0.2), Low Stress (20)",
            "genes": 0.2, "stress": 20.0, "age": 30
        },
        {
            "name": "Stressed Steve",
            "desc": "Avg Genes (0.5), High Stress (90)",
            "genes": 0.5, "stress": 90.0, "age": 35
        },
        {
            "name": "Risk-prone Ray",
            "desc": "Bad Genes (0.9), Moderate Stress (50)",
            "genes": 0.9, "stress": 50.0, "age": 55
        },
        {
            "name": "Critical Carl",
            "desc": "Bad Genes (0.8) + High Stress (95)",
            "genes": 0.8, "stress": 95.0, "age": 50
        }
    ]

    table = Table(title="Composite Health Risk Prediction")
    table.add_column("Subject", style="cyan")
    table.add_column("Profile Input", style="dim")
    table.add_column("Risk Prob", justify="right")
    table.add_column("Risk Level", style="bold")
    table.add_column("Primary Driver", style="italic")

    for p in profiles:
        result = await check_risk(p["name"], p["genes"], p["stress"], p["age"])
        
        if "error" in result:
            table.add_row(p["name"], "Error", "-", f"[red]{result['error']}[/red]", "-")
            continue
            
        prob = f"{result['risk_probability']:.1%}"
        level = result['risk_level']
        
        # Colorize level
        if level == "High": level = f"[red]{level}[/red]"
        elif level == "Moderate": level = f"[yellow]{level}[/yellow]"
        else: level = f"[green]{level}[/green]"
        
        # Determine driver
        factors = result.get("contributing_factors", {})
        gene_load = factors.get("genetic_load", 0)
        stress_load = factors.get("stress_load", 0)
        
        driver = "Genetics" if gene_load > stress_load else "Lifestyle/Stress"
        
        table.add_row(p["name"], p["desc"], prob, level, driver)

    console.print(table)
    console.print("\n[bold green]✓ Cortex Analysis Complete[/bold green]")

if __name__ == "__main__":
    asyncio.run(run_demo())
