import React from 'react'

const Data: React.FC = () => {
  return (
      <div className="animate-fade-in">
      <div className="max-w-4xl mx-auto">

      <h1 className="text-2xl font-semibold mb-4">Our Data, Your Health</h1>
          <main>
              <h2>Our Models</h2>
                  <div className="w-full max-w-4xl bg-white shadow rounded p-4">
                      <img src="/src/assets/confusion_matrix.png" alt="Age Distribution"
                           className="w-full h-auto rounded"/>
                  </div>
              <h2>Demographics of Our Data</h2>
              <div className="flex flex-col gap-6 p-4 items-center">
                  <div className="w-full max-w-4xl bg-white shadow rounded p-4">
                      <img src="/src/assets/age_distribution.png" alt="Age Distribution"
                           className="w-full h-auto rounded"/>
                  </div>
                  <div className="w-full max-w-4xl bg-white shadow rounded p-4">
                      <img src="/src/assets/sex_distribution.png" alt="Graph 2" className="w-full h-auto rounded"/>
                  </div>
                  <div className="w-full max-w-4xl bg-white shadow rounded p-4">
                      <img src="/src/assets/edu_distribution.png" alt="Graph 3" className="w-full h-auto rounded"/>
                  </div>
              </div>
              <div className="w-full max-w-4xl bg-white shadow rounded p-4">
                      <img src="/src/assets/ses_distribution.png" alt="Graph 4" className="w-full h-auto rounded"/>
                  </div>
                  <div className="w-full max-w-4xl bg-white shadow rounded p-4">
                      <img src="/src/assets/mmse_distribution.png" alt="Graph 4" className="w-full h-auto rounded"/>
                  </div>
                  <div className="w-full max-w-4xl bg-white shadow rounded p-4">
                      <img src="/src/assets/asf_distribution.png" alt="Graph 4" className="w-full h-auto rounded"/>
                  </div>
                  <div className="w-full max-w-4xl bg-white shadow rounded p-4">
                      <img src="/src/assets/etiv_distribution.png" alt="Graph 4" className="w-full h-auto rounded"/>
                  </div>
                                    <div className="w-full max-w-4xl bg-white shadow rounded p-4">
                      <img src="/src/assets/nwbv_distribution.png" alt="Graph 4" className="w-full h-auto rounded"/>
              </div>

          </main>
      </div>

      </div>
  )
}

export default Data