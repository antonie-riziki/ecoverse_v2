import dotenv from "dotenv";
dotenv.config({ path: "../.env" });

import { Keypair, Connection, LAMPORTS_PER_SOL } from "@solana/web3.js";
import bs58 from "bs58";

const SOLANA_PRIVATE_KEY = process.env.SOLANA_PRIVATE_KEY;
const SOLANA_RPC_URL = process.env.SOLANA_RPC_URL;

if (!SOLANA_PRIVATE_KEY || !SOLANA_RPC_URL) {
    throw new Error("SOLANA_PRIVATE_KEY and SOLANA_RPC_URL are required in .env");
}

async function main() {
    const keypair = Keypair.fromSecretKey(bs58.decode(SOLANA_PRIVATE_KEY as string));
    const connection = new Connection(SOLANA_RPC_URL as string);

    const balance = await connection.getBalance(keypair.publicKey);

    console.log("Wallet:", keypair.publicKey.toBase58());
    console.log("Balance:", balance / LAMPORTS_PER_SOL, "SOL");
}

main().catch(console.error);