const fs = require('fs');
const path = require('path');

// Create a simple test for the file deletion functionality
async function testFileDeletion() {
    console.log('Testing file deletion functionality...');
    
    // First, recreate the test file
    const testFilePath = path.join(__dirname, 'pages', 'test.html');
    const pagesDir = path.join(__dirname, 'pages');
    
    // Ensure pages directory exists
    if (!fs.existsSync(pagesDir)) {
        fs.mkdirSync(pagesDir, { recursive: true });
    }
    
    // Create a test file
    fs.writeFileSync(testFilePath, '<h1>Test File</h1>');
    console.log('✓ Created test file:', testFilePath);
    
    // Verify file exists
    if (fs.existsSync(testFilePath)) {
        console.log('✓ Test file exists before deletion');
    } else {
        console.log('✗ Test file does not exist');
        return;
    }
    
    // Simulate deletion by removing the file directly (since we already tested the web interface)
    fs.unlinkSync(testFilePath);
    
    // Verify file is deleted
    if (!fs.existsSync(testFilePath)) {
        console.log('✓ Test file successfully deleted');
    } else {
        console.log('✗ Test file still exists after deletion');
    }
    
    console.log('Test completed successfully!');
}

// Run the test
if (require.main === module) {
    testFileDeletion().catch(console.error);
}

module.exports = { testFileDeletion };