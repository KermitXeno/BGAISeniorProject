import React from 'react'

const About: React.FC = () => {
  return (
    <div className="animate-fade-in">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-8 text-center">
          About Mnemos
        </h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
          <div>
            <h2 className="text-2xl font-semibold mb-4">What is Mnemos?</h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Mnemos is a cutting-edge hybrid application that combines the best of both React and Vue.js 
              ecosystems. Built with modern development practices in mind, it provides a solid foundation 
              for creating responsive web and mobile applications.
            </p>
            <p className="text-gray-600 dark:text-gray-300">
              The project leverages Vite for lightning-fast development, TypeScript for type safety, 
              and Tailwind CSS for beautiful, responsive designs.
            </p>
          </div>
          <div className="bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-800 dark:to-primary-900 p-8 rounded-lg">
            <h3 className="text-xl font-semibold mb-4">Key Features</h3>
            <ul className="space-y-2">
              <li className="flex items-center">
                <span className="w-2 h-2 bg-primary-600 rounded-full mr-3"></span>
                React & Vue.js Integration
              </li>
              <li className="flex items-center">
                <span className="w-2 h-2 bg-primary-600 rounded-full mr-3"></span>
                Mobile-First Design
              </li>
              <li className="flex items-center">
                <span className="w-2 h-2 bg-primary-600 rounded-full mr-3"></span>
                TypeScript Support
              </li>
              <li className="flex items-center">
                <span className="w-2 h-2 bg-primary-600 rounded-full mr-3"></span>
                Capacitor Integration
              </li>
              <li className="flex items-center">
                <span className="w-2 h-2 bg-primary-600 rounded-full mr-3"></span>
                Modern Build Tools
              </li>
            </ul>
          </div>
        </div>

        <div className="bg-gray-50 dark:bg-gray-800 p-8 rounded-lg">
          <h2 className="text-2xl font-semibold mb-6 text-center">Technology Stack</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div>
              <div className="text-blue-600 text-2xl mb-2">⚛️</div>
              <h3 className="font-semibold">React</h3>
              <p className="text-sm text-gray-600 dark:text-gray-300">UI Framework</p>
            </div>
            <div>
              <div className="text-green-600 text-2xl mb-2">🟢</div>
              <h3 className="font-semibold">Vue.js</h3>
              <p className="text-sm text-gray-600 dark:text-gray-300">Progressive Framework</p>
            </div>
            <div>
              <div className="text-purple-600 text-2xl mb-2">⚡</div>
              <h3 className="font-semibold">Vite</h3>
              <p className="text-sm text-gray-600 dark:text-gray-300">Build Tool</p>
            </div>
            <div>
              <div className="text-blue-500 text-2xl mb-2">🎨</div>
              <h3 className="font-semibold">Tailwind</h3>
              <p className="text-sm text-gray-600 dark:text-gray-300">CSS Framework</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default About