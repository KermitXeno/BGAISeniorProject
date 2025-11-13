import { useEffect, useState } from "react";

export default function AgePlot() {
  const [img, setImg] = useState("");

  useEffect(() => {
    fetch("/age-distribution")
      .then(res => res.json())
      .then(data => setImg(`data:image/png;base64,${data.image}`))
      .catch(console.error);
  }, []);

  return (
    <div className="flex justify-center mt-10">
      {img ? <img src={img} alt="Age Distribution" /> : <p>Loading...</p>}
    </div>
  );
};

