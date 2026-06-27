from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.schemas.agent_workflow import (
    ContentWorkflowRunRequest,
    ContentWorkflowRunResponse,
)
from app.schemas.llm import LLMGenerateRequest
from app.services.llm_service import LLMService


class ContentWorkflowState(TypedDict):
    brand_name: str
    topic: str
    platform: str
    content_type: str
    tone: str
    use_ai: bool
    plan: str
    draft: str
    review: str
    workflow_status: str
    generation_engine: str


class AgentWorkflowService:
    def __init__(self):
        self.llm_service = LLMService()

    def run_content_workflow(
        self,
        request_data: ContentWorkflowRunRequest,
    ) -> ContentWorkflowRunResponse:
        graph = self._build_graph()

        initial_state: ContentWorkflowState = {
            "brand_name": request_data.brand_name,
            "topic": request_data.topic,
            "platform": request_data.platform,
            "content_type": request_data.content_type,
            "tone": request_data.tone,
            "use_ai": request_data.use_ai,
            "plan": "",
            "draft": "",
            "review": "",
            "workflow_status": "started",
            "generation_engine": "local-agent-workflow-v1",
        }

        result = graph.invoke(initial_state)

        return ContentWorkflowRunResponse(
            brand_name=result["brand_name"],
            topic=result["topic"],
            platform=result["platform"],
            content_type=result["content_type"],
            tone=result["tone"],
            use_ai=result["use_ai"],
            plan=result["plan"],
            draft=result["draft"],
            review=result["review"],
            workflow_status=result["workflow_status"],
            generation_engine=result["generation_engine"],
        )

    def _build_graph(self):
        workflow = StateGraph(ContentWorkflowState)

        workflow.add_node("planner", self._planner_node)
        workflow.add_node("writer", self._writer_node)
        workflow.add_node("reviewer", self._reviewer_node)

        workflow.add_edge(START, "planner")
        workflow.add_edge("planner", "writer")
        workflow.add_edge("writer", "reviewer")
        workflow.add_edge("reviewer", END)

        return workflow.compile()

    def _planner_node(
        self,
        state: ContentWorkflowState,
    ) -> dict:
        return {
            "plan": (
                f"Plan a {state['tone']} {state['content_type']} for "
                f"{state['brand_name']} on {state['platform']} about {state['topic']}."
            ),
            "workflow_status": "planned",
        }

    def _writer_node(
        self,
        state: ContentWorkflowState,
    ) -> dict:
        if state["use_ai"]:
            return self._ai_writer_node(state)

        return self._local_writer_node(state)

    def _ai_writer_node(
        self,
        state: ContentWorkflowState,
    ) -> dict:
        try:
            llm_response = self.llm_service.generate_text(
                LLMGenerateRequest(
                    system_prompt=(
                        "You are ContentOS AI writer agent. "
                        "Write concise, platform-ready marketing content."
                    ),
                    user_prompt=(
                        f"Brand: {state['brand_name']}\n"
                        f"Topic: {state['topic']}\n"
                        f"Platform: {state['platform']}\n"
                        f"Content type: {state['content_type']}\n"
                        f"Tone: {state['tone']}\n"
                        f"Plan: {state['plan']}\n"
                        "Write one polished draft."
                    ),
                    metadata={
                        "agent": "writer",
                        "workflow": "content_workflow",
                    },
                )
            )

            return {
                "draft": llm_response.output_text,
                "workflow_status": "drafted",
                "generation_engine": "openai-agent-writer",
            }

        except RuntimeError:
            return {
                **self._local_writer_node(state),
                "generation_engine": "local-agent-workflow-v1-fallback",
            }

    def _local_writer_node(
        self,
        state: ContentWorkflowState,
    ) -> dict:
        return {
            "draft": (
                f"{state['brand_name']} presents: {state['topic']}! "
                f"Here is a {state['tone']} draft for {state['platform']}."
            ),
            "workflow_status": "drafted",
            "generation_engine": "local-agent-workflow-v1",
        }

    def _reviewer_node(
        self,
        state: ContentWorkflowState,
    ) -> dict:
        return {
            "review": (
                "Draft reviewed successfully. It is clear, brand-focused, "
                "and ready for final AI enhancement."
            ),
            "workflow_status": "reviewed",
        }
