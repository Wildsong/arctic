import { ApolloServer } from '@apollo/server'
import { expressMiddleware } from '@apollo/server/express4'
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer'
import express from 'express'
import http from 'http'
import cors from 'cors'
import bodyParser from 'body-parser'
import { makeExecutableSchema } from '@graphql-tools/schema';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { typeDefs, resolvers } from './schema.js'

const THIS_HOST="cc-gislicense"; // Normally "localhost" is fine here
const PORT=4000;
const ROUTE='/api'; // Normally for both HTTP and WS

const app = express();
const httpServer = http.createServer(app);
const schema = makeExecutableSchema({ typeDefs, resolvers });
const wsServer = new WebSocketServer({
    server: httpServer,
//    path: ROUTE, // default; the sandbox stops working if you define this differently
});
const serverCleanup = useServer({ schema }, wsServer); // Start listening on websocket
const apolloserver = new ApolloServer({
    schema,
    plugins: [
        ApolloServerPluginDrainHttpServer({ httpServer }), // this is supposed to provide a clean shutdown
        { // WebSocket shutdown
            async serverWillStart() {
                return {
                    async drainServer() {
                        await serverCleanup.dispose();
                    }
                }
            }
        }
    ]
});
await apolloserver.start();

app.get('/', (req,res)=> {
    let content = '<h1>flexlm api landing page</h1>    \
        <a href="/api">api</a> <br/>      \
    ';
    res.send(content);
});

app.use(
    ROUTE, // "http://THIS_HOST:PORT/ROUTE/"

    // https://www.apollographql.com/docs/apollo-server/security/cors/#specifying-origins
    cors(), // allow everything for now
//  cors({
//        origin: [
//            'https://records.clatsopcounty.gov', // in production
//            'http://localhost:8080', // in development
//        ],
//    }),

    bodyParser.json(),
    // or maybe it should be 
    // express.json(),

    // takes an optional context function, see https://www.apollographql.com/docs/apollo-server/data/context/#the-context-function
    expressMiddleware(apolloserver),
);

httpServer.listen(PORT, () => {
    console.log(`Server ready http://${THIS_HOST}:${PORT}${ROUTE}`);
});
