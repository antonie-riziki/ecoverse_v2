import dotenv from "dotenv";
dotenv.config({ path: "../.env" });

import { Connection, Keypair, PublicKey } from "@solana/web3.js";
import {
    getOrCreateAssociatedTokenAccount,
    transferChecked,
} from "@solana/spl-token";
import bs58 from "bs58";

type RewardRequest = {
    recipientWallet: string;
    amount: number;
    mintAddress: string;
    decimals?: number;
};

export async function sendEcoReward(body: RewardRequest) {
    const rpcUrl = process.env.SOLANA_RPC_URL;
    const privateKey = process.env.PRIVATE_KEY || process.env.SOLANA_PRIVATE_KEY;

    if (!rpcUrl) throw new Error("Missing SOLANA_RPC_URL");
    if (!privateKey) throw new Error("Missing PRIVATE_KEY or SOLANA_PRIVATE_KEY");

    if (!body.recipientWallet) throw new Error("recipientWallet is required");
    if (!body.amount) throw new Error("amount is required");
    if (!body.mintAddress) throw new Error("mintAddress is required");

    const decimals = body.decimals ?? 6;

    const connection = new Connection(rpcUrl, "confirmed");
    const payer = Keypair.fromSecretKey(bs58.decode(privateKey));

    const mint = new PublicKey(body.mintAddress);
    const recipient = new PublicKey(body.recipientWallet);

    const senderTokenAccount = await getOrCreateAssociatedTokenAccount(
        connection,
        payer,
        mint,
        payer.publicKey
    );

    const recipientTokenAccount = await getOrCreateAssociatedTokenAccount(
        connection,
        payer,
        mint,
        recipient
    );

    const rawAmount = BigInt(Math.floor(body.amount * 10 ** decimals));

    const signature = await transferChecked(
        connection,
        payer,
        senderTokenAccount.address,
        mint,
        recipientTokenAccount.address,
        payer,
        rawAmount,
        decimals
    );

    return {
        status: "REWARD_SENT",
        signature,
        mintAddress: mint.toBase58(),
        recipientWallet: recipient.toBase58(),
        amount: body.amount,
        decimals,
    };
}