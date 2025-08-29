import React, { useEffect, useState } from "react";
import "./Loader.css";

const phrases = [
  "Scanning... █▒▒▒▒▒▒▒▒▒",
  "Bypassing firewall... ███▒▒▒▒▒",
  "Extracting data... █████▒▒▒▒",
  "Decrypting... ████████▒▒",
  "Access Granted ✔"
];

const glitchChars = ["@", "#", "%", "$", "0", "1", "X"];

const Loader = () => {
  const [displayText, setDisplayText] = useState("");
  const [phraseIndex, setPhraseIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);

  useEffect(() => {
    let typingInterval;

    if (phraseIndex < phrases.length) {
      typingInterval = setInterval(() => {
        const currentPhrase = phrases[phraseIndex];

        if (charIndex < currentPhrase.length) {
          const realChar = currentPhrase[charIndex];
          const glitch =
            Math.random() < 0.2
              ? glitchChars[Math.floor(Math.random() * glitchChars.length)]
              : realChar;

          setDisplayText((prev) => prev + glitch);
          setCharIndex((prev) => prev + 1);
        } else {
          clearInterval(typingInterval);
          setTimeout(() => {
            setPhraseIndex((prev) => prev + 1);
            setCharIndex(0);
            setDisplayText("");
          }, 1200);
        }
      }, 120);
    }

    return () => clearInterval(typingInterval);
  }, [charIndex, phraseIndex]);

  return (
    <div className="loader-wrapper">
      <div className="loader">
        {/* 🔹 10 rings */}
        <div className="ring"></div>
        <div className="ring"></div>
        <div className="ring"></div>
        <div className="ring"></div>
        <div className="ring"></div>
        <div className="ring"></div>
        <div className="ring"></div>
        <div className="ring"></div>
        <div className="ring"></div>
        <div className="ring"></div>
        <div className="typing-text">
          {displayText}
          <span className="cursor">█</span>
        </div>
      </div>
    </div>
  );
};

export default Loader;
