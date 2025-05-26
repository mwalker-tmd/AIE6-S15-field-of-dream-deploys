# Frontend Documentation

This document provides an overview of the frontend architecture and components for the AI Maker Space project.

## Project Structure

```
frontend/
├── public/           # Static assets
├── src/              # Source code
│   ├── components/   # React components
│   ├── utils/        # Utility functions
│   ├── App.jsx       # Main application component
│   ├── App.css       # Application styles
│   ├── index.css     # Global styles
│   └── main.jsx      # Application entry point
├── .env              # Environment variables (not in repo)
├── index.html        # HTML template
├── package.json      # Dependencies and scripts
└── vite.config.js    # Vite configuration
```

## Core Components

### App Component

The `App.jsx` component serves as the main container for the application. It manages:

- Application state for file upload status
- Conditional rendering of components based on application state
- Overall layout and structure

### FileUploader Component

The `FileUploader.jsx` component handles:

- File selection via input element
- File upload to the backend API
- Upload status feedback
- Success callback to trigger chat mode

### ChatBox Component

The `ChatBox.jsx` component provides:

- Text input for questions
- API endpoint selection (RAG or Agent)
- Streaming response handling
- Response display

## Environment Configuration

The application uses environment variables for configuration. See `.env.template` for required variables:

- `VITE_API_URL` - URL of the backend API (defaults to http://localhost:7860)

## Development Setup

1. Clone the repository
2. Create a `.env` file based on `.env.template`
3. Install dependencies:
   ```
   npm install
   ```
4. Run the development server:
   ```
   npm run dev
   ```

## Building for Production

To build the application for production:

```
npm run build
```

This will generate optimized static files in the `dist` directory.

## Customization Points

The template includes several TODO comments indicating areas for customization:

1. **Branding**: Replace the logo and application title in `App.jsx`
2. **FileUploader**: Customize or replace the file upload component
3. **ChatBox**: Modify the chat interface to match your specific use case
4. **API Endpoints**: Update the API endpoints in the components to match your backend

## API Integration

The frontend communicates with the backend through the following endpoints:

- `POST /upload` - Upload documents for processing
- `POST /ask` - Query the knowledge base
- `POST /agent` - Execute an agent

## Styling

The application uses CSS for styling:

- `App.css` - Component-specific styles
- `index.css` - Global styles and CSS variables

## Testing

The application includes data-testid attributes for testing purposes. You can use these with testing libraries like React Testing Library.

## Architecture Notes

- The application uses React 19 with Vite for fast development
- Components are functional and use React hooks for state management
- The application supports streaming responses from the backend
- The UI adapts based on whether a file has been uploaded 