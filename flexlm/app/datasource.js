import fs from "node:fs/promises";
const LOGFILE = "C:/srv/logs/lmgrd9.log";

//const ac = new AbortController();
//const { signal } = ac;
//setTimeout(() => ac.abort(), 60000);

class DataSource {
    constructor() {

    }

    // read the entire log file and return it in one go
    async readLogFile() {
        let fp = await fs.open(LOGFILE);
        let rval = [];
        for await (const line of fp.readLines()) {
            rval.push(line);
        };
        return rval;
    }


    async watchLogFile() {
        console.log(`Watching ${LOGFILE}`)
        try {
            const watcher = fs.watch(LOGFILE);
            for await (const event of watcher) {
                console.log(event);
            }
        } catch (err) {
            console.log('ABORT ABORT ABORT', err)
            //throw err;
        }
    }

    async watchLogFilePrime() {
        fs.watchFile(filename, (curr, prev) => {
            if (filename) {
                if (curr.size.valueOf() === previousFileSize.valueOf())
                    return; // no change in file size
                let buffer = new Buffer.alloc(curr,size - lastByteRead + 1);
                
                previousFileSize = curr.size;
                console.log('file changed');

                fs.open(filename, fileOpenMode, (err, filedata) => {
                    if (err)
                        return console.error(err);
                    console.log("Reading file.");
                    fs.read(filedata, buffer, 0, buffer.length, lastReadByte, (err,bytes) => {
                        if (err)
                            return console.error(err);
                        if (bytes > 0) {
                            const dataString = buffer.slice(0,bytes).toString();
                            const dataArray = dataString.split("\n");
                            dataArray.forEach(logline => {
                                if (logline)
                                    console.log(logline);
                            })
                        }
                        lastReadByte = stats.size;
                        fs.close(filedata, (err) => {
                            if (err)
                                return console.error(err);
                            console.log("File closed.");
                        })
                    })
                })
            }
        })
    }

}
export default DataSource

