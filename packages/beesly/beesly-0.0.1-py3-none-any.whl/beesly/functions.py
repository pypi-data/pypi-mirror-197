import classes
import helpers
import exceptions


def PageWiseTask(page,jobList,pages):
	pageUrl = page.requestUrl
	if pageUrl.count('@page') != 1:
		raise exceptions.InvalidDynamicUrl()
			
	pageUrls = []
	for pageId in pages:
		pageUrls.append(pageUrl.replace('@page',str(pageId)))
	resultSet = []
	for url in pageUrls:
		page.requestUrl = url
		resultSet.append(page.runJobs(jobList))
	jobZipped = []
	for pageResult in resultSet[:-1]:
		jobZipped = list(zip(pageResult,resultSet[resultSet.index(pageResult) + 1]))
	resultList = []
	for jobSet in jobZipped:
		jobMerged = []
		for i in jobSet:
			jobMerged.extend(i)
		resultList.append(jobMerged)
	return resultList
	
def ForEachUrl(urlList,page,jobList):
	resultSet = []
	for url in urlList:
		if url != None:
			page.requestUrl = url
			resultSet.append(page.runJobs(jobList))
	pageZipped = []
	for page in resultSet[:-1]:
		pageZipped = zip(page,resultSet[resultSet.index(page) + 1])
	final = []
	for job in pageZipped:
		buffer = []
		for result in job:
			buffer.extend(result)
		final.append(buffer)
	return final