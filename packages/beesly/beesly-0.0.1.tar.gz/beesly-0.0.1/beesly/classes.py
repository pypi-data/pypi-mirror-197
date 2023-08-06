import requests
from bs4 import BeautifulSoup
import helpers
from helpers import log
import exceptions

class Page:
	def __init__(self,url,userAgentType = 'all',headers = {},parser = 'html.parser'):
		self.requestUrl = url
		self.headers = headers
		self.UserAgent = helpers.getUserAgent(userAgentType)
		self.parser = parser
		self.headers['User-Agent'] = self.UserAgent
	def load(self):
		log(f'Loading page {self.requestUrl}')
		try:
			self.soup = BeautifulSoup(requests.get(self.requestUrl,headers=self.headers).text,self.parser)
		except Exception as e:
			print(f'There was a problem loading the page {self.requestUrl} : {e}')
			quit()
	def runJobs(self,jobs,export=None):
		self.load()
		log(f'Running {len(jobs)} jobs')
		resultSet = []
		jobId = 1
		for job in jobs:
			log(f'[Job {jobId}] Running {len(job.queries)} queries')
			resultSet.append(job.run(self.soup,export))
			jobId += 1
		return resultSet

class Job:
	def __init__(self,queries):
		for item in queries:
			if len(item) != 3:
				raise exceptions.InvalidJobQuery(item)
		self.queries = queries

	def run(self,soup,export=None):
		results = []
		objects = 0
		queryId = 1
		for query in self.queries:
			data = soup.select(query[0])
			log(f'[query {queryId}] {len(data)} tags collected')
			result = [query[1]]
			value = query[2]
			for item in data:
				if value == 'content':
					selection = item.contents
				if value == 'text':
					selection = item.string
				else:	
					selection = item.get(value)
				objects += 1
				result.append(selection)
			results.append(result)
			queryId += 1
		
		if len(results) == 1:
			if export == None:
				return results[0][1:]
			else:
				results = [[i] for i in results[0]]
				helpers.export(results,export)
		else:
			zipped = []
			for result in results[:-1]:
				zipped.extend(zip(result,results[results.index(result) + 1]))
			if export == None:
				return list(zipped)[1:]
			else:
				if export.split('.')[1] == 'csv':
					helpers.export(list(zipped),export)
				else:
					helpers.export(list(zipped),export)
					
					
					
			


'''
a = Page('https://xhamster19.desi')
r = Job([['.thumb-image-container__image','name','alt'],['.video-thumb-views','views','text']])
f = Job([['.thumb-image-container__image','name','alt'],['span','test','text']])
print(a.runJobs([r],export='hello.csv'))
'''