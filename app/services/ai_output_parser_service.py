from typing import Any

from app.schemas.ai_output import AIContentVariation, StructuredAIOutput


class AIOutputParserService:
    def parse_content_generation_result(
        self,
        generation_result: dict[str, Any],
    ) -> StructuredAIOutput:
        raw_output = generation_result.get("raw_output") or generation_result.get(
            "ai_output"
        )

        variations = self._parse_variations(
            generation_result=generation_result,
            raw_output=raw_output,
        )

        return StructuredAIOutput(
            generation_engine=self._safe_string(
                generation_result.get("generation_engine"),
                "unknown",
            ),
            model=self._safe_optional_string(generation_result.get("model")),
            content_type=self._safe_string(
                generation_result.get("content_type"),
                "general_content",
            ),
            platform=self._safe_string(
                generation_result.get("platform"),
                "General",
            ),
            tone=self._safe_string(
                generation_result.get("tone"),
                "engaging",
            ),
            brief=self._safe_string(
                generation_result.get("brief"),
                "Generated content",
            ),
            brand_context=generation_result.get("brand_context"),
            variations=variations,
            raw_output=self._safe_optional_string(raw_output),
        )

    def parse_raw_text_response(
        self,
        raw_output: str,
        content_type: str,
        platform: str = "General",
        tone: str = "engaging",
        brief: str = "Generated content",
        generation_engine: str = "openai",
        model: str | None = None,
        brand_context: dict[str, Any] | None = None,
    ) -> StructuredAIOutput:
        return StructuredAIOutput(
            generation_engine=generation_engine,
            model=model,
            content_type=content_type,
            platform=platform,
            tone=tone,
            brief=brief,
            brand_context=brand_context,
            raw_output=raw_output,
            variations=[
                AIContentVariation(
                    variation=1,
                    headline=brief,
                    caption=raw_output,
                    call_to_action="Try it today",
                )
            ],
        )

    def _parse_variations(
        self,
        generation_result: dict[str, Any],
        raw_output: Any,
    ) -> list[AIContentVariation]:
        raw_variations = generation_result.get("variations", [])

        if not isinstance(raw_variations, list):
            raw_variations = []

        parsed_variations = [
            self._parse_single_variation(
                variation_data=variation_data,
                fallback_number=index + 1,
            )
            for index, variation_data in enumerate(raw_variations)
        ]

        if parsed_variations:
            return parsed_variations

        if raw_output:
            return [
                AIContentVariation(
                    variation=1,
                    headline=self._safe_string(
                        generation_result.get("brief"),
                        "Generated Content",
                    ),
                    caption=self._safe_string(
                        raw_output,
                        "Generated content",
                    ),
                    call_to_action=self._safe_string(
                        generation_result.get("call_to_action")
                        or generation_result.get("cta"),
                        "Try it today",
                    ),
                )
            ]

        return []

    def _parse_single_variation(
        self,
        variation_data: Any,
        fallback_number: int,
    ) -> AIContentVariation:
        if not isinstance(variation_data, dict):
            return AIContentVariation(
                variation=fallback_number,
                headline=f"Variation {fallback_number}",
                caption=self._safe_string(
                    variation_data,
                    "Generated content",
                ),
                call_to_action="Try it today",
            )

        return AIContentVariation(
            variation=self._safe_int(
                variation_data.get("variation"),
                fallback_number,
            ),
            headline=self._safe_string(
                variation_data.get("headline"),
                f"Variation {fallback_number}",
            ),
            caption=self._safe_string(
                variation_data.get("caption")
                or variation_data.get("message")
                or variation_data.get("body"),
                "Generated content",
            ),
            call_to_action=self._safe_string(
                variation_data.get("call_to_action") or variation_data.get("cta"),
                "Try it today",
            ),
            hashtags=self._parse_hashtags(
                variation_data.get("hashtags"),
            ),
            notes=self._safe_optional_string(
                variation_data.get("notes"),
            ),
        )

    def _parse_hashtags(self, value: Any) -> list[str]:
        if value is None:
            return []

        if isinstance(value, str):
            items = value.replace(",", " ").split()
            return [self._normalize_hashtag(item) for item in items if item.strip()]

        if isinstance(value, list):
            return [
                self._normalize_hashtag(str(item))
                for item in value
                if str(item).strip()
            ]

        return []

    def _normalize_hashtag(self, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            return ""

        if cleaned.startswith("#"):
            return cleaned

        return f"#{cleaned}"

    def _safe_string(
        self,
        value: Any,
        fallback: str,
    ) -> str:
        if value is None:
            return fallback

        text = str(value).strip()

        if not text:
            return fallback

        return text

    def _safe_optional_string(
        self,
        value: Any,
    ) -> str | None:
        if value is None:
            return None

        text = str(value).strip()

        if not text:
            return None

        return text

    def _safe_int(
        self,
        value: Any,
        fallback: int,
    ) -> int:
        try:
            number = int(value)

            if number < 1:
                return fallback

            return number

        except (TypeError, ValueError):
            return fallback


ai_output_parser_service = AIOutputParserService()
