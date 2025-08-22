# Web Console Usage

## Starting the Web Console

1. Install dependencies:
```bash
npm install
```

2. Start the server:
```bash
npm start
```

3. Open your browser and navigate to:
```
http://localhost:3000
```

## Features

- **File Listing**: View all files in the `pages/` directory with metadata (size, modification date)
- **File Deletion**: Delete files through the web interface with confirmation dialogs
- **Real-time Updates**: File list automatically refreshes after operations
- **Security**: Path traversal protection ensures files can only be deleted within the project directory

## API Endpoints

- `GET /api/files` - List all files in the pages directory
- `DELETE /api/files/*` - Delete a specific file (e.g., `DELETE /api/files/pages/index.html`)

## Security Features

- Path validation prevents access to files outside the project directory
- Confirmation dialogs prevent accidental deletions
- Error handling for missing files and permission issues

## Screenshots

The web console provides a clean, modern interface for file management:

![Web Console Interface](https://github.com/user-attachments/assets/80b80027-c394-4bbb-ba8c-6e5364475db0)

After successful deletion:

![After File Deletion](https://github.com/user-attachments/assets/c6725048-ef4c-4441-871f-b1a1a6cc2dbb)