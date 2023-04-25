# 🕸️ Web-Crawler
This is a Phase 1 of OASIS project. These python scripts are spiders to crawl from web sites and extract data related cybersecurity, haking attacks and data breaches.
This web crawler has been built with __Scrapy__ framework and some other python libraries for data scraping like __selenium__, __beautifulsoup__ and __requests__.
## Getting started 🚀

---

- First, you need to create a python virtual environment -> "venv" in the project folder directoy:

  Please open your command terminal and run the following command:

  ```shell
  python -m venv /path/to/your project
  ```

  This will make a .venv folder in your project folder directory.


- Second, select the python interpreter:

  In your IDE (highly recommend VS code), open the command palette with __"ctrl + shift + p"__ on windows or __"cmd + shift + p"__ on MacOS.
  Then, select the **./.venv\Scripts\python.exe** interpreter.

 
- Third, activate the virtual environment:

  Open command prompt in your project folder directory and run following command

   On windows, run:

   ```shell
   .venv\Scripts\activate.bat
   ```

   On MacOS, run:

   ```shell
   source .venv/bin/activate
   ```
 
 - Then, please install all dependencies with following command:
 
   If you are using **pip** python package manager, you just need to do a simple:
 
   ```shell
   pip install
   ```
   
## Run script 🕷️

---

- Change the current directory to Crawler_1 directory in the terminal.
- You can run spiders with following command:

  ```shell
  scrapy crawl <spider_name>
  ```
