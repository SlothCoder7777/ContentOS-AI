from app.schemas.whatsapp_campaign import (
    WhatsAppCampaignGenerateRequest,
    WhatsAppCampaignGenerateResponse,
    WhatsAppCampaignMessage,
)


class WhatsAppCampaignService:
    def generate(
        self,
        request_data: WhatsAppCampaignGenerateRequest,
    ) -> WhatsAppCampaignGenerateResponse:
        messages = []

        for index in range(1, request_data.output_count + 1):
            messages.append(
                WhatsAppCampaignMessage(
                    variation=index,
                    message=self._build_message(
                        request_data=request_data,
                        index=index,
                    ),
                    short_message=self._build_short_message(
                        request_data=request_data,
                    ),
                    call_to_action=request_data.call_to_action,
                )
            )

        return WhatsAppCampaignGenerateResponse(
            brand_name=request_data.brand_name,
            offer_title=request_data.offer_title,
            tone=request_data.tone,
            output_count=request_data.output_count,
            messages=messages,
        )

    def _build_message(
        self,
        request_data: WhatsAppCampaignGenerateRequest,
        index: int,
    ) -> str:
        greeting = self._get_greeting(request_data.tone)

        parts = [
            greeting,
            f"*{request_data.brand_name}* brings you:",
            f"*{request_data.offer_title}*",
            request_data.offer_details,
        ]

        if request_data.target_audience:
            parts.append(f"Perfect for: {request_data.target_audience}")

        if request_data.validity:
            parts.append(f"Valid till: {request_data.validity}")

        parts.append(f"{request_data.call_to_action}!")

        if index == 2:
            parts.insert(2, "Limited-time offer for our customers.")
        elif index == 3:
            parts.insert(2, "Don’t miss this special deal.")

        return "\n".join(parts)

    def _build_short_message(
        self,
        request_data: WhatsAppCampaignGenerateRequest,
    ) -> str:
        validity_text = (
            f" Valid till {request_data.validity}." if request_data.validity else ""
        )

        return (
            f"{request_data.brand_name}: {request_data.offer_title}. "
            f"{request_data.offer_details}.{validity_text} "
            f"{request_data.call_to_action}!"
        )

    def _get_greeting(self, tone: str) -> str:
        normalized_tone = tone.lower()

        if normalized_tone in {"urgent", "limited", "flash"}:
            return "⚡ Hurry!"

        if normalized_tone in {"premium", "luxury"}:
            return "✨ Exclusive offer"

        if normalized_tone in {"festive", "celebration"}:
            return "🎉 Special celebration offer"

        return "Hi there 👋"
