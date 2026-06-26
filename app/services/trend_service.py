from app.schemas.trend import TrendDetectRequest, TrendDetectResponse, TrendIdea


class TrendService:
    def detect_trends(
        self,
        request_data: TrendDetectRequest,
    ) -> TrendDetectResponse:
        trends = []

        for rank in range(1, request_data.result_count + 1):
            trends.append(
                TrendIdea(
                    rank=rank,
                    title=self._build_title(request_data, rank),
                    hook=self._build_hook(request_data, rank),
                    content_angle=self._build_content_angle(request_data, rank),
                    suggested_format=self._get_suggested_format(
                        request_data.platform,
                        rank,
                    ),
                    hashtags=self._build_hashtags(request_data),
                )
            )

        return TrendDetectResponse(
            niche=request_data.niche,
            platform=request_data.platform,
            location=request_data.location,
            audience=request_data.audience,
            trends=trends,
        )

    def get_presets(self) -> dict:
        return {
            "platforms": [
                "Instagram",
                "YouTube",
                "WhatsApp",
                "LinkedIn",
                "Facebook",
                "X",
                "Website",
            ],
            "popular_niches": [
                "Food and Beverage",
                "Fashion",
                "Fitness",
                "Technology",
                "Travel",
                "Education",
                "Personal Brand",
                "Local Business",
            ],
            "formats": [
                "short_video",
                "carousel",
                "story",
                "whatsapp_broadcast",
                "long_form_post",
                "blog",
            ],
            "default_result_count": 5,
            "max_result_count": 10,
        }

    def _build_title(
        self,
        request_data: TrendDetectRequest,
        rank: int,
    ) -> str:
        location_text = f" in {request_data.location}" if request_data.location else ""

        title_templates = [
            f"{request_data.niche} seasonal offer trend{location_text}",
            f"{request_data.niche} behind-the-scenes content trend{location_text}",
            f"{request_data.niche} customer reaction trend{location_text}",
            f"{request_data.niche} limited-time deal trend{location_text}",
            f"{request_data.niche} storytelling trend{location_text}",
        ]

        return title_templates[(rank - 1) % len(title_templates)]

    def _build_hook(
        self,
        request_data: TrendDetectRequest,
        rank: int,
    ) -> str:
        audience_text = request_data.audience or "your audience"

        hooks = [
            f"Show {audience_text} why this is worth trying today.",
            f"Start with a strong visual moment for {request_data.niche}.",
            f"Use a before-and-after style story for {audience_text}.",
            f"Create urgency around a limited-time {request_data.niche} offer.",
            f"Turn your customer experience into a simple story.",
        ]

        return hooks[(rank - 1) % len(hooks)]

    def _build_content_angle(
        self,
        request_data: TrendDetectRequest,
        rank: int,
    ) -> str:
        angles = [
            "Offer-led content with clear call-to-action.",
            "Emotional storytelling focused on customer experience.",
            "Educational content that explains the product benefit.",
            "Visual-first content using colors, movement, and close-up shots.",
            "Community-driven content featuring local or repeat customers.",
        ]

        return angles[(rank - 1) % len(angles)]

    def _get_suggested_format(
        self,
        platform: str,
        rank: int,
    ) -> str:
        normalized_platform = platform.lower()

        if normalized_platform == "instagram":
            formats = ["reel", "carousel", "story", "static_post", "reel"]
        elif normalized_platform == "youtube":
            formats = ["shorts", "long_video", "community_post", "shorts", "live"]
        elif normalized_platform == "whatsapp":
            formats = [
                "broadcast_message",
                "status_update",
                "catalog_offer",
                "broadcast_message",
                "poster_message",
            ]
        elif normalized_platform == "linkedin":
            formats = ["text_post", "carousel", "case_study", "poll", "newsletter"]
        else:
            formats = [
                "short_video",
                "carousel",
                "story",
                "text_post",
                "campaign_message",
            ]

        return formats[(rank - 1) % len(formats)]

    def _build_hashtags(
        self,
        request_data: TrendDetectRequest,
    ) -> list[str]:
        base = request_data.niche.lower().replace(" ", "")
        platform = request_data.platform.lower().replace(" ", "")

        hashtags = [
            f"#{base}",
            f"#{platform}marketing",
            "#contentideas",
            "#trendingnow",
            "#brandgrowth",
        ]

        if request_data.location:
            location_tag = request_data.location.lower().replace(" ", "")
            hashtags.append(f"#{location_tag}")

        return hashtags
