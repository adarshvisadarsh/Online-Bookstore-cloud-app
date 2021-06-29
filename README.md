
## BookStore Application
### Cloud Computing: CSCI-5409

#### Contents
1. A3_Extraction includes the logic to scrap english books with author names from given url.
   (http://www.gutenberg.org/wiki/Gutenberg:Offline_Catalogs)

2. A3_Backend includes the files for running containerized docker application on Ubuntu EC2 instance hosted on AWS.
	
	Directory Structure:

	~A3_Backend/ 
		~docker-compose.yml
		
		~search_service/
		
			~Dockerfile
			
			~requirements.txt
			
			~search.py
			
			~search_log.txt
			
		~notes_service/
		
			~Dockerfile
			
			~requirements.txt
			
			~notes.py
			
		~catalog_service/
		
			~Dockerfile
			
			~requirements.txt
			
			~data.json
			
			~catalog.py
			
		~web-app/
		
			~index.html
			
			~css/
			
				~main.css
			

	Description:
	- Docker-compose acts as the 'Services' in the cloud application infrastructure facilitating a virtual gateway for the incoming requests. Each service is containerized in separate directories and runs on different ports. Each service has its own requirements.txt file where the dependencies are listed.

#### Steps to Execute:

 - Run index.html on any browser.
 - Enter Search Keyword in the search bar and hit Enter. Ex: "James","Charles"
 - Click on the 'Add Notes' button to add new note about the search 
 	- Enter text for the note and click OK button.
 - Or Click 'View Notes' button to view notes in the Notes section.
 - Repeat above operations in any sequence. 
 - Evaluate search_logs.txt in search_service container. It shows the search keywords with their frequencies and timestamp.
 - Evaluate data.json in catalog_service container.It shows search_results appended each time of a successful search.

#### License
##### B00807065 - Aakash Patel 
