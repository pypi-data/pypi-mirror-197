class InvalidUserAgentType(Exception):
	def __init__(self,message):
		super().__init__(f'\"{message}\" is a invalid User-Agent type please choose from [desktop,smartphone,tablet]')
		
class InvalidJobQuery(Exception):
	def __init__(self,message):
		super().__init__(f'Job query must have 3 elements but \"{message}\" has only {len(message)} ')
		
		
class InvalidExportFileFormat(Exception):
	def __init__(self,message):
		super().__init__(f'\"{message}\" is not a valid export file format. Please use csv or json')
		
class InvalidDynamicUrl(Exception):
	def __init__(self,message):
		super().__init__(f'The url provided is invalid. The url muct contain only one @page.')
		
