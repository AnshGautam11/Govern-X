import { useState, useEffect } from 'react';
import TypingEffect from './TypingEffect';
import './TerminalMessages.css';

function TerminalMessages() {
  const messages = [
    'Scanning cybersecurity controls...',
    'Analyzing NIST CSF requirements...',
    'Checking organizational compliance...',
    'Threat surface assessment complete.',
    'GovernX engine online.',
    'Monitoring compliance posture...'
  ];

  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [key, setKey] = useState(0);

  useEffect(() => {
    const messageChangeInterval = setInterval(() => {
      setCurrentMessageIndex((prev) => (prev + 1) % messages.length);
      setKey((k) => k + 1);
    }, 4000);

    return () => clearInterval(messageChangeInterval);
  }, [messages.length]);

  return (
    <div className="terminal-messages">
      <div className="terminal-prefix">{'>'}</div>
      <TypingEffect key={key} text={messages[currentMessageIndex]} speed={30} />
    </div>
  );
}

export default TerminalMessages;
