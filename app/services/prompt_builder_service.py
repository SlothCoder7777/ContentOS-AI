from typing import Any


class PromptBuilderService:
    def build_content_system_prompt(self) -> str:
        return (
            "You are ContentOS AI, an expert AI content strategist. "
            "Create clear, practical, brand-aware marketing content. "
            "Keep output useful, structured, and ready for real business use."
        )

    def build_content_user_prompt(
        self,
        title: str,
        content_type: str,
        platform: str | None,
        brief: str | None,
        tone: str | None,
        output_count: int,
        brand_context: dict[str, Any] | None = None,
    ) -> str:
        return "\n".join(
            [
                f"Project title: {title}",
                f"Content type: {content_type}",
                f"Platform: {platform or 'General'}",
                f"Tone: {tone or 'engaging'}",
                f"Brief: {brief or title}",
                f"Output count: {output_count}",
                f"Brand context: {brand_context or 'No brand context provided'}",
                "",
                "Generate polished marketing content.",
                "Return content that can be used directly by a business owner.",
            ]
        )

    def build_campaign_system_prompt(self) -> str:
        return (
            "You are ContentOS AI, a campaign strategist. "
            "Create marketing campaigns with trend ideas, content angles, "
            "WhatsApp messages, and influencer directions."
        )

    def build_campaign_user_prompt(
        self,
        brand_name: str,
        niche: str,
        campaign_goal: str,
        target_audience: str,
        platform: str,
        offer_details: str | None,
        tone: str,
        output_count: int,
    ) -> str:
        return "\n".join(
            [
                f"Brand name: {brand_name}",
                f"Niche: {niche}",
                f"Campaign goal: {campaign_goal}",
                f"Target audience: {target_audience}",
                f"Platform: {platform}",
                f"Offer details: {offer_details or 'No specific offer'}",
                f"Tone: {tone}",
                f"Output count: {output_count}",
                "",
                "Create a complete campaign package.",
                "Include strategy, hooks, captions, CTA ideas, and platform-specific suggestions.",
            ]
        )
