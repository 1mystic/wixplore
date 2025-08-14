# Vue Frontend for Cultural Explorer

This is the frontend application for the Cultural Explorer project, built with Vue 3 and designed to work with a Flask backend.

## Project Setup

```bash
# Install dependencies
npm install

# Serve with hot reload at localhost:8080
npm run serve

# Build for production
npm run build
```

## Project Structure

- `src/` - Source files
  - `components/` - Vue components
  - `views/` - Page components
  - `router/` - Vue Router configuration
  - `store/` - Vuex store
  - `assets/` - Static assets
- `public/` - Public static files
- `dist/` - Built files (generated)

## Development

1. The development server runs on port 8080 by default
2. API requests are proxied to the Flask backend (http://localhost:5000)
3. Hot reload is enabled for development

## Building for Production

1. Run `npm run build`
2. The built files will be in the `dist` directory
3. These files are automatically copied to the Flask template directory

## Integration with Flask

The built files are automatically placed in the Flask template directory (`../vuefronttest/dist`). The Flask backend should be configured to serve these files as static assets and use the `index.html` as the template.

## Dependencies

- Vue 3
- Vue Router 4
- Vuex 4
- Bootstrap 5
- Chart.js
- Marked (for markdown rendering) 