# trismax-challenge
--- program to retrieve CSV files and perform database operations ---

This is a quick app I put together for a company as part of their interview process. With that being said, the emphasis here really seemed to be on meeting the list of
deliverables as quickly as possible instead of creating the most robust and fully featured app possible. This is not meant to be a finished product. Below, I will list
what I was asked to do and then talk about some of the decisions I made and the things I thought about when making them. 

The upshot of what I was asked to do was essentially
  - download a CSV file from a remote URL
  - validate each line of the CSV
  - throw out lines that don't match the criteria
  - send clean CSV file to a specified URL
  - be able to perform simple SQL queries on the data (ie search by NOC, year, and medal type)
  - run app once a week at specified time

Things I added

  - persist clean data to database (this seemed to be implied, but wasn't specifically asked for)
  - added basic logging for http responses related to sending out the clean CSV
  - also logged errors related to the format of the original CSV file
  
I really wasn't given any other parameters for this problem, not even so much as a desired framework or language. I went with Python for this challenge because I 
already had experience parsing CSV files with Python and, since there was a bit of a time consideration here, I wanted to stick with things I was already familiar with as much as possible. 
I used the Winter Olympics CSV file because I stumbled on it while doing some research and it was a convenient CSV file I could just download and work with 
without having to think about anything else. 

The biggest decision I had to make, and the one I spent the most amount of time on, was whether I wanted to write my own code for data validation or use an existing 
library. I felt that writing my own data validation code would likely give better performance, but might make the code harder to read and might leave my code more vulnerable
to security concerns such as SQL injections. Also, why reinvent the wheel if there's a plethora of choices just waiting to be pulled in. I also noted that, since the 
retrieval portion of the program only needed to run once per week, I probably didn't need to worry too much about performance as long as there weren't too many records 
(which, in the data set I chose, there weren't). And that's what lead me to use pandas, pandas_schema, and sqlalchemy. In the end, I'm not convinced this method really made
the app more secure, which was a bit of a let down, but in the end this was also beyond the scope of what I was asked to do.

I used "https://httpbin.org/post" to test my post request. I also could have set up postman, and perhaps that was the better option, but again, the story of this 
project seemed to be to hit the minimal functionality as quickly as possible. As such, I was more concerned that everything functioned as intended quickly than that every 
detail was perfect. I also set up some very basic logging to make sure things were working correctly, particularly when I started working on the crontab portion of the app.

The SQL query function was sort of tacked on at the end and really didn't seem to fit the rest of the challenge. There was a lot of emphasis on dealing with the original 
CSV file and then, at the very end, was a bit about doing a single SQL query involving three data fields. If I had more time, maybe I would have set up an Apache server 
with a basic web page, or set up some kind of API endpoint, or set up postman, etc. But the company in question mostly just seemed interested in whether or not I could 
write a simple SQL query. So that's there and that's what it does. 

I ended up using crontab to run the app weekly at it's scheduled time. This is mostly because I'd previously done precisely this for a small app I built that got 
Twitter results periodically a while back. In hindsight, I wonder if it would have been better to just run the app continually and have it monitor it's own tasks and do them
weekly. My understanding is that this can create security concerns. That being said, the function that does the SQL queries should probably be setup to respond to http 
requests in real time. But that's not what was requested, so that's not what was built. Again, I put a lot of emphasis on hitting the list of deliverables quickly. This app
is definitely still rough around the edges and could use quite a bit of polish as well as more error checking and just a general pass concentrating on robustness. 
