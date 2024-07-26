# xmtp-you-up
To know if my computer is up, it sends me a little message through XMTP every morning.

# Need
I have a little (linux) computer that runs litte tasks for me, like [taking custody of my NFTs](https://github.com/hardymathieu/nftsave) .

Sometimes it dies, and because it's hidden away somewhere and I don't need to do stuff with it daily, sometimes I don't notice. But that means I miss NFT backups, or adding stuff to a notion table for me (which it is also tasked with doing)

I want to know that it's dead. The easiest way is for it to let me know it's still there. 
A bit like the [canary thing](https://en.wikipedia.org/wiki/Warrant_canary). 

I don't want emails (email servers are a pain), SMS is too expensive, I don't have an app to create a nice push notificaiton on my phone by myself. 
And that's how I thought of XMTP. Because I have [converse](https://getconverse.app/) (which is awesome), and it will also show up in Hey.xyz and Orb. 

After looking in their documentation, and some help from Claude, yup, it's real easy to send messages through XMTP. 
No email server to setup, and it's free. And I get a push notification on my phone.

The most annoying part is setting up node.js. I would have preferred python.

## Nice to have
if I'm gonna do all that, I might as well have it send me something somewhat useful, and not just a "GM".
See below for [fun stuff](https://github.com/hardymathieu/xmtp-you-up/tree/main?tab=readme-ov-file#taking-it-a-step-further-reading-a-page-summarizing-it-and-sending-that-over-xmtp-instead-of-a-gm).

# Setting up Node.js & sending a message

Create a new directory. From the terminal, you'd do it like this:
```
mkdir xmtp-you-up
```
Then get in there
```
cd xmtp-you-up
```
Once in there, initialize a new Node.js project:
```
npm init -y
```
Install the required dependencies:
```
npm install @xmtp/xmtp-js ethers@5.7.2
```
Note: I'm using ethers v5 here as it's compatible with the current version of xmtp-js.

Create a new file named gm.js and paste the code that you find in the [basic-gm.js file in this repo](https://github.com/hardymathieu/xmtp-you-up/blob/main/basic-gm.js) into it.

To run the script:
```
node basic-gm.js
```
## to send every morning at 6:30 am, use cron

Open the crontab file for editing
```
crontab -e
```
Add the following line to the crontab file
```
30 6 * * * /usr/bin/node /home/you/xmtp-you-up/basic-gm.js
```
Save and exit the editor. If you're using nano, press Ctrl+X, then Y, then Enter.

Done!

Claude also had this to say which beginners like me might find useful:
* Ensure that the Node.js path is correct. You can find it by running the following in the terminal
```
which node
```

* Make sure your script has the necessary permissions to run.


# taking it a step further: reading a page, summarizing it, and sending that over XMTP instead of a GM
This is wholly unecessary for the purpose of solving my problem. 
But I have ollama and I kinda want to find out what I can do :) 
Read on for not strictly useful but fun stuff.

The idea here is to make the morning message interesting. So I’m going to ask for a daily news briefing.

## Step 1: with Python scrape a news site for the last 5 news, use ollama and Phi3 to get the scraped data and turn that into an actual summary, put that summary in a sqlite db

* Get yourself [ollama](https://ollama.com/download/linux) and [download Phi3](https://github.com/ollama/ollama?tab=readme-ov-file#pull-a-model). [It has APIs, that’s awesome](https://github.com/ollama/ollama?tab=readme-ov-file#rest-api). [We’ll use the Python library](https://github.com/ollama/ollama-python). They also have [JS](https://github.com/ollama/ollama-js), but I like (= I have fiddled around more with) python. 
* Make yourself a [venv](https://github.com/hardymathieu/nftsave/blob/main/README.md#psa-a-note-if-like-me-youre-newish-to-python-and-shy) in that xmtp-you-up folder
```
python -m venv /home/you/xmtp-you-up/xmtppy
```
* Then make sure you have the required packages
```
/home/you/xmtp-you-up/xmtppy/bin/python /home/you/xmtp-you-up/xmtppy/bin/pip install requests beautifulsoup4 ollama
```
* Take the code in [news_summary_to_db.py](https://github.com/hardymathieu/xmtp-you-up/blob/main/news_summary_to_db.py) & run it. When it's done running you should have a db called “rtbf_news.db" with one entry
```
/home/you/xmtp-you-up/xmtppy/bin/python /home/you/xmtp-you-up/news_summary_to_db.py
```
## Step 2: with Node and the XMTP SDK, get the XMTP bot to retrieve the entry in the db and send that as a message instead.

* Install the required dependencies, from inside the xmtp-you-up folder since that’s where we previously initialized the Node.js project with npm
```
cd /home/you/xmtp-you-up
```
```
npm install ethers @xmtp/xmtp-js sqlite3
```
Use the code in xmtp_news_gm.js and put it into the xmtp-you-up folder, change the recipient to be your wallet, and run
```
node /home/you/xmtp-you-up/xmtp_news_gm.js
```
You should have gotten your daily briefing notification after a couple of seconds.

## Step 3: cron for the daily dose of news

### Cron with Python
This at the top of your python code ensures that it’s the venv python that’s used -- change the path to yours

```
#!/home/you/xmtp-you-up/xmtppy/bin/python
#-*- coding: utf-8 -*- 
```
Then make the python script executable
```
sudo chmod +x /home/you/xmtp-you-up/news_summary_to_db.py
```
Then 
```
crontab -e
```

Add a line - to start the script at 6:20 am
```
20  6 * * * /home/you/xmtp-you-up/news_summary_to_db.py
```
Then, to exit nano
* CTRL+X
* Y
* enter

### 8 minutes later, cron for notification with Node.js

It takes a bit of time to do the scraping (on my little machine). Not 8 min, but running an LLM on CPU on a small box does take a bit of time. And it’s early morning, there’s no need to rush.

```
crontab -e
```

Add a line - to start the script at 6:28 am

```
28  6 * * * /usr/bin/node /home/you/xmtp-you-up/xmtp_news_gm.js
```


Then, to exit nano
* CTRL+X
* Y
* enter

Boom. Daily news briefing in a notification every morning so you know your computer is still up and you stay informed.

# Future ideas, because XMTP is the simplest messaging thing I’ve ever seen

* IoT: a button (or little sensor, or connetions to the Wifi network) to have household members broadcast “I’m home” to family. 
* Just chatting with an LLM: I could quite probably have convos with ollama/phi 3 over XMTP. I think that would be the easiest interface to use for that use case.
* Use XMTP to send messages/todos/ideas/…  to my computer, and have an LLM pick it up and organise it all for me. Doesn’t need to be conversational; one way would be fine.

If you build any of that, let me know: [mhardymathieu.converse.xyz](http://mhardymathieu.converse.xyz) or via xmtp on m.hardymathieu.eth :) 
