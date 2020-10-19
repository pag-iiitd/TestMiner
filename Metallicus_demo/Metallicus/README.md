************************************
NOTE: This is a demonstration version of Metallicus, bundled with a sample query and a subset of pre-processed functions
from the dataset, to keep the setup light-weight.
************************************

************************************
ENVIRONMENT:
Metallicus has been tested on Windows 10 64-bit system with an Intel Core i7-5500U 2.40GHz processor with 8GB RAM. 

PREREQUISITES:
1) The system requires the following pre-requisites installed:
-jdk1.8, 
-python3.7 or above, 
-pip 19.0.3 or above


The necessary jar files have been provided in the 'jars' sub-folder

2) Unarchive the MetallicusTool.zip file that would extract the TestMiner folder

3) To install the necessary python modules, open the command prompt and run the following commands, replacing with appropriate path details:

cd <path to TestMiner folder>
pip install -r requirements.txt

4) Install NLTK Stopwords Package
python -m nltk.downloader stopwords
************************************

************************************
TOOL EXECUTION INSTRUCTIONS:
The following steps would execute Metallicus on the provided query sample from the evaluation set, whose documentation and signature
may be found at TestMiner/query/querydoc.txt and the test suite template may be found at TestMiner/query/test_temp.py

Steps:

To execute Metallicus from command line on a query sample, run these commands in the command prompt, replacing with appropriate path details:

cd <path to TestMiner folder>
cd scripts
python master.py python test_temp.py


NOTE: master.py takes two arguments: 1) the language of the query (python or java), and 2) the name of the test template file
************************************

************************************
OUTPUT:
Metallicus's execution displays the query details passed, followed by the match function candidates shortlisted. 
Further refining of the candidates happens while processing, as indicated through 'skipped' and 'processed' 
messages displayed. On the execution of the tool, test_temp.py at TestMiner/query/ would be populated with tests recommended by Metallicus.
************************************

