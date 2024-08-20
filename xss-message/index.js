import express from 'express';
import path from 'path';
import axios from 'axios';
import querystring from 'querystring';
import puppeteer from 'puppeteer';
import cookieParser from 'cookie-parser'
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);


const app = express();
const port = 3010;
const servicehost = 'localhost:3010';

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'static')));
app.use(cookieParser());

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

const message = [];
const sleep = (t) => new Promise(resolve => setTimeout(resolve, t));

app.get('/', (req, res) => {
    res.render('index', {message: message});
});

app.post('/submit-question', async (req, res) => {
    const question = req.body.question;
    const pattern = /(img|script|svg)/i;

    if(question.match(pattern)){
        message.push({
            text: "XSS Detected!!",
            timestamp: new Date().toDateString() + ' ' + new Date().toTimeString().split(' ')[0]
        })
        return res.redirect('/');
    }

    message.push({ 
        text: "Admin get your feedback.",
        timestamp: new Date().toDateString() + ' ' + new Date().toTimeString().split(' ')[0]
    });

    const fullUrl = req.protocol + '://' + req.get('host') + "/adminLookup/?payload=" + encodeURIComponent(question);
    try {
        await axios.post(`http://${servicehost}/preview`, querystring.stringify({ url: fullUrl }));
    } catch (error) {
        console.error('Error making POST request:', error);
        return res.status(500).send('Error making POST request');
    }
    
    return res.redirect('/');
});

app.get('/adminLookup', (req, res) => {
    if (req.cookies.admin === '15b962711bba612357991b3a4441099a2afd4660b') {
        console.log('ok')
        const message = {
            text: req.query.payload,
            timestamp: new Date().toDateString() + ' ' + new Date().toTimeString().split(' ')[0]
        }
        res.cookie('hint', 'flag is in /aN4n9M0us_flag response',{
            secure: false,
            path: '/',
            sameSite: 'lax'
        });
        return res.render('backdoor', { message: message })
    }
    else {
        return res.status(403).send('Forbidden: Hacker!!');
    }
});

app.post('/preview', async (req, res) => {
    const url = req.body.url;
    if (!url) return res.status(400).send('Please provide a URL to preview');
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', "--disable-gpu"],
        executablePath: "/usr/bin/chromium-browser",
    });
    try {
        const page = await browser.newPage();
        await sleep(1000);
        await page.setCookie({
            name: 'admin',
            value: '15b962711bba612357991b3a4441099a2afd4660b',
            domain: 'localhost:3010',
            httpOnly: true
        });
        await sleep(1000);
        await page.goto(url);
        await sleep(3000);
        await page.close();
        await browser.close();
    } catch (error) {
        console.error('Error generating preview:', error);
        return res.status(500).send('Error generating preview');
    } finally {
        if (browser) await browser.close();
    }
    return res.sendStatus(200);
});

app.get('/aN4n9M0us_flag', (req, res) => {
    if (req.cookies.admin === '15b962711bba612357991b3a4441099a2afd4660b') {
        message.pop();
        message.push({
            text: "YOU GET FALG!! If you don't get the flag, try more time.",
            timestamp: new Date().toDateString() + ' ' + new Date().toTimeString().split(' ')[0]
        })
        return res.status(200).send(process.env.FLAG);
    }
    else{
        return res.status(403).send('Admin only');
    }
});


app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
