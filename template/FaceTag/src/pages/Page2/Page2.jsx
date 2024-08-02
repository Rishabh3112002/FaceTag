import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import './Page2.css';
import Navbar from '../../components/Navbar/Navbar';

function Page2() {
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [responseMessage, setResponseMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const webcamRef = useRef(null);

  const startCamera = () => {
    setIsCameraOpen(true);
    setResponseData(null);
    setResponseMessage('');
    setErrorMessage('');
  };

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);
    setIsCameraOpen(false);
  }, [webcamRef]);

  const retake = () => {
    setCapturedImage(null);
    setIsCameraOpen(true);
    setResponseMessage('');
    setErrorMessage('');
  };

  const handleAnotherCapture = () => {
    setCapturedImage(null);
    setIsCameraOpen(true);
    setResponseData(null);
    setResponseMessage('');
    setErrorMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!capturedImage) return;

    // Convert base64 image to file
    const base64Response = await fetch(capturedImage);
    const blob = await base64Response.blob();
    const file = new File([blob], 'captured_image.jpg', { type: 'image/jpeg' });

    // Create FormData object
    const payload = new FormData();
    payload.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/recognise', {
        method: 'POST',
        body: payload,
      });
      const data = await response.json();

      if (data.code === 'success') {
        if (Object.keys(data.data).length === 0) {
          setResponseMessage(data.message);
        } else {
          setResponseData(data.data);
          setResponseMessage(data.message);
        }
        setCapturedImage(null);
      } else {
        setErrorMessage(data.message);
      }
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  return (
    <>
      <Navbar />
      <div className="page1-container">
        <h2>Face Recognition</h2>
        <form onSubmit={handleSubmit} className="employee-form">
          {!isCameraOpen && !capturedImage && !responseData && !responseMessage && (
            <button type="button" onClick={startCamera} className="start-camera-button">
              Start Camera
            </button>
          )}
          {isCameraOpen && (
            <div className="camera-container">
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                className="webcam"
              />
              <button type="button" onClick={capture} className="capture-button">
                Capture Photo
              </button>
            </div>
          )}
          {capturedImage && !responseData && (
            <div className="captured-image-container">
              <h3>Captured Photo:</h3>
              <img src={capturedImage} alt="Captured" className="captured-image" />
              <button type="button" onClick={retake} className="retake-button">
                Retake Photo
              </button>
              <button type="submit" className="submit-button">
                Submit
              </button>
            </div>
          )}
          {responseMessage && !responseData && (
            <div className="response-data-container">
              <h3>{responseMessage}</h3>
              <button type="button" onClick={handleAnotherCapture} className="another-capture-button">
                Capture Another
              </button>
            </div>
          )}
          {responseData && (
            <div className="response-data-container">
              <h3>{responseMessage}</h3>
              <p><strong>Employee ID:</strong> {responseData.employee_id}</p>
              <p><strong>Name:</strong> {responseData.name}</p>
              <p><strong>Similarity:</strong> {responseData.similarity.toFixed(2)}</p>
              <button type="button" onClick={handleAnotherCapture} className="another-capture-button">
                Capture Another
              </button>
            </div>
          )}
          {errorMessage && <div className="error-message">{errorMessage}</div>}
        </form>
      </div>
    </>
  );
}

export default Page2;
