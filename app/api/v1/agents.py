from fastapi import APIRouter, status

from app.schemas.agent_workflow import (
    ContentWorkflowRunRequest,
    ContentWorkflowRunResponse,
)
from app.services.agent_workflow_service import AgentWorkflowService

router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


@router.post(
    "/content-workflow/run",
    response_model=ContentWorkflowRunResponse,
    status_code=status.HTTP_200_OK,
)
def run_content_workflow(
    request_data: ContentWorkflowRunRequest,
) -> ContentWorkflowRunResponse:
    return AgentWorkflowService().run_content_workflow(request_data)
