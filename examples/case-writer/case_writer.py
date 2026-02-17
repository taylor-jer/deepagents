#!/usr/bin/env python3
import warnings
from typing import Optional
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")
import typer
import asyncio
import os
import sys
from pathlib import Path
from typing import Literal

import yaml

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.text import Text

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

EXAMPLE_DIR = Path(__file__).parent
console = Console()

def load_subagents(config_path: Path) -> list:
    """Load subagent definitions from YAML and wire up tools.

    NOTE: This is a custom utility for this example. Unlike `memory` and `skills`,
    deepagents doesn't natively load subagents from files - they're normally
    defined inline in the create_deep_agent() call. We externalize to YAML here
    to keep configuration separate from code.
    """
    # Map tool names to actual tool objects
    available_tools = {
        "web_search": web_search,
    }

    with open(config_path) as f:
        config = yaml.safe_load(f)

    subagents = []
    for name, spec in config.items():
        subagent = {
            "name": name,
            "description": spec["description"],
            "system_prompt": spec["system_prompt"],
        }
        if "model" in spec:
            subagent["model"] = spec["model"]
        if "tools" in spec:
            subagent["tools"] = [available_tools[t] for t in spec["tools"]]
        subagents.append(subagent)

    return subagents


def create_content_writer(model: str = None): #"openrouter:z-ai/glm-4.7"):
    """Create a content writer agent configured by filesystem files."""
    return create_deep_agent(
        model = model,
        memory=["./AGENTS.md"],           # Loaded by MemoryMiddleware
        skills=["./skills/"],             # Loaded by SkillsMiddleware
        tools=[],
        #subagents=load_subagents(EXAMPLE_DIR / "subagents.yaml"),  # Custom helper
        backend=FilesystemBackend(root_dir=EXAMPLE_DIR),
    )


class AgentDisplay:
    """Manages the display of agent progress."""

    def __init__(self):
        self.printed_count = 0
        self.current_status = ""
        self.spinner = Spinner("dots", text="Thinking...")

    def update_status(self, status: str):
        self.current_status = status
        self.spinner = Spinner("dots", text=status)

    def print_message(self, msg):
        """Print a message with nice formatting."""
        if isinstance(msg, HumanMessage):
            console.print(Panel(str(msg.content), title="You", border_style="blue"))

        elif isinstance(msg, AIMessage):
            content = msg.content
            if isinstance(content, list):
                text_parts = [p.get("text", "") for p in content if isinstance(p, dict) and p.get("type") == "text"]
                content = "\n".join(text_parts)

            if content and content.strip():
                console.print(Panel(Markdown(content), title="Agent", border_style="green"))

            if msg.tool_calls:
                for tc in msg.tool_calls:
                    name = tc.get("name", "unknown")
                    args = tc.get("args", {})

                    if name == "task":
                        desc = args.get("description", "researching...")
                        console.print(f"  [bold magenta]>> Researching:[/] {desc[:60]}...")
                        self.update_status(f"Researching: {desc[:40]}...")
                    elif name in ("generate_cover", "generate_social_image"):
                        console.print(f"  [bold cyan]>> Generating image...[/]")
                        self.update_status("Generating image...")
                    elif name == "write_file":
                        path = args.get("file_path", "file")
                        console.print(f"  [bold yellow]>> Writing:[/] {path}")
                    elif name == "web_search":
                        query = args.get("query", "")
                        console.print(f"  [bold blue]>> Searching:[/] {query[:50]}...")
                        self.update_status(f"Searching: {query[:30]}...")

        elif isinstance(msg, ToolMessage):
            name = getattr(msg, "name", "")
            if name in ("generate_cover", "generate_social_image"):
                if "saved" in msg.content.lower():
                    console.print(f"  [green]✓ Image saved[/]")
                else:
                    console.print(f"  [red]✗ Image failed: {msg.content}[/]")
            elif name == "write_file":
                console.print(f"  [green]✓ File written[/]")
            elif name == "task":
                console.print(f"  [green]✓ Research complete[/]")
            elif name == "web_search":
                if "error" not in msg.content.lower():
                    console.print(f"  [green]✓ Found results[/]")


def main(scenario_file: Optional[str] = None, personae_file: Optional[str] = None, pedagogy_file: Optional[str] = None):
    scenario = open(scenario_file,'r').read()
    personae = open(personae_file,'r').read()
    pedagogy = open(pedagogy_file,'r').read()
    prompt = f"""
       Case context:
          
          Scenario: {scenario}

          Personae: {personae}

          Pedagogical concepts to cover: {pedagogy}
    """
    task = prompt
    asyncio.run(run_task(task))
async def run_task(task):
    print('# Task = ',task)

    console.print()
    console.print("[bold blue]Content Builder Agent[/]")
    console.print(f"[dim]Task: {task}[/]")
    console.print()

    agent = create_content_writer()
    display = AgentDisplay()

    console.print()

    # Use Live display for spinner during waiting periods
    with Live(display.spinner, console=console, refresh_per_second=10, transient=True) as live:
        async for chunk in agent.astream(
            {"messages": [("user", task)]},
            config={"configurable": {"thread_id": "content-writer-demo"}},
            stream_mode="values",
        ):
            if "messages" in chunk:
                messages = chunk["messages"]
                if len(messages) > display.printed_count:
                    # Temporarily stop spinner to print
                    live.stop()
                    for msg in messages[display.printed_count:]:
                        display.print_message(msg)
                    display.printed_count = len(messages)
                    # Resume spinner
                    live.start()
                    live.update(display.spinner)

    console.print()
    console.print("[bold green]✓ Done![/]")


if __name__ == "__main__":
    try:
        typer.run(main)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/]")
