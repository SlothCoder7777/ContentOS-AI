from typing import Any

from sqlalchemy.orm import Session

from app.repositories.generated_content_repository import (
    generated_content_repository,
)
from app.schemas.ai_output import StructuredAIOutput
from app.schemas.generated_content import GeneratedContentCreate
from app.services.ai_output_parser_service import ai_output_parser_service


class GeneratedContentService:
    def save_structured_output(
        self,
        db: Session,
        output: StructuredAIOutput,
        project_id: str | None = None,
        title: str | None = None,
        content_metadata: dict[str, Any] | None = None,
    ):
        data = GeneratedContentCreate(
            project_id=project_id,
            title=title,
            generation_engine=output.generation_engine,
            model=output.model,
            content_type=output.content_type,
            platform=output.platform,
            tone=output.tone,
            brief=output.brief,
            brand_context=output.brand_context,
            variations=[variation.model_dump() for variation in output.variations],
            raw_output=output.raw_output,
            content_metadata=content_metadata,
        )

        return generated_content_repository.create(
            db=db,
            data=data,
        )

    def save_generation_result(
        self,
        db: Session,
        generation_result: dict[str, Any],
        project_id: str | None = None,
        title: str | None = None,
        content_metadata: dict[str, Any] | None = None,
    ):
        structured_output = ai_output_parser_service.parse_content_generation_result(
            generation_result
        )

        return self.save_structured_output(
            db=db,
            output=structured_output,
            project_id=project_id,
            title=title,
            content_metadata=content_metadata,
        )

    def get_by_id(
        self,
        db: Session,
        generated_content_id: str,
    ):
        return generated_content_repository.get_by_id(
            db=db,
            generated_content_id=generated_content_id,
        )

    def list_recent(
        self,
        db: Session,
        limit: int = 20,
        offset: int = 0,
    ):
        return generated_content_repository.list_recent(
            db=db,
            limit=limit,
            offset=offset,
        )

    def count(
        self,
        db: Session,
    ) -> int:
        return generated_content_repository.count(db=db)


generated_content_service = GeneratedContentService()
