def url_to_title(link):
	if 'netflix.com' in link:
		page = requests.get(link)
		soup = BeautifulSoup(page.content, 'html.parser')
		movies = soup.findAll('title')
		title = str(movies)
		title = title.replace('[<title>','')
		title = title.replace('| Netflix</title>]','')
		print('Movie title is: ',title)
	if 'primevideo.com' in link: 
		page = requests.get(link)
		soup = BeautifulSoup(page.content, 'html.parser')
		movies = soup.findAll('title')
		title = str(movies[0])
		title = title.replace('<title>Prime Video:','')
		title = title.replace('</title>','')
		print('Movie title is: ',title)
	else:
		print('URL not redirecting to Netflix or PrimeVideo')