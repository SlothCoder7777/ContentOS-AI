from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.schemas.agent_workflow import (
    ContentWorkflowRunRequest,
    ContentWorkflowRunResponse,
)


class ContentWorkflowState(TypedDict):
    brand_name: str
    topic: str
    platform: str
    content_type: str
    tone: str
    plan: str
    draft: str
    review: str
    workflow_status: str


class AgentWorkflowService:
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
            "plan": "",
            "draft": "",
            "review": "",
            "workflow_status": "started",
        }

        result = graph.invoke(initial_state)

        return ContentWorkflowRunResponse(
            brand_name=result["brand_name"],
            topic=result["topic"],
            platform=result["platform"],
            content_type=result["content_type"],
            tone=result["tone"],
            plan=result["plan"],
            draft=result["draft"],
            review=result["review"],
            workflow_status=result["workflow_status"],
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
        return {
            "draft": (
                f"{state['brand_name']} presents: {state['topic']}! "
                f"Here is a {state['tone']} draft for {state['platform']}."
            ),
            "workflow_status": "drafted",
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
