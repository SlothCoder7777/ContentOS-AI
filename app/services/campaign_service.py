from app.schemas.campaign import (
    CampaignContentVariation,
    CampaignGenerateRequest,
    CampaignGenerateResponse,
    CampaignInfluencerDirection,
    CampaignTrendIdea,
    CampaignWhatsAppMessage,
)


class CampaignService:
    def generate(
        self,
        request_data: CampaignGenerateRequest,
    ) -> CampaignGenerateResponse:
        return CampaignGenerateResponse(
            brand_name=request_data.brand_name,
            niche=request_data.niche,
            campaign_goal=request_data.campaign_goal,
            platform=request_data.platform,
            tone=request_data.tone,
            strategy_summary=self._build_strategy_summary(request_data),
            trends=self._build_trends(request_data),
            content_variations=self._build_content_variations(request_data),
            whatsapp_messages=self._build_whatsapp_messages(request_data),
            influencer_direction=self._build_influencer_direction(request_data),
        )

    def _build_strategy_summary(
        self,
        request_data: CampaignGenerateRequest,
    ) -> str:
        offer_text = (
            f" The campaign should highlight this offer: {request_data.offer_details}."
            if request_data.offer_details
            else ""
        )

        return (
            f"Create a {request_data.tone} campaign for {request_data.brand_name} "
            f"targeting {request_data.target_audience} on {request_data.platform}. "
            f"The main goal is: {request_data.campaign_goal}.{offer_text}"
        )

    def _build_trends(
        self,
        request_data: CampaignGenerateRequest,
    ) -> list[CampaignTrendIdea]:
        trends = []

        for rank in range(1, request_data.output_count + 1):
            trends.append(
                CampaignTrendIdea(
                    rank=rank,
                    title=f"{request_data.niche} campaign trend idea {rank}",
                    hook=(
                        f"Show {request_data.target_audience} why "
                        f"{request_data.brand_name} is worth trying now."
                    ),
                    suggested_format=self._suggest_format(
                        platform=request_data.platform,
                        rank=rank,
                    ),
                )
            )

        return trends

    def _build_content_variations(
        self,
        request_data: CampaignGenerateRequest,
    ) -> list[CampaignContentVariation]:
        variations = []

        offer = request_data.offer_details or request_data.campaign_goal

        for index in range(1, request_data.output_count + 1):
            variations.append(
                CampaignContentVariation(
                    variation=index,
                    headline=f"{request_data.brand_name} Campaign Idea {index}",
                    caption=(
                        f"{request_data.brand_name} brings a {request_data.tone} "
                        f"{request_data.niche} campaign for {request_data.target_audience}. "
                        f"Focus: {offer}"
                    ),
                    call_to_action=self._build_call_to_action(request_data.platform),
                )
            )

        return variations

    def _build_whatsapp_messages(
        self,
        request_data: CampaignGenerateRequest,
    ) -> list[CampaignWhatsAppMessage]:
        messages = []

        offer = request_data.offer_details or request_data.campaign_goal

        for index in range(1, request_data.output_count + 1):
            messages.append(
                CampaignWhatsAppMessage(
                    variation=index,
                    message=(
                        f"Hi 👋\n"
                        f"*{request_data.brand_name}* has something special for you!\n"
                        f"{offer}\n"
                        f"Perfect for {request_data.target_audience}.\n"
                        f"{self._build_call_to_action('WhatsApp')}!"
                    ),
                )
            )

        return messages

    def _build_influencer_direction(
        self,
        request_data: CampaignGenerateRequest,
    ) -> CampaignInfluencerDirection:
        first_word = request_data.brand_name.split()[0]

        return CampaignInfluencerDirection(
            influencer_name=f"{first_word} Campaign Muse",
            personality=request_data.tone,
            bio=(
                f"A {request_data.tone} AI influencer persona for "
                f"{request_data.brand_name}, focused on {request_data.niche} "
                f"content for {request_data.target_audience}."
            ),
        )

    def _suggest_format(
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
            formats = ["broadcast_message", "status_update", "poster_message"]
        else:
            formats = ["short_video", "carousel", "text_post"]

        return formats[(rank - 1) % len(formats)]

    def _build_call_to_action(
        self,
        platform: str,
    ) -> str:
        normalized_platform = platform.lower()

        if normalized_platform == "whatsapp":
            return "Message us now"

        if normalized_platform == "instagram":
            return "Follow for more"

        if normalized_platform == "youtube":
            return "Subscribe for more"

        return "Try it today"
