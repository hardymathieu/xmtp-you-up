const ethers = require('ethers');
const { Client } = require('@xmtp/xmtp-js');
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();

// SQLite database file
const DB_FILE = '/home/you/xmtp-you-up/rtbf_news.db';

// XMTP wallet file
const WALLET_FILE = '/home/you/xmtp-you-up/sender_wallet.json';

// Function to get or create a persistent wallet
function getOrCreateWallet() {
  if (fs.existsSync(WALLET_FILE)) {
    const walletData = JSON.parse(fs.readFileSync(WALLET_FILE, 'utf8'));
    return new ethers.Wallet(walletData.privateKey);
  } else {
    const wallet = ethers.Wallet.createRandom();
    fs.writeFileSync(WALLET_FILE, JSON.stringify({
      address: wallet.address,
      privateKey: wallet.privateKey
    }));
    return wallet;
  }
}

// Function to get the latest news summary from the database
function getLatestNewsSummary() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_FILE, (err) => {
      if (err) {
        return reject(err);
      }
    });

    db.get('SELECT summary FROM daily_news_summary ORDER BY id DESC LIMIT 1', [], (err, row) => {
      if (err) {
        return reject(err);
      }
      db.close();
      resolve(row ? row.summary : null);
    });
  });
}

async function main() {
  // Get or create a persistent sender wallet
  const senderWallet = getOrCreateWallet();
  console.log('Sender address:', senderWallet.address);

  // Create an XMTP client with the sender's wallet, specifying the production environment
  const xmtp = await Client.create(senderWallet, { env: 'production' });

  // Recipient's address (replace with the actual recipient's address)
  const recipientAddress = '0x937C0d4a6294cdfa575de17382c7076b579DC176';

  // Get the latest news summary from the database
  const latestSummary = await getLatestNewsSummary();
  if (!latestSummary) {
    console.error('No news summary found in the database.');
    process.exit(1);
  }

  // Create a new conversation
  const conversation = await xmtp.conversations.newConversation(recipientAddress);

  // Send a message
  const message = `GM! I'm alive. Here are the news of the day: ${latestSummary}. You can find out more at rtbf.be/info`;
  await conversation.send(message);

  console.log(`Message sent to ${recipientAddress}: "${message}"`);
}

main().catch((error) => {
  console.error('Error:', error);
  process.exit(1);
});
