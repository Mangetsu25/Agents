# Agents

This repository now integrates the [Google Agent Development Kit](https://github.com/google/adk-docs) to orchestrate a diet planning workflow. It showcases multiple agents coordinated by an ADK `SequentialAgent` as well as a simple retrieval‑augmented generation (RAG) component backed by FAISS and Vertex AI.

## Agents

- **RootAgent** – ADK sequential agent coordinating all other agents
- **CreatorADKAgent** – wraps `DietCreatorAgent` to build a plan
- **ValidatorADKAgent** – validates a generated plan
- **SupportADKAgent** – answers questions with guardrails
- **RagAgent** – retrieves context from a FAISS index and responds using Vertex AI
- **Guardrails** – checks queries for PII/PHI and unsafe content

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Example asynchronous use:

```python
import asyncio
from google.adk.agents.invocation_context import InvocationContext
from agents.root_agent import RootAgent

async def main():
    root = RootAgent(documents=["oatmeal is healthy", "salmon contains omega 3"])
    ctx = InvocationContext(agent=root, session_service=None)
    ctx.session_state['profile'] = {"age": 30, "goal": "weight loss"}
    async for _ in root.run_async(ctx):
        pass
    plan = ctx.session_state.get('plan')
    root.generate_pdf(plan, "plan.pdf")

asyncio.run(main())
```

This will generate a plan, validate it, answer a query if provided and create a `plan.pdf` file.
