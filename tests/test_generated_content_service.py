from typing import cast

from sqlalchemy import Table, create_engine, engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base
from app.models.generated_content import GeneratedContent
from app.schemas.ai_output import AIContentVariation, StructuredAIOutput
from app.services.generated_content_service import GeneratedContentService


def build_test_db_session() -> Session:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    generated_content_table = cast(Table, GeneratedContent.__table__)

    Base.metadata.create_all(
        bind=engine,
        tables=[generated_content_table],
    )

    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    return testing_session_local()


def test_save_structured_output_to_database():
    db = build_test_db_session()

    output = StructuredAIOutput(
        generation_engine="openai",
        model="gpt-5.5",
        content_type="instagram_post",
        platform="Instagram",
        tone="friendly",
        brief="Promote mixed berries milkshake offer",
        brand_context={
            "name": "Kulfi Lounge",
        },
        variations=[
            AIContentVariation(
                variation=1,
                headline="Berry Refreshment is Here",
                caption="Enjoy Mixed Berries Milkshake at Rs.90 only.",
                call_to_action="Grab it soon",
                hashtags=["#KulfiLounge"],
            )
        ],
        raw_output="Raw AI output",
    )

    saved = GeneratedContentService().save_structured_output(
        db=db,
        output=output,
        project_id="project-1",
        title="Monsoon Campaign",
        content_metadata={
            "source": "unit-test",
        },
    )

    assert saved.id is not None
    assert saved.project_id == "project-1"
    assert saved.title == "Monsoon Campaign"
    assert saved.generation_engine == "openai"
    assert saved.model == "gpt-5.5"
    assert saved.content_type == "instagram_post"
    assert saved.platform == "Instagram"
    assert saved.tone == "friendly"
    assert saved.brand_context is not None
    assert saved.brand_context["name"] == "Kulfi Lounge"

    assert saved.variations is not None
    assert saved.variations[0]["headline"] == "Berry Refreshment is Here"

    assert saved.content_metadata is not None
    assert saved.content_metadata["source"] == "unit-test"

    db.close()


def test_save_generation_result_to_database():
    db = build_test_db_session()

    generation_result = {
        "generation_engine": "local-template-v1",
        "content_type": "whatsapp_campaign",
        "platform": "WhatsApp",
        "tone": "urgent",
        "brief": "Weekend offer",
        "variations": [
            {
                "variation": 1,
                "headline": "Weekend Offer",
                "caption": "Special dessert offer today.",
                "call_to_action": "Message us now",
            }
        ],
    }

    service = GeneratedContentService()

    saved = service.save_generation_result(
        db=db,
        generation_result=generation_result,
        project_id="project-2",
        title="Weekend WhatsApp Offer",
    )

    fetched = service.get_by_id(
        db=db,
        generated_content_id=saved.id,
    )

    assert fetched is not None
    assert fetched.id == saved.id
    assert fetched.project_id == "project-2"
    assert fetched.title == "Weekend WhatsApp Offer"
    assert fetched.content_type == "whatsapp_campaign"
    assert fetched.variations[0]["call_to_action"] == "Message us now"

    db.close()


def test_list_recent_and_count_generated_contents():
    db = build_test_db_session()

    service = GeneratedContentService()

    for index in range(3):
        service.save_generation_result(
            db=db,
            generation_result={
                "generation_engine": "local-template-v1",
                "content_type": "instagram_post",
                "platform": "Instagram",
                "tone": "friendly",
                "brief": f"Offer {index}",
                "variations": [
                    {
                        "variation": 1,
                        "headline": f"Offer {index}",
                        "caption": "Caption",
                        "call_to_action": "Follow for more",
                    }
                ],
            },
            title=f"Saved Output {index}",
        )

    items = service.list_recent(
        db=db,
        limit=2,
        offset=0,
    )

    total = service.count(db=db)

    assert len(items) == 2
    assert total == 3

    db.close()
