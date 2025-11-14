import React from 'react'
import Slideshow from "@components/slideshow.tsx";

const Data: React.FC = () => {

    const slides = [
        "/src/assets/age_distribution.png",
        "/src/assets/sex_distribution.png",
        "/src/assets/edu_distribution.png",
        "/src/assets/ses_distribution.png",
        "/src/assets/mmse_distribution.png",
        "/src/assets/asf_distribution.png",
        "/src/assets/etiv_distribution.png",
        "/src/assets/nwbv_distribution.png"
    ]

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
              <div>
                  <Slideshow slides={slides}></Slideshow>
                  </div>
      </main>
          </div>
          </div>
  );
}
export default Data