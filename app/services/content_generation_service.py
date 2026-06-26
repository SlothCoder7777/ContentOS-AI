from typing import Any

from app.models.content_project import ContentProject
from app.schemas.content_project import ContentProjectGenerateRequest


class ContentGenerationService:
    def generate(
        self,
        project: ContentProject,
        request_data: ContentProjectGenerateRequest,
    ) -> dict[str, Any]:
        platform = project.platform or "General"
        tone = request_data.tone or self._get_brand_voice(project) or "engaging"
        brief = request_data.prompt_override or project.brief or project.title
        brand_context = self._build_brand_context(project)

        variations = []

        for index in range(1, request_data.output_count + 1):
            variations.append(
                {
                    "variation": index,
                    "headline": self._build_headline(
                        project=project,
                        index=index,
                    ),
                    "caption": self._build_caption(
                        project=project,
                        platform=platform,
                        tone=tone,
                        brief=brief,
                        brand_context=brand_context,
                    ),
                    "call_to_action": self._build_call_to_action(project),
                }
            )

        return {
            "content_type": project.content_type,
            "platform": platform,
            "tone": tone,
            "brief": brief,
            "brand_context": brand_context,
            "variations": variations,
        }

    def _build_brand_context(self, project: ContentProject) -> dict[str, Any] | None:
        brand = getattr(project, "brand", None)

        if brand is None:
            return None

        return {
            "name": getattr(brand, "name", None),
            "description": getattr(brand, "description", None),
            "industry": getattr(brand, "industry", None),
            "target_audience": getattr(brand, "target_audience", None),
            "brand_voice": getattr(brand, "brand_voice", None),
            "brand_values": getattr(brand, "brand_values", None),
            "visual_guidelines": getattr(brand, "visual_guidelines", None),
        }

    def _get_brand_voice(self, project: ContentProject) -> str | None:
        brand = getattr(project, "brand", None)

        if brand is None:
            return None

        return getattr(brand, "brand_voice", None)

    def _build_headline(
        self,
        project: ContentProject,
        index: int,
    ) -> str:
        brand = getattr(project, "brand", None)
        brand_name = getattr(brand, "name", None)

        if brand_name:
            return f"{brand_name}: {project.title} - Idea {index}"

        return f"{project.title} - Idea {index}"

    def _build_caption(
        self,
        project: ContentProject,
        platform: str,
        tone: str,
        brief: str,
        brand_context: dict[str, Any] | None,
    ) -> str:
        caption = (
            f"Create a {tone} {project.content_type} for {platform}. Brief: {brief}"
        )

        if not brand_context:
            return caption

        brand_name = brand_context.get("name")
        target_audience = brand_context.get("target_audience")
        brand_voice = brand_context.get("brand_voice")

        brand_lines = []

        if brand_name:
            brand_lines.append(f"Brand: {brand_name}")

        if target_audience:
            brand_lines.append(f"Target audience: {target_audience}")

        if brand_voice:
            brand_lines.append(f"Brand voice: {brand_voice}")

        if brand_lines:
            caption = f"{caption} " + " | ".join(brand_lines)

        return caption

    def _build_call_to_action(self, project: ContentProject) -> str:
        content_type = project.content_type.lower()

        if "whatsapp" in content_type:
            return "Message us now"

        if "instagram" in content_type or "reel" in content_type:
            return "Follow for more"

        if "blog" in content_type:
            return "Read more"

        return "Try it today"
