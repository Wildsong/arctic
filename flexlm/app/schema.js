/*
    schema.js

    GraphQL typeDefs and Resolvers
*/
import { spawn } from 'node:child_process';
import DataSource from './datasource.js';
import fs from "node:fs/promises";
import TailFile from '@logdna/tail-file';
const LOGFILE = "C:/srv/logs/lmgrd9.log";

const ac = new AbortController();
const { signal } = ac;
setTimeout(() => ac.abort(), 10000);

const datasource = new DataSource({});

export const typeDefs = `#graphql
    type Ping {
        timestamp: String
        version: String
    }

    # The "Query" type lists all of the available queries that
    # clients can execute, along with the return type for each.
    type Query { 
        ping: Ping
        log: [String] 
        lmstat: [String]
    }

    type Subscription {
        hello: String
        newLogEntry: String
    }
`;

export const resolvers = {
    Query: { 
        ping : () => {
            const t = new Date().toLocaleString('en-US',{timezone:'PST'}); 
            return {
                timestamp: t,
                version: process.env.npm_package_version
            };
        },

        log: () => {
            datasource.watchLogFile();
            return ['Roger that']; //datasource.readLogFile();
        },

        lmstat: async () => {
            let rawdata = '';
            // using a BAT file
            const lmstat = spawn('cmd', ['/c', 'lmstat.bat']);
            // Direct invocation does not work
//            const lmstat = spawn('bin/lmutil.exe', ['lmstat', '-c', 'C:\\srv\\service.txt', '-a'])
            for await (const chunk of lmstat.stdout) {
                rawdata += chunk;
            }
            lmstat.stderr.on('data', (data) => {
                console.log(data.toString());
            });
            lmstat.on('close', (code) => {
                console.log(`lmstat exit code ${code}`);
            });
            let rval = [];
            for (const line of rawdata.toString().split('\r\n')) {
                if (line != "") {
                    rval.push(line);
                }
            }
            return rval;
        }
    },
    Subscription: {
        hello: {
            subscribe: async function* () { // function* is a generator function.
                for await (const word of ['Hello', 'Bonjour', 'Ciao']) {
                    yield { hello: word };
                }
            }
        },
        newLogEntry: {
            subscribe: async () => {
                const tf = new TailFile(LOGFILE, {encoding:'utf8'})
                    .on('data', (chunk)=>{
                        console.log(chunk)
                    })
                    .on('tail_error', (err) => {
                        console.error('TailFile had an error!', err)
                    })
                    .on('error', (err) => {
                        console.error('TailFile stream error ', err)
                    })
                    .start()
                    .catch((err) => {
                        console.error('Cannot start.  Does the file exist?', err)
                    })
            }
        },
    }
};

