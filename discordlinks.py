import discord
import arxiv
import re

intents = discord.Intents.default()  # Use the default intents

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, intents=intents)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        # check if the message contains an arXiv link
        match = re.search(r'arxiv.org/pdf/(\d+\.\d+)', message.content)
        if match:
            arxiv_id = match.group(1)

            # fetch the metadata for the paper
            search = arxiv.Search(id_list=[arxiv_id])
            paper = next(search.results())

            # create a string with the metadata
            metadata =  f"**Title**: {paper.title}\n" \
                        f"-----------------------------------------------------------------------------\n" \
                        f"**Abstract**: {paper.summary}\n" \
                        f"-----------------------------------------------------------------------------\n" \
                        f"**Published**: {paper.published}\n" \
                        f"-----------------------------------------------------------------------------\n" \
                        f"**Updated**: {paper.updated}\n" \
                        f"-----------------------------------------------------------------------------\n" \
                        f"**Categories**: {' , '.join(paper.categories)}\n" \
                        f"-----------------------------------------------------------------------------\n" \
                        f"**DOI**: {paper.doi}"

            # split the metadata into chunks of 2000 characters
            chunks = [metadata[i:i+2000] for i in range(0, len(metadata), 2000)]

            # send each chunk as a separate message
            for chunk in chunks:
                await message.channel.send(chunk)

client = MyClient()
client.run('MTEyNjI4MzEyNTAzOTg0NTUxMA.G5uT4a.jYSHdgtcwRu_3gOmGVE-3bTyFqF3MWrHqro5tQ')
