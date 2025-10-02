import React from 'react';
import { useNavigate } from 'react-router-dom';
const Header: React.FC = () => {
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);
 
  const handleGetStarted = () => {
    navigate('/create-account');
  };
  const handleSignIn = () => {
    navigate('/signin');
  };
  return (
    <header className="bg-background shadow-primary border-b border-secondary-200/30">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo/Brand */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">M</span>
            </div>
            <h1 className="text-xl font-bold text-gradient-primary">
              Mnemos
            </h1>
          </div>
          
          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <a 
              href="/" 
              className="text-text-primary hover:text-primary-500 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            >
              Home
            </a>
            <a 
              href="/about" 
              className="text-text-primary hover:text-primary-500 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            >
              About
            </a>
      
            <a  href="/chat" className="text-text-primary hover:text-primary-500 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
              Chat
            </a>
          </div>
          
          {/* CTA Button */}
          <div className="hidden md:flex items-center space-x-4">
            <button className="btn-outline btn-sm" onClick={handleSignIn}>
              Sign In
            </button>
            <button className="btn-primary btn-sm" onClick={handleGetStarted}>
              Get Started
            </button>
          </div>
          
          {/* Mobile menu button */}
          <div className="md:hidden">
                        <button 
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="text-slate-700 hover:text-primary-500 p-2 rounded-md transition-colors duration-200"
              aria-label="Toggle mobile menu"
            >
              <svg 
                className={`w-6 h-6 transform transition-transform duration-200 ${isMobileMenuOpen ? 'rotate-90' : ''}`} 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                {isMobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

                {/* Mobile Menu */}
        <div className={`md:hidden transition-all duration-300 ease-in-out ${
          isMobileMenuOpen 
            ? 'max-h-80 opacity-100 pb-4' 
            : 'max-h-0 opacity-0 overflow-hidden'
        }`}>
          <div className="px-2 pt-2 pb-3 space-y-1 bg-background rounded-lg shadow-lg border border-secondary-200/30 mt-2">
            <a
              href="/"
              className="block px-3 py-2 rounded-md text-base font-medium text-slate-700 hover:text-primary-500 hover:bg-secondary-50 transition-all duration-200"
            >
              Home
            </a>
            <a
              href="/about"
              className="block px-3 py-2 rounded-md text-base font-medium text-slate-700 hover:text-primary-500 hover:bg-secondary-50 transition-all duration-200"
            >
              About
            </a>
            <a
              href="/chat"
              className="block px-3 py-2 rounded-md text-base font-medium text-slate-700 hover:text-primary-500 hover:bg-secondary-50 transition-all duration-200"
            >
              Chat
            </a>
             {/* Mobile CTA Buttons */}
            <div className="pt-4 space-y-2 border-t border-secondary-200/30">
              <button 
                onClick={handleSignIn}
                className="w-full btn-outline btn-md"
              >
                Sign In
              </button>
              <button 
                onClick={handleGetStarted}
                className="w-full btn-primary btn-md shadow-primary flex items-center justify-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
                <span>Get Started</span>
              </button>
            </div>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;