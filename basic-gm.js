/*
=> getOrCreateWallet() function that does the following:
- It checks if a wallet file (sender_wallet.json) exists.
- If it exists, it reads the private key from the file and creates a wallet from it.
- If it doesn't exist, it creates a new random wallet and saves its details to the file.

*/

const ethers = require('ethers');
const { Client } = require('@xmtp/xmtp-js');
const fs = require('fs');

const WALLET_FILE = 'sender_wallet.json';

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

async function main() {
  // Get or create a persistent sender wallet
  const senderWallet = getOrCreateWallet();
  console.log('Sender address:', senderWallet.address);

  // Create an XMTP client with the sender's wallet, specifying the production environment
  const xmtp = await Client.create(senderWallet, { env: 'production' });

  // Recipient's address (replace with the actual recipient's address)
  const recipientAddress = '0x937C0d4a6294cdfa575de17382c7076b579DC176';

  // Create a new conversation
  const conversation = await xmtp.conversations.newConversation(recipientAddress);

  // Send a message
  const message = 'GM! I'm alive';
  await conversation.send(message);

  console.log(`Message sent to ${recipientAddress}: "${message}"`);
}

main().catch((error) => {
  console.error('Error:', error);
  process.exit(1);
});
