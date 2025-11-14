import { useState } from "react";

type Props = {
  slides: string[];
};

export default function Slideshow({ slides }: Props) {
  const [index, setIndex] = useState(0);

  function next() {
    setIndex((index + 1) % slides.length);
  }

  function prev() {
    setIndex((index - 1 + slides.length) % slides.length);
  }

  return (
    <div className="relative w-full flex items-center justify-center">
        <img
          src={slides[index]}
          className="w-full h-auto rounded"
        />

      <button
        style={{ position: "absolute", top: "50%", left: 0 }}
        onClick={prev}
        className="absolute left-0 top-1/2 -translate-y-1/2 text-4xl px-4 py-2"
      >
        ❮
      </button>
      <button
        style={{ position: "absolute", top: "50%", right: 0 }}
        onClick={next}
        className="absolute right-0 top-1/2 -translate-y-1/2 text-4xl px-4 py-2"
      >
        ❯
      </button>
    </div>
  );
}
