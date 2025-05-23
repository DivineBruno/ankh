import NextAuth from "next-auth";
import Resend from "next-auth/providers/resend";
import GoogleProvider from "next-auth/providers/google";
import { MongoDBAdapter } from "@auth/mongodb-adapter";
import clientPromise from "@/libs/mongo";

const config = {
    providers: [
        Resend({
        apiKey: process.env.RESEND_API_KEY,
        from: "noreply@resend.brunochasqueira.com",
        name: "Email"
        }),
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET,
        }),
    ],
    adapter: MongoDBAdapter(clientPromise),
     };
    
     export const { handlers, signIn, signOut, auth } = NextAuth(config);