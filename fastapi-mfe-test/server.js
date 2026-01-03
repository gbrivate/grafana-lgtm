const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 4200;
// Change 'my-app/browser' to match your actual dist folder structure
const DIST_PATH = path.join(__dirname, 'dist/fastapi-mfe-test/browser');

const server = http.createServer((req, res) => {
  // Determine the file path
  let filePath = path.join(DIST_PATH, req.url === '/' ? 'index.html' : req.url);

  // Get the file extension to set the correct Content-Type
  const extname = path.extname(filePath);
  let contentType = 'text/html';

  const mimeTypes = {
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.svg': 'image/svg+xml',
  };

  contentType = mimeTypes[extname] || 'text/html';

  // Try to read the file
  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        // FILE NOT FOUND: Serve index.html (Angular's Router handles the rest)
        fs.readFile(path.join(DIST_PATH, 'index.html'), (err, data) => {
          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end(data, 'utf-8');
        });
      } else {
        // Server error
        res.writeHead(500);
        res.end(`Server Error: ${error.code}`);
      }
    } else {
      // SUCCESS: Serve the requested file
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
});
