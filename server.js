const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// API Routes

// Get list of files in pages directory
app.get('/api/files', (req, res) => {
    try {
        const pagesDir = path.join(__dirname, 'pages');
        if (!fs.existsSync(pagesDir)) {
            return res.json({ files: [] });
        }
        
        const files = fs.readdirSync(pagesDir).map(file => {
            const filePath = path.join(pagesDir, file);
            const stats = fs.statSync(filePath);
            return {
                name: file,
                path: `/pages/${file}`,
                size: stats.size,
                modified: stats.mtime
            };
        });
        
        res.json({ files });
    } catch (error) {
        res.status(500).json({ error: 'Failed to read files', message: error.message });
    }
});

// Delete a file
app.delete('/api/files/*', (req, res) => {
    try {
        // Get the file path from the URL, remove the /api/files prefix
        const filePath = req.path.replace('/api/files', '');
        const absolutePath = path.join(__dirname, filePath);
        
        // Security check: ensure the file is within our project directory
        const resolvedPath = path.resolve(absolutePath);
        const projectRoot = path.resolve(__dirname);
        
        if (!resolvedPath.startsWith(projectRoot)) {
            return res.status(403).json({ error: 'Access denied: Path outside project directory' });
        }
        
        // Check if file exists
        if (!fs.existsSync(resolvedPath)) {
            return res.status(404).json({ error: 'File not found' });
        }
        
        // Delete the file
        fs.unlinkSync(resolvedPath);
        
        res.json({ 
            success: true, 
            message: `File ${filePath} deleted successfully`,
            deletedFile: filePath
        });
        
    } catch (error) {
        res.status(500).json({ 
            error: 'Failed to delete file', 
            message: error.message 
        });
    }
});

// Serve the web console
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'console.html'));
});

// Start server
app.listen(PORT, () => {
    console.log(`Web console running at http://localhost:${PORT}`);
    console.log('Open the URL in your browser to access the file management console');
});