from typing import Any


class ContentPresetService:
    def get_presets(self) -> dict[str, Any]:
        return {
            "content_types": [
                {
                    "key": "instagram_post",
                    "label": "Instagram Post",
                    "description": "Caption, headline, CTA, and hashtag-ready content.",
                    "recommended_platform": "Instagram",
                },
                {
                    "key": "instagram_reel_script",
                    "label": "Instagram Reel Script",
                    "description": "Short-form reel hook, scene flow, voiceover, and CTA.",
                    "recommended_platform": "Instagram",
                },
                {
                    "key": "whatsapp_campaign",
                    "label": "WhatsApp Campaign",
                    "description": "Promotional WhatsApp message with clear CTA.",
                    "recommended_platform": "WhatsApp",
                },
                {
                    "key": "blog_post",
                    "label": "Blog Post",
                    "description": "Structured long-form blog content.",
                    "recommended_platform": "Website",
                },
                {
                    "key": "linkedin_post",
                    "label": "LinkedIn Post",
                    "description": "Professional thought-leadership style post.",
                    "recommended_platform": "LinkedIn",
                },
                {
                    "key": "youtube_script",
                    "label": "YouTube Script",
                    "description": "Video script with hook, intro, body, and CTA.",
                    "recommended_platform": "YouTube",
                },
            ],
            "platforms": [
                "Instagram",
                "WhatsApp",
                "YouTube",
                "LinkedIn",
                "Website",
                "Facebook",
                "X",
                "General",
            ],
            "tones": [
                "friendly",
                "premium",
                "funny",
                "professional",
                "urgent",
                "luxury",
                "youthful",
                "trustworthy",
            ],
            "default_output_count": 3,
            "max_output_count": 10,
        }
