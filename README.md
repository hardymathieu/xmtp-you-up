# xmtp-you-up
To know if my computer is up, it sends me a little message through XMTP every morning.

# Need
I have a little (linux) computer that runs litte tasks for me, like [taking custody of my NFTs](https://github.com/hardymathieu/nftsave) 
Sometimes it dies, and because it's hidden away somewhere and I don't need to do stuff with it daily, sometimes I don't notice. But that means I miss NFT backups, or adding stuff to my a notion table for me (which it is also tasked with doing)

I want to know that it's dead. The easiest way is for it to let me know it's still there. 
A bit like the [canary thing](https://en.wikipedia.org/wiki/Warrant_canary). 

I don't want emails (email servers are a pain), SMS is too expensive, I don't have an app to create a nice push notificaiton on my phone by myself. 
And that's how I thought of XMTP. Because I have [converse](https://getconverse.app/) (which is awesome), and it will also show up in Hey.xyz and Orb. 

After looking in their documentation, and some help from Claude, yup, it's real easy to send messages through XMTP. 
No email server to setup, and it's free. And I get a push notification on my phone.

The most annoying part is setting up node.js. I would have preferred python.

## Nice to have
if I'm gonna do all that, I might as well have it send me something somewhat useful, and not just a "GM".

# Setting up Node.js & sending a message

Create a new directory. From the terminal, you'd do it like this:
> mkdir xmtp-you-up

Then get in there

> cd xmtp-you-up

Once in there, initialize a new Node.js project:
> npm init -y

Install the required dependencies:
> npm install @xmtp/xmtp-js ethers@5.7.2

Note: I'm using ethers v5 here as it's compatible with the current version of xmtp-js.

Create a new file named gm.js and paste the code that you find in the [basic-gm.js file in this repo](https://github.com/hardymathieu/xmtp-you-up/blob/main/basic-gm.js) into it.

To run the script:
> node basic-gm.js

## to send every morning at 6:30 am, use cron

Open the crontab file for editing

> crontab -e

Add the following line to the crontab file

> 30 6 * * * /usr/bin/node /home/you/xmtp-you-up/basic-gm.js

Save and exit the editor. If you're using nano, press Ctrl+X, then Y, then Enter.

Done!

Claude also had this to say which beginners like me might find useful:
* Ensure that the Node.js path is correct. You can find it by running

> **which node**

in the terminal.

* Make sure your script has the necessary permissions to run.


# taking it a step further: reading a page, summarizing it, and sending that over XMTP instead of a GM
This is wholly unecessary for the purpouse of solving my problem. 
But I have ollama and I kinda want to find out what I can do :) 
Read on for useless stuff.
