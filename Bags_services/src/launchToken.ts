import { BagsSDK } from "@bagsfm/bags-sdk";
import { Connection, Keypair } from "@solana/web3.js";
import bs58 from "bs58";
import dotenv from "dotenv";
import path from "path";

// Load environment variables from the root .env file
dotenv.config({ path: path.resolve(__dirname, "../../.env") });

export const launchToken = async () => {
  const apiKey = process.env.BAGS_API_KEY;
  const solanaAddress = process.env.SOLANA_ADDRESS;

  if (!apiKey) {
    throw new Error("BAGS_API_KEY is not defined in the environment variables.");
  }

  console.log("Initializing Bags SDK...");
  
  const connection = new Connection("https://api.mainnet-beta.solana.com", "confirmed");
  const sdk = new BagsSDK(apiKey, connection);

  console.log("SDK initialized successfully.");
  
  // Example: Log the Solana address from .env
  console.log("Target Solana Address:", solanaAddress);

  // Future implementation: Add token launch logic here
  // const result = await sdk.launchpad.launch({ ... });
  
  return sdk;
};

// If running directly
if (require.main === module) {
  launchToken().catch(console.error);
}
