import discord
from discord.ext import commands

from bs4 import BeautifulSoup
import requests

async def scrape_url(ctx, url):
        page = requests.get(url)
        request = requests.get(url)

        print(page.content)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(class_="rows")
        soup2 = BeautifulSoup(request.content, 'html.parser')
        gpu_elems = results.find_all('li',class_="result-row")

        all_tags = list(soup2.find_all('div', class_='alert alert-sm alert-warning'))
        gpu_elems = results.find_all('li',class_="result-row")

        seenfile = open('cl/listings.txt', 'r+')
        seenlist = [line.strip() for line in seenfile.readlines()]

        for tag in all_tags:
            if len(tag.text) > 0:
                await ctx.send("No results")

        for gpu_elem in gpu_elems:
            try:
                price_elem = gpu_elem.find('span', class_="result-price")
                #url_elem = gpu_elem.find('a', class_="result-image gallery")
                url_elem = gpu_elem.find('a', { 'class': 'result-image gallery'})['href']
                title_elem = gpu_elem.find('a', class_="result-title hdrlnk")
                title = title_elem.text.strip()
                price = price_elem.text.strip()
                price_int = int(price.replace("$",""))

                #only operate on the item if we've not seen it before and it's cheap
                if str(url_elem) not in seenlist and price_int < 600:
                    print(title)
                    print(price)
                    print(url_elem)
                    #seenfile.write(f"{str(url_elem)}\n")
                    #seenlist.append(str(url_elem))

                    messageToSend = ""
                    messageToSend = messageToSend + str(title)+"\n"
                    messageToSend = messageToSend + str(price)+"\n"
                    messageToSend = messageToSend + str(url_elem)+"\n"
                    if not messageToSend == "":
                        await ctx.send(messageToSend)
            except:
                pass
        #print(seenlist)
        #seenfile.close()


class scraper(commands.Cog):

    @commands.command(pass_context=True, brief="", name='search')
    async def searchCMD(self,ctx,*searchterm):
        searchterm = " ".join(searchterm)
        url = "https://vancouver.craigslist.org/d/for-sale/search/sss?sort=pricedsc&query="+str(searchterm)
        await scrape_url(ctx,url)

    @commands.command(pass_context=True, brief="", name='searchmax')
    async def searchmaxCMD(self,ctx,searchterm,price):
        #searchterm = "".join(searchterm)
        url = "https://vancouver.craigslist.org/d/for-sale/search/sss?sort=pricedsc&query="+str(searchterm)+"&max_price="+str(price)
        await scrape_url(ctx,url)
        #print(ctx,url)



    def __init__(self,bot):

        self.bot = bot

        print("Scraper plugin started")

def setup(bot):
    bot.add_cog(scraper(bot))