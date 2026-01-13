
import httpx
import asyncio
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()
API_URL = "http://localhost:8000/api/v1/reports/generate_insight"

async def generate_report():
    console.print(Panel.fit("[bold blue]AuraMax Autonomous Consultant[/bold blue]\n[dim]Synthesizing Bio-OS Report...[/dim]"))

    # Patient Profile: "Critical Carl" returning for a checkup
    payload = {
        "user_name": "Carl Critical",
        "age": 52,
        "medications": ["Warfarin", "Simvastatin"],
        "genotypes": {
            "CYP2C9": "*3/*3", # Slow metabolizer for Warfarin
            "CYP2C19": "*2/*2" # Poor metabolizer
        },
        "recent_rri": [600, 610, 590, 605, 595, 600, 600, 610, 590, 605] # High Stress (Low HRV)
    }

    try:
        async with httpx.AsyncClient() as client:
            console.print(f"[dim]Sending payload for {payload['user_name']}... (Drugs: {len(payload['medications'])})[/dim]")
            response = await client.post(API_URL, json=payload, timeout=20.0)
            
            if response.status_code == 200:
                data = response.json()
                
                # Render Executive Summary
                console.print("\n[bold]Executive Summary:[/bold]")
                console.print(Panel(data["executive_summary"], border_style="cyan"))
                
                # Render Detailed Sections
                for section in data["sections"]:
                    color = "green"
                    if section["status"] == "warning": color = "yellow"
                    if section["status"] == "critical": color = "red"
                    
                    console.print(f"\n[bold {color}]### {section['title']} ###[/bold {color}]")
                    console.print(section["content"])
                
                console.print(f"\n[dim]Report ID: {data['report_id']} | Generated: {data['generated_at']}[/dim]")
                
            else:
                console.print(f"[red]Error {response.status_code}:[/red] {response.text}")

    except Exception as e:
        console.print(f"[red]Failed:[/red] {str(e)}")

if __name__ == "__main__":
    asyncio.run(generate_report())
