# Mnemos

A modern hybrid web and mobile application built with React and Vue.js.

## Features

- 🚀 **Fast Development** - Built with Vite for lightning-fast development
- ⚛️ **React & Vue.js** - Hybrid approach combining both frameworks
- 📱 **Mobile Ready** - Capacitor integration for native mobile apps
- 🎨 **Modern UI** - Tailwind CSS for beautiful, responsive designs
- 🔧 **TypeScript** - Full type safety and modern development experience
- 🔍 **ESLint** - Code linting for consistent code quality

## Tech Stack

- **Frontend Frameworks**: React 18, Vue.js 3
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Mobile**: Capacitor
- **Routing**: React Router (React), Vue Router (Vue)
- **HTTP Client**: Axios

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn package manager

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Mnemos
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy the environment file:
   ```bash
   cp .env.example .env.local
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open your browser and navigate to `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint issues
- `npm test` - Run tests
- `npm run test:coverage` - Run tests with coverage

## Mobile Development

### Setup Capacitor

1. Build the web app:
   ```bash
   npm run build
   ```

2. Initialize Capacitor (first time only):
   ```bash
   npx cap init
   ```

3. Add mobile platforms:
   ```bash
   npx cap add ios
   npx cap add android
   ```

4. Sync the web app to mobile:
   ```bash
   npm run mobile:build
   ```

5. Open in native IDE:
   ```bash
   npx cap open ios
   npx cap open android
   ```

## Project Structure

```
src/
├── components/        # Reusable React components
├── views/            # Page components
├── hooks/            # Custom React hooks
├── utils/            # Utility functions
├── assets/           # Static assets
└── stores/           # State management (future)

public/               # Static public assets
```

## Architecture

This project uses a hybrid approach where:
- **React** serves as the primary framework for the main application
- **Vue.js** components can be integrated as micro-frontends or embedded components
- **Vite** handles the build process and supports both frameworks
- **Capacitor** provides native mobile capabilities

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Project Link: [https://github.com/yourusername/mnemos](https://github.com/yourusername/mnemos)




# commands to run project


npm run dev - Development server (already running)
npm run build - Build for production
npm run preview - Preview production build
npm run lint - Check code quality
npm run test - Run tests
npm run mobile:build - Prepare for mobile deployment