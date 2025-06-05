from __future__ import annotations
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.base_agent import BaseAgent
from google.adk.events.event import Event
from google.adk.agents.invocation_context import InvocationContext
from google.genai.types import Content, Part

from .diet_creator_agent import DietCreatorAgent
from .diet_support_agent import DietSupportAgent
from .diet_validator_agent import DietValidatorAgent
from .pdf_utils import json_to_pdf
from .guardrails import Guardrails
from .rag_agent import RagAgent

class CreatorADKAgent(BaseAgent):
    def __init__(self, core: DietCreatorAgent | None = None, **kwargs):
        super().__init__(**kwargs)
        self.core = core or DietCreatorAgent()

    async def _run_async_impl(self, ctx: InvocationContext):
        profile = ctx.session_state.get('profile', {})
        plan = self.core.create_diet(profile)
        ctx.session_state['plan'] = plan
        yield Event(invocation_id=ctx.invocation_id, author=self.name,
                    content=Content(role='assistant', parts=[Part(text='diet created')]))

class ValidatorADKAgent(BaseAgent):
    def __init__(self, core: DietValidatorAgent | None = None, **kwargs):
        super().__init__(**kwargs)
        self.core = core or DietValidatorAgent()

    async def _run_async_impl(self, ctx: InvocationContext):
        plan = ctx.session_state.get('plan', {})
        if not self.core.validate_plan(plan):
            ctx.session_state['valid'] = False
            yield Event(invocation_id=ctx.invocation_id, author=self.name,
                        content=Content(role='assistant', parts=[Part(text='validation failed')]))
            ctx.end_invocation = True
            return
        ctx.session_state['valid'] = True
        yield Event(invocation_id=ctx.invocation_id, author=self.name,
                    content=Content(role='assistant', parts=[Part(text='plan validated')]))

class SupportADKAgent(BaseAgent):
    def __init__(self, guardrails: Guardrails | None = None, core: DietSupportAgent | None = None, **kwargs):
        super().__init__(**kwargs)
        self.core = core or DietSupportAgent()
        self.guardrails = guardrails or Guardrails()

    async def _run_async_impl(self, ctx: InvocationContext):
        question = ctx.session_state.get('query', '')
        if not self.guardrails.is_safe(question):
            yield Event(invocation_id=ctx.invocation_id, author=self.name,
                        content=Content(role='assistant', parts=[Part(text='Query blocked by guardrails')]))
            ctx.end_invocation = True
            return
        plan = ctx.session_state.get('plan', {})
        answer = self.core.answer_question(question, plan)
        yield Event(invocation_id=ctx.invocation_id, author=self.name,
                    content=Content(role='assistant', parts=[Part(text=answer)]))

class RootAgent(SequentialAgent):
    """ADK-based root agent coordinating the diet workflow."""

    def __init__(self, documents: list[str] | None = None):
        creator = CreatorADKAgent(name='creator')
        validator = ValidatorADKAgent(name='validator')
        support = SupportADKAgent(name='support')
        rag = RagAgent(name='rag', documents=documents or [])
        super().__init__(name='root', sub_agents=[creator, validator, support, rag])
        self.guardrails = Guardrails()

    def generate_pdf(self, plan: dict, path: str) -> None:
        json_to_pdf(plan, path)

__all__ = ["RootAgent"]
