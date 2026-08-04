from discord_webhook import DiscordWebhook, DiscordEmbed


def send_test(webhook_url):
    webhook = DiscordWebhook(url=webhook_url)

    embed = DiscordEmbed(
        title="Epic Developer Giveaway",
        description="This is a test notification.",
        color="2ecc71"
    )

    embed.add_embed_field(
        name="Status",
        value="✅ Webhook is working",
        inline=False
    )

    webhook.add_embed(embed)

    response = webhook.execute()

    return response.status_code
