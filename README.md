# EssensGetter

With EssensGetter you can easily look up what food is served in the canteen of the Berufsakademie Leipzig.
Currently, this service is only available for the canteen "Mensa Schönauer Straße". This python programm allows you to call
the data via HTML Request and converts it to usable data. After that it sends an email with the data to the user.

## Where is the data from?
The data is provided by the [Studentenwerk Leipzig](https://www.studentenwerk-leipzig.de/). You can directly access the data [here](https://www.studentenwerk-leipzig.de/mensen-cafeterien/speiseplan) and choose the canteen "Mensa Schönauer Straße".

## How to run the script?
1. Open the terminal
2. Go to the directory of the script
3. install the library "requests-html" -> 
```bash
pip install requests-html
```
4. Create a new file called "receivers.txt" and put the names and email addresses of the recipients in it.
   1. Note that you have to enter the name first and then the email address
   2. Name and email address have to be in a seperated line
   3. Don't leave whitespaces between the lines
   4. For example:
   ```
      Emil
      emil@email.com
      Paul
      paul@email.com
      Laura
      laura@email.com
      ....
    ```
5. To send Emails via your own SMTP-Server you have to enter your credentials  
6. Run the script with "python3 essensGetter.py"

**Note: You can execute the script via Linux cronjobs to automate the process**