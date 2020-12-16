import discord
from discord.ext import commands

from bs4 import BeautifulSoup
import requests

async def scrape_url(ctx, url):
        page = requests.get(url)

        print(page.content)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(class_="rows")

        gpu_elems = results.find_all('li',class_="result-row")

        seenfile = open('cl/listings.txt', 'r+')
        seenlist = [line.strip() for line in seenfile.readlines()]

        for gpu_elem in gpu_elems:
            try:
                price_elem = gpu_elem.find('span', class_="result-price")
                #url_elem = gpu_elem.find('a', class_="result-image gallery")
                url_elem = gpu_elem.find('a', { 'class': 'result-image gallery'})['href']
                title_elem = gpu_elem.find('a', class_="result-title hdrlnk")
                title = title_elem.text.strip()
                price = price_elem.text.strip()

                #only operate on the item if we've not seen it before and it's cheap
                if str(url_elem) not in seenlist :
                    print(title)
                    print(price)
                    print(url_elem)
                    seenfile.write(f"{str(url_elem)}\n")
                    seenlist.append(str(url_elem))

                    messageToSend = ""
                    messageToSend = messageToSend + str(title)+"\n"
                    messageToSend = messageToSend + str(price)+"\n"
                    messageToSend = messageToSend + str(url_elem)+"\n"
                    if not messageToSend == "":
                        await ctx.send(messageToSend)
            except:
                pass
        print(seenlist)
        seenfile.close()

class scraper(commands.Cog):

    @commands.command(pass_context=True, brief="", name='gtx1080')
    async def gtx1080(self,ctx):
        url = "https://vancouver.craigslist.org/d/for-sale/search/sss?query=GTX 1080"
        await scrape_url(ctx,url)

    @commands.command(pass_context=True, brief="", name='rtx2060')
    async def rtx2060(self,ctx):
        url = "https://vancouver.craigslist.org/d/for-sale/search/sss?query=RTX 2060"
        await scrape_url(ctx,url)

    #TODO add more commands for different urls
    @commands.command(pass_context=True, brief="", name='rtx2070')
    async def rtx2070(self,ctx):
        url = "https://vancouver.craigslist.org/d/for-sale/search/sss?query=RTX 2070"
        await scrape_url(ctx,url)

    @commands.command(pass_context=True, brief="", name='rx5600')
    async def rx5600(self,ctx):
        url = "https://vancouver.craigslist.org/d/for-sale/search/sss?query=RX 5600"
        await scrape_url(ctx,url)

    @commands.command(pass_context=True, brief="", name='rx5700')
    async def rx5700(self,ctx):
        url = "https://vancouver.craigslist.org/d/for-sale/search/sss?query=RX 5700"
        await scrape_url(ctx,url)



    def __init__(self,bot):

        self.bot = bot

        print("Scraper plugin started")

def setup(bot):
    bot.add_cog(scraper(bot))