const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync } = require('child_process');

const VERSION = 'v0.1.0';
const REPO = 'HashimCodeDev/treetouch';

const PLATFORM_MAP = {
    win32: 'treetouch-win.exe',
    darwin: 'treetouch-macos',
    linux: 'treetouch-linux'
};

const platform = process.platform;
const assetName = PLATFORM_MAP[platform];

if (!assetName) {
    console.error(`Unsupported platform: ${platform}`);
    process.exit(1);
}

const url = `https://github.com/${REPO}/releases/download/${VERSION}/${assetName}`;
const dir = path.join(__dirname, 'bin');
const filePath = path.join(dir, platform === 'win32' ? 'treetouch.exe' : 'treetouch');

if (!fs.existsSync(dir)) fs.mkdirSync(dir);

console.log(`Downloading ${assetName} from ${url}...`);

https.get(url, (res) => {
    if (res.statusCode === 302) {
        https.get(res.headers.location, (redirectRes) => {
            redirectRes.pipe(fs.createWriteStream(filePath)).on('finish', () => {
                if (platform !== 'win32') {
                    execSync(`chmod +x ${filePath}`);
                }
                console.log('Download complete.');
            });
        });
    } else if (res.statusCode === 200) {
        res.pipe(fs.createWriteStream(filePath)).on('finish', () => {
            if (platform !== 'win32') {
                execSync(`chmod +x ${filePath}`);
            }
            console.log('Download complete.');
        });
    } else {
        console.error(`Failed to download binary; status code: ${res.statusCode}`);
        process.exit(1);
    }
}).on('error', (err) => {
    console.error('Error downloading:', err.message);
    process.exit(1);
});
