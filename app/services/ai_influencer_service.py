from app.schemas.ai_influencer import (
    AIInfluencerContentIdea,
    AIInfluencerGenerateRequest,
    AIInfluencerGenerateResponse,
)


class AIInfluencerService:
    def generate(
        self,
        request_data: AIInfluencerGenerateRequest,
    ) -> AIInfluencerGenerateResponse:
        influencer_name = self._build_influencer_name(request_data)

        return AIInfluencerGenerateResponse(
            influencer_name=influencer_name,
            brand_name=request_data.brand_name,
            niche=request_data.niche,
            platform=request_data.platform,
            personality=request_data.personality,
            bio=self._build_bio(
                influencer_name=influencer_name,
                request_data=request_data,
            ),
            content_pillars=self._build_content_pillars(request_data),
            visual_style=self._build_visual_style(request_data),
            content_ideas=self._build_content_ideas(request_data),
        )

    def get_presets(self) -> dict:
        return {
            "niches": [
                "Food and Beverage",
                "Travel",
                "Fashion",
                "Fitness",
                "Technology",
                "Education",
                "Beauty",
                "Local Business",
            ],
            "personalities": [
                "friendly",
                "premium",
                "funny",
                "luxury",
                "youthful",
                "professional",
                "bold",
                "calm",
            ],
            "platforms": [
                "Instagram",
                "YouTube",
                "LinkedIn",
                "WhatsApp",
                "Facebook",
                "X",
            ],
            "language_styles": [
                "simple and engaging",
                "premium and polished",
                "funny and relatable",
                "short and punchy",
                "professional and clear",
            ],
        }

    def _build_influencer_name(
        self,
        request_data: AIInfluencerGenerateRequest,
    ) -> str:
        brand_words = request_data.brand_name.replace("-", " ").split()
        first_word = brand_words[0] if brand_words else "Brand"

        niche_word = request_data.niche.replace("&", " ").split()[0]

        return f"{first_word} {niche_word} Muse"

    def _build_bio(
        self,
        influencer_name: str,
        request_data: AIInfluencerGenerateRequest,
    ) -> str:
        return (
            f"{influencer_name} is a {request_data.personality} AI influencer for "
            f"{request_data.brand_name}, focused on {request_data.niche}. "
            f"The persona speaks to {request_data.target_audience} using a "
            f"{request_data.language_style} style on {request_data.platform}."
        )

    def _build_content_pillars(
        self,
        request_data: AIInfluencerGenerateRequest,
    ) -> list[str]:
        return [
            f"{request_data.niche} education",
            "Behind-the-scenes brand moments",
            "Offer and campaign promotions",
            "Customer-focused storytelling",
            "Trend-based short-form content",
        ]

    def _build_visual_style(
        self,
        request_data: AIInfluencerGenerateRequest,
    ) -> dict[str, str]:
        personality = request_data.personality.lower()

        if personality in {"premium", "luxury"}:
            return {
                "color_mood": "rich, clean, premium",
                "shot_style": "high-quality close-ups and elegant scenes",
                "design_style": "minimal layout with strong product focus",
            }

        if personality in {"funny", "youthful", "bold"}:
            return {
                "color_mood": "bright, energetic, eye-catching",
                "shot_style": "dynamic reels, reactions, and quick cuts",
                "design_style": "bold text overlays and playful layouts",
            }

        return {
            "color_mood": "warm, friendly, approachable",
            "shot_style": "natural product moments and human-style storytelling",
            "design_style": "clean visuals with simple captions",
        }

    def _build_content_ideas(
        self,
        request_data: AIInfluencerGenerateRequest,
    ) -> list[AIInfluencerContentIdea]:
        return [
            AIInfluencerContentIdea(
                title=f"Why {request_data.brand_name} stands out",
                format="reel",
                hook=f"Here is why {request_data.target_audience} should try this.",
                caption_direction="Explain the main product benefit in a simple way.",
            ),
            AIInfluencerContentIdea(
                title=f"Behind the scenes at {request_data.brand_name}",
                format="story",
                hook="A quick look at what makes this brand special.",
                caption_direction="Show trust, quality, and personality.",
            ),
            AIInfluencerContentIdea(
                title=f"{request_data.niche} trend reaction",
                format="short_video",
                hook=f"This trend is perfect for {request_data.brand_name}.",
                caption_direction="Connect a trending idea with the brand offer.",
            ),
        ]
