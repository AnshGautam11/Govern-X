import React, { useState, useEffect } from 'react';

function TypingEffect({ text, speed = 50 }) {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    if (displayedText.length < text.length && isTyping) {
      const timeout = setTimeout(() => {
        setDisplayedText(text.slice(0, displayedText.length + 1));
      }, speed);
      return () => clearTimeout(timeout);
    } else if (displayedText.length === text.length) {
      setIsTyping(false);
    }
  }, [displayedText, text, speed, isTyping]);

  return (
    <span className="typing-effect">
      {displayedText}
      {isTyping && <span className="cursor">▌</span>}
    </span>
  );
}

export default TypingEffect;
