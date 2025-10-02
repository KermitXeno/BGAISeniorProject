import React from 'react'

const VueDemo: React.FC = () => {
  return (
    <div className="animate-fade-in">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-8 text-center">
          Vue.js Integration Demo
        </h1>
        
        <div className="card mb-8">
          <h2 className="text-2xl font-semibold mb-4">Coming Soon!</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            This section will demonstrate Vue.js components integrated within the React application.
            The hybrid approach allows you to leverage both frameworks' strengths in a single project.
          </p>
          
          <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
            <div className="flex items-center mb-2">
              <span className="text-yellow-600 dark:text-yellow-400 text-xl mr-2">⚠️</span>
              <h3 className="font-semibold text-yellow-800 dark:text-yellow-200">Development Note</h3>
            </div>
            <p className="text-yellow-700 dark:text-yellow-300 text-sm">
              Vue.js components will be integrated here using micro-frontends approach or 
              dynamic imports to showcase the hybrid nature of this application.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="card">
            <h3 className="text-xl font-semibold mb-4 text-green-600">Vue.js Benefits</h3>
            <ul className="space-y-2">
              <li className="flex items-start">
                <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>Progressive framework approach</span>
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>Gentle learning curve</span>
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>Excellent documentation</span>
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>Template-based syntax</span>
              </li>
            </ul>
          </div>

          <div className="card">
            <h3 className="text-xl font-semibold mb-4 text-blue-600">React Benefits</h3>
            <ul className="space-y-2">
              <li className="flex items-start">
                <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>Large ecosystem</span>
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>JSX flexibility</span>
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>Strong TypeScript support</span>
              </li>
              <li className="flex items-start">
                <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                <span>Mature tooling</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VueDemo