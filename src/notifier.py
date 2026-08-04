from discord_webhook import DiscordWebhook, DiscordEmbed

from src.utils import (
    discord_timestamp,
    get_store_url,
    get_best_image,
)

from src.epic import (
    get_developer,
    get_original_price,
    get_end_date,
)


EPIC_ICON_URL = "https://files.catbox.moe/cy5a0u.png"

RONALDO_ICON_URL = "https://files.catbox.moe/qttqpy.png"


def send_giveaway(webhook_url, game):
    webhook = DiscordWebhook(url=webhook_url)

    embed = DiscordEmbed(
        title=f"🎁 {game['title']}",
        url=get_store_url(game),
        color=0x2ECC71,
    )

    embed.set_author(
        name="Epic Games Developer Giveaway",
        icon_url=EPIC_ICON_URL,
    )

    embed.set_description(
        "⚠️ **Not part of Epic Games' official weekly free games.**"
    )

    embed.add_embed_field(
        name="👨‍💻 Developer",
        value=get_developer(game),
        inline=True,
    )

    embed.add_embed_field(
        name="💸 Price",
        value=f"~~{get_original_price(game)}~~ → **FREE**",
        inline=True,
    )

    embed.add_embed_field(
        name="⏰ Ends",
        value=discord_timestamp(get_end_date(game)),
        inline=False,
    )

    embed.add_embed_field(
        name="🔗 Store Page",
        value=f"[Open Store]({get_store_url(game)})",
        inline=False,
    )

    image = get_best_image(game)

    if image:
        embed.set_image(url=image)

    embed.set_footer(
        text="Subho's EGS Developer Giveaway Informer",
        icon_url=RONALDO_ICON_URL,
    )

    webhook.add_embed(embed)

    response = webhook.execute()

    print(f"Webhook status code: {response.status_code}")

    try:
        print(response.text)
    except Exception:
        pass

    return response
