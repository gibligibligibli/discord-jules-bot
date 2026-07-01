import discord
import bot

async def send_log_message(session, channel_id, message):
    guild = session.guild
    channel = guild.get_channel(channel_id)
    if channel:
        await channel.send(message)
    session.log("OK", "Mensagem enviada.")

bot.ACTION_MAP["send_log"] = send_log_message
