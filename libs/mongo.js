import { MongoClient, ServerApiVersion } from 'mongodb';

    if (!process.env.MONGO_URI) {
        throw new Error('MONGO_URI is not defined in the environment variables');
    }
    const uri = process.env.MONGO_URI;
    const options = {
        serverApi: {
            version: ServerApiVersion.v1,
            strict: true,
            deprecationErrors: true,
        },
    };
    let client;
    let clientPromise;

    if (process.env.NODE_ENV === 'development') {
       let globalWithMongo = global;
       globalWithMongo._mongoClientPromise = undefined;
        // Prevents creating a new client on every reload in development mode 
     
        if (!globalWithMongo._mongoClientPromise) {
            client = new MongoClient(uri, options);
            globalWithMongo._mongoClientPromise = client.connect();
        }
        clientPromise = globalWithMongo._mongoClientPromise;
    } else {
        client = new MongoClient(uri, options);
        clientPromise = client.connect();
    }

    export default clientPromise