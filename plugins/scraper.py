import discord
from discord.ext import commands

from bs4 import BeautifulSoup
import requests

class scraper(commands.Cog):
    
    @commands.command(pass_context=True, brief="", name='scraper')
    async def scraperCMD(self,ctx):
        
        url = "xxx"
 
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
                    seenfile.write(url_elem)
                    seenlist.append(url_elem)
                
                    messageToSend = f"{str(title)}\n{str(price)}\n{str(url_elem)}\n"
                    if not messageToSend == "\n\n\n":
                        await ctx.send(messageToSend)
            except:
                pass
        seenfile.close()
    
    def __init__(self,bot):
        
        self.bot = bot
        
        print("Scraper plugin started")
        
def setup(bot):
    bot.add_cog(scraper(bot))