Link to excel for meet: [https://docs.google.com/spreadsheets/d/1pAofYI4Q4Lgb5c0GobnLcvycE8gyT7zLptEOcba1QLI/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1pAofYI4Q4Lgb5c0GobnLcvycE8gyT7zLptEOcba1QLI/edit?usp=sharing)

### 8Nov Client Meeting Note

#### Software overview
* Set of papers → NLP → stored in some forms
  * Find the connection between authors
  * Find the connection between papers (department, university, person)
  * Citation networks : which papers have the most influence in certain areas
    * See how papers evolve and relate to each other
    * See how it influences technology/government policy/etc.
  * Graph networks : better representation of the results
Requirements
* Most important : Ability to link author with potential connections
  * Link on co-authors
  * Work in the same centre/organisation
  * Have geographical connections
  * In the same research group for some specific project
    * May not be able to locate directly from the paper
  * Need to consider that ‘name is not unique’
    * Distinguish people with the same name
    * Match the same people with different name formats
  * Keywords is a good starting point for linking similar topics
* More accurate data
  * Need to check on what are being store currently
* Sentiment : Partial NLP analysis of the paper
  * Analyse smaller section that is positive/critical about something
  * Get the general overview sentiment
* MongoDB : Provide a way to interact without needing to be MongoDB expert
  * Create an interface for people to interact with
Design
* Prioritise what is achievable in this time period (not interested the depth details)
  * Design the whole prototype system : Ideas + how to achieve it
    * How this data model link with query
    * How query get the results
  * Go into detail only for some specific areas
  * State reason for choosing specific technology
    * Python? MongoDB?
    * Suitability to the task?
    * Have more experience within the team?
* Gantt chart
  * State features for each sprints
  * Plan in details for the first 2 sprints
    * Why we will do these tasks first
    * How to track these task + Give estimation for each task
  * Agile : we can apply element of Agile into our Gantt
