from discord.ext import commands
from google.cloud import vision
import os
import requests


class Ocr(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix="!", help_command=None, **kwargs)
        self.vision_client = (
            vision.ImageAnnotatorClient()
        )  # Google Vision API authentication needed


ocr_bot = Ocr()


@ocr_bot.event
async def on_ready():
    print(f"Activated as {ocr_bot.user.name}, {ocr_bot.user.id}")


@ocr_bot.command()
async def ocr(ctx: commands.Context):
    if not ctx.message.attachments[0]:
        return await ctx.send("Pls attach your image")

    image = vision.Image(content=requests.get(ctx.message.attachments[0].url).content)
    response = ocr_bot.vision_client.text_detection(image=image)

    texts = response.text_annotations
    if not texts:
        return await ctx.send("I couldn't find any text in your image!")
    text = texts[0].description

    await ctx.send(f"```{text}```")


ocr_bot.run(os.environ["BOT_TOKEN"])
