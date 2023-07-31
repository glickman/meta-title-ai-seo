# meta-title-ai-seo

HELLO EVERYONE!


I'm excited to present to you a tool I've developed for SEO optimization – an #AI-powered generator for optimised titles and meta-descriptions. We all know how complicated it can be when a page's title coincides with the h1 tag or when there's a complete absence of a meta-description. But today, I'm offering a solution to this problem.
My tool, created with #Python & #artificialintelligence, specifically, the OpenAI models, allows for the generation of good-quality titles and meta descriptions. 

What's more, it will include the original page titles in the output table, so you don't need to prepare any data in advance. The best part: you don't need experience with virtual machines or programming skills to use this tool.

The principle of the tool is simple:

1. Insert the URLs of the pages for which you need titles and descriptions (you can use the standard list from the Site Audit in #Semrush).
2. Add keywords that can be used.
3. Choose the language of generation (English, Spanish, Russian) and click "Create and Download CSV".
4. Wait a little while and enjoy the result! Under the table, there's a link to download the CSV file.

Before you start using this tool, you will need the #OpenAI API key. Follow the instructions on their site to obtain it (https://platform.openai.com/overview)
Regarding the cost of tokens: for processing 164 pages and preparing a document, I spent only about 1.9€ and 10 minutes of the script running. During this time and for this money, you can enjoy a cup of coffee. Meanwhile, a professional SEO specialist would require 2 to 4 hours to fill in the title and description for this number of pages.


INSTALLING PYTHON3 ON WINDOWS/MAC

For Windows:
1. Go to the Python Downloads page at https://www.python.org/downloads/windows/.
2. Choose the latest Python3 version and download the executable installer.
3. Run the installer file and make sure to check the box labeled "Add Python 3.x to PATH" before clicking on Install.

For Mac:
1. Go to the Python Downloads page at https://www.python.org/downloads/mac-osx/.
2. Download the latest Python3 version for Mac OS and run the .pkg file.
3. Follow the instructions in the Python Installer.

INSTALLING NECESSARY MODULES

Open the terminal/command prompt.
Use the following commands to install the necessary modules. (Please make sure Python3 is installed and added to PATH before proceeding. If Python3 was just installed, you might need to restart your terminal/command prompt.)

pip3 install requests

pip3 install beautifulsoup4

pip3 install pandas

pip3 install openai

RUNNING THE SCRIPT

Open file and PUT your KEY

openai.api_key = 'HERE'

Open the terminal/command prompt and navigate to the directory where you saved the script using the cd command.
Type python3 seo.py in the terminal/command prompt and press enter. The script should start running.

Remember, the script will need an OpenAI API key to function. 
To obtain it, sign up on the OpenAI website, navigate to the API section, and generate a new key.

Be sure to keep this key confidential.
