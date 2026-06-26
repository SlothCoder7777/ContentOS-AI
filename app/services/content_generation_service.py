from app.models.content_project import ContentProject
from app.schemas.content_project import ContentProjectGenerateRequest


class ContentGenerationService:
    def generate(
        self,
        project: ContentProject,
        request_data: ContentProjectGenerateRequest,
    ) -> dict:
        platform = project.platform or "General"
        tone = request_data.tone or "engaging"
        brief = request_data.prompt_override or project.brief or project.title

        variations = []

        for index in range(1, request_data.output_count + 1):
            variations.append(
                {
                    "variation": index,
                    "headline": f"{project.title} - Idea {index}",
                    "caption": (
                        f"Create a {tone} {project.content_type} for {platform}. "
                        f"Brief: {brief}"
                    ),
                    "call_to_action": "Try it today",
                }
            )

        return {
            "content_type": project.content_type,
            "platform": platform,
            "tone": tone,
            "brief": brief,
            "variations": variations,
        }
