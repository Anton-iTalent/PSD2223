# Patrick__Barrera_and_Collins


## Performance experimental design and docs


* There is no description of the environment the experiment ran in. Some environment specifications would have been useful for comparison with performance in other environments.

* The profiling method is lacking detail. There is no outline of the experiment, exact tools or justification for choosing them and it is unclear whether the profiling procedure tasks were repeated for all five runs.

* Good documentation for the instructions for running the profiling commands but the profile output files should not have been pushed to the repository. These should have been managed with gitignore.


## Results and analysis visualisation


* The team should have considered ways of documenting the program’s flow other than a rushed description in the summary paragraph. Some examples would be through the use of a flowchart, or pseudocode.

* The team should have considered better ways of visualising the profiling outputs table of numbers of calls per function. For example, a graph showing each of the functions time as a percentage of the total program time.


## Quality of analysis


* The team did not conduct a detailed analysis of the program flow.

* The defects section is described in a non-specific and vague manner. It is unclear what conversion this is referring to.

* Listing of dependencies is missing out the fact that the requirements file contains unnecessary requirements. This is also a strict interpretation of dependency with no regard to other dependencies such as input formatting.

* Presentation of profiling outputs without any analysis of the results.

* Suggestions for improvement are described in a non-specific and vague manner. For example “Separating the code into two scripts should increase the practicality when running and profiling.” - what parts of the code would be separated, why would it be an improvement? Looking at the files in the repository a reader can see two scripts but this should have been explained and justified in the report.

* Use of vague and unjustified statements such as “various sections of the code are redundant” should be avoided. The redundant code and code that has potential for parallelisation should have been identified and explicitly stated.


## Conceptual understanding of the problem and code


* If the defects section is referring to the PDF to DOCX and/or DOCX to JSON, then this is an incorrect assumption. The conversion does not take place if the paper already has DOCX or JSON files present on the filesystem.

* “JSON SQL database” under Dependencies shows a misunderstanding of the program processes and what an SQLite database is.

* “First part of the document conversion should not be required to run every time if the user only wants to query the existing database” shows a misunderstanding of the program processes because the program was only tested for a fresh run. If the program would have been analysed in more detail and/or profiled with more use cases, it would have become apparent that the conversion is only called if a paper does not already have a DOCX or JSON file present on the filesystem.


## Quality of presentation


* Use of README file makes the review report easier to find, however, the initial information about the program has been deleted instead of being expanded on or at least linked from the main documentation.

* Small summary of what the program does is a good introduction.

* The language used is very sparse, non-specific and vague. For example “Total of five profiling procedures were generated…” - assuming this refers to running the profiler command five times.

* Commit history shows pre-assessment bulk push of work, not showing progression in time, and commit messages are non-descriptive.