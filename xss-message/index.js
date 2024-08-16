import express from 'express';
import path from 'path';
import axios from 'axios';
import querystring from 'querystring';
import puppeteer from 'puppeteer';
import cookieParser from 'cookie-parser'

const app = express();
const port = 3010;
const servicehost = 'localhost:3010';

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'static')));
app.use(cookieParser());

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

const message = []

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
        text: question,
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
    try {
        const browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();
        await page.setCookie({
            name: 'admin',
            value: '15b962711bba612357991b3a4441099a2afd4660b',
            domain: 'localhost:3010',
            httpOnly: true
        });
        await page.goto(url, { waitUntil: ['domcontentloaded', 'networkidle2']});
        await new Promise(resolve => setTimeout(resolve, 2000));
        await page.close();
        await browser.close();
    } catch (error) {
        console.error('Error generating preview:', error);
        return res.status(500).send('Error generating preview');
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
        return res.status(200).send('flag{fake}');
    }
    else{
        return res.status(403).send('Admin only');
    }
});


app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
