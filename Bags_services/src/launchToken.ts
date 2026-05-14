import dotenv from "dotenv";
dotenv.config({ path: "../.env" });

import { Connection, Keypair, LAMPORTS_PER_SOL } from "@solana/web3.js";
import bs58 from "bs58";

type LaunchRequest = {
  name?: string;
  symbol?: string;
  description?: string;
  imageUrl?: string;
  initialBuyLamports?: number;
};

export async function launchEcoVerseToken(body: LaunchRequest = {}) {
  const apiKey = process.env.BAGS_API_KEY;
  const rpcUrl = process.env.SOLANA_RPC_URL;
  const privateKey = process.env.PRIVATE_KEY || process.env.SOLANA_PRIVATE_KEY;

  if (!apiKey) throw new Error("Missing BAGS_API_KEY");
  if (!rpcUrl) throw new Error("Missing SOLANA_RPC_URL");
  if (!privateKey) throw new Error("Missing PRIVATE_KEY or SOLANA_PRIVATE_KEY");

  const wallet = Keypair.fromSecretKey(bs58.decode(privateKey));
  const connection = new Connection(rpcUrl, "confirmed");

  const balanceLamports = await connection.getBalance(wallet.publicKey);
  const balanceSol = balanceLamports / LAMPORTS_PER_SOL;

  const tokenConfig = {
    name: body.name || process.env.ECOVERSE_TOKEN_NAME || "EcoVerse",
    symbol: body.symbol || process.env.ECOVERSE_TOKEN_SYMBOL || "ECO",
    description:
      body.description ||
      process.env.ECOVERSE_TOKEN_DESCRIPTION ||
      "Organic waste recycling reward token for EcoVerse",
    imageUrl: body.imageUrl || process.env.ECOVERSE_TOKEN_IMAGE_URL,
    initialBuyLamports:
      body.initialBuyLamports ||
      Number(process.env.ECOVERSE_INITIAL_BUY_LAMPORTS || 10000000),
  };

  const requiredSol = 0.05;

  if (balanceSol < requiredSol) {
    return {
      status: "PENDING_FUNDING",
      message: "Wallet is connected, but needs SOL before token launch.",
      wallet: wallet.publicKey.toBase58(),
      balanceSol,
      requiredSol,
      tokenConfig,
      nextStep: `Fund this wallet with at least ${requiredSol} SOL, then retry launch.`,
    };
  }

  return {
    status: "READY_TO_LAUNCH",
    message: "Wallet funded. Ready to call Bags launch transaction.",
    wallet: wallet.publicKey.toBase58(),
    balanceSol,
    tokenConfig,
  };
}