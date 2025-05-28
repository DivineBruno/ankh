import { NextApiRequest, NextApiResponse } from 'next';
import { TradingEngine } from '@/src/bot/TradingEngine';

const engine = new TradingEngine(
  process.env.BYBIT_API_KEY!,
  process.env.BYBIT_API_SECRET!
);

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'POST') {
    try {
      switch(req.body.action) {
        case 'loadStrategy':
          await engine.loadStrategyFromSheet(req.body.sheetId);
          res.status(200).json({ message: 'Strategy loaded successfully' });
          break;
        
        case 'startTrading':
          await engine.executeTrades();
          res.status(200).json({ message: 'Trading started' });
          break;
          
        default:
          res.status(400).json({ error: 'Invalid action' });
      }
    } catch (error) {
      res.status(500).json({ error: 'Internal server error' });
    }
  }
}
