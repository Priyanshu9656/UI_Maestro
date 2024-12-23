

import React, { useState, useEffect, useRef } from 'react';

const ErrorBoundary = ({ children }) => {
  const [hasError, setHasError] = useState(false);
  const [errorInfo, setErrorInfo] = useState(null);
  const loggedErrors = useRef(new Set());

  const sendErrorToServer = async (error, errorInfo) => {
    if (loggedErrors.current.has(error.toString())) {
      return;
    }

    loggedErrors.current.add(error.toString());

    await fetch('http://localhost:8000/log-error', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        error: error.toString(),
        errorInfo,
      }),
    });
  };

  useEffect(() => {
    const handleError = (event) => {
      setHasError(true);
      setErrorInfo(event.message);
      sendErrorToServer(event.error, event.message);
    };

    const handleUnhandledRejection = (event) => {
      setHasError(true);
      setErrorInfo(event.reason);
      sendErrorToServer(event.reason, 'Unhandled promise rejection');
    };

    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, []);

  return children;
};

export default ErrorBoundary;