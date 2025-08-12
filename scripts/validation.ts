import { RestClient } from 'bybit-api';

export async function testBybitConnection(apiKey: string, apiSecret: string) {
  try {
    const client = new RestClient(
      apiKey,
      apiSecret,
      true // use testnet for safety
    );

    // Try to fetch account info to validate connection
    const serverTime = await client.getServerTime();
    const walletBalance = await client.getWalletBalance({ coin: 'USDT' });

    console.log('Connection successful!');
    console.log('Server time:', serverTime);
    console.log('Wallet balance:', walletBalance);

    return true;
  } catch (error) {
    console.error('Failed to connect to Bybit:', error);
    return false;
  }
}