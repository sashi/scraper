import discord
from discord.ext import commands

from bs4 import BeautifulSoup
import requests

def scrape_url(ctx, url):
        page = requests.get(url)
         
        print(page.content)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(class_="rows")
          
        gpu_elems = results.find_all('li',class_="result-row")

        seenfile = open('listings_seen_before.txt', 'r+')
        seenlist = [line.strip() for line in seenfile.readlines()]

        for gpu_elem in gpu_elems:
            try:
                price_elem = gpu_elem.find('span', class_="result-price")
                #url_elem = gpu_elem.find('a', class_="result-image gallery")
                url_elem = gpu_elem.find('a', { 'class': 'result-image gallery'})['href']
                title_elem = gpu_elem.find('a', class_="result-title hdrlnk")
                title = title_elem.text.strip()
                price = int(price_elem.text.strip())
                
                #only operate on the item if we've not seen it before and it's cheap
                if url_elem not in seenlist and price < 1000:
                    print(title)
                    print(price)
                    print(url_elem)
                    seenfile.write(str(url_elem))
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
    
    @commands.command(pass_context=True, brief="", name='scraper')
    async def scraperCMD(self,ctx):
        url = ""
        scrape_url(ctx,url)

    #TODO add more commands for different urls
    
    def __init__(self,bot):
        
        self.bot = bot
        
        print("Scraper plugin started")
        
def setup(bot):
    bot.add_cog(scraper(bot))