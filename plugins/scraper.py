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
		for gpu_elem in gpu_elems:
			try:
				price_elem = gpu_elem.find('span', class_="result-price")
				#url_elem = gpu_elem.find('a', class_="result-image gallery")
				url_elem = gpu_elem.find('a', { 'class': 'result-image gallery'})['href']
				title_elem = gpu_elem.find('a', class_="result-title hdrlnk")
				title = title_elem.text.strip()
				price = price_elem.text.strip()
				
				print(title)
				print(price)
				print(url_elem)
				
				messageToSend = ""
				messageToSend = messageToSend + str(title)+"\n"
				messageToSend = messageToSend + str(price)+"\n"
				messageToSend = messageToSend + str(url_elem)+"\n"
				if not messageToSend == "":
					await ctx.send(messageToSend)
			except:
				pass
	
	def __init__(self,bot):
		
		self.bot = bot
		
		print("Scraper plugin started")
		
def setup(bot):
	bot.add_cog(scraper(bot))