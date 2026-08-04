from discord_webhook import DiscordWebhook, DiscordEmbed

from src.config import COUNTRY

from src.utils import (
    discord_timestamp,
    get_store_url,
    get_best_image,
)

from src.epic import (
    get_developer,
    get_publisher,
    get_original_price,
    get_end_date,
)

# Replace these with your own image URLs
EPIC_ICON_URL = "https://YOUR_EPIC_LOGO_URL.png"
RONALDO_ICON_URL = "https://YOUR_RONALDO_IMAGE_URL.png"


def send_giveaway(webhook_url, game):
    webhook = DiscordWebhook(url=webhook_url)

    embed = DiscordEmbed(
        title=f"🎁 {game['title']}",
        url=get_store_url(game),
        color=0x2ECC71,
    )

    embed.set_author(
        name="Epic Games Developer Giveaway",
        icon_url="https://files.catbox.moe/cy5a0u.png",
    )

    embed.set_description(
        "⚠️ **Not part of Epic Games' official weekly free games.**\n\n"
        "Claim it before the promotion ends!"
    )

    embed.add_embed_field(
        name="👨‍💻 Developer",
        value=get_developer(game),
        inline=True,
    )

    embed.add_embed_field(
        name="🏢 Publisher",
        value=get_publisher(game),
        inline=True,
    )

    embed.add_embed_field(
        name="🌍 Region",
        value=COUNTRY,
        inline=True,
    )

    embed.add_embed_field(
        name="💸 Discount",
        value=f"~~{get_original_price(game)}~~ → **FREE**",
        inline=True,
    )

    embed.add_embed_field(
        name="⏰ Ends",
        value=discord_timestamp(get_end_date(game)),
        inline=True,
    )

    embed.add_embed_field(
        name="🔗 Store Page",
        value=f"[Open Store]({get_store_url(game)})",
        inline=False,
    )

    image = get_best_image(game)

    if image:
        embed.set_image(url=image)

   

    webhook.add_embed(embed)

    response = webhook.execute()

print(f"Webhook status code {response.status_code}")

try:
    print(response.text)
except Exception:
    pass

return response
