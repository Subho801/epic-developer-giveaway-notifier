from discord_webhook import DiscordWebhook, DiscordEmbed

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


def send_giveaway(webhook_url, game):
    webhook = DiscordWebhook(url=webhook_url)

    embed = DiscordEmbed(
        title=game["title"],
        url=get_store_url(game),
        color="2ecc71",
    )

    embed.set_author(
        name="Epic Developer Giveaway"
    )

    embed.set_description(
        "⚠️ This is **NOT** part of Epic's official weekly free games."
    )

    embed.add_embed_field(
        name="Developer",
        value=get_developer(game),
        inline=True,
    )

    embed.add_embed_field(
        name="Publisher",
        value=get_publisher(game),
        inline=True,
    )

    embed.add_embed_field(
        name="Original Price",
        value=get_original_price(game),
        inline=True,
    )

    embed.add_embed_field(
        name="Ends",
        value=discord_timestamp(
            get_end_date(game)
        ),
        inline=False,
    )

    image = get_best_image(game)

    if image:
        embed.set_image(url=image)

    webhook.add_embed(embed)

    return webhook.execute()
