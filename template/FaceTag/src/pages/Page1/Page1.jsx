import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { useNavigate } from 'react-router-dom';
import './Page1.css';
import Navbar from '../../components/Navbar/Navbar';

function Page1() {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    employeeId: ''
  });

  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const startCamera = () => {
    setIsCameraOpen(true);
  };

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setCapturedImage(imageSrc);
    setIsCameraOpen(false);
  }, [webcamRef]);

  const retake = () => {
    setCapturedImage(null);
    setIsCameraOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { name, age, employeeId } = formData;

    // Convert base64 image to file
    const base64Response = await fetch(capturedImage);
    const blob = await base64Response.blob();
    const file = new File([blob], 'captured_image.jpg', { type: 'image/jpeg' });

    // Create FormData object
    const payload = new FormData();
    payload.append('name', name);
    payload.append('age', age);
    payload.append('employee_id', employeeId);
    payload.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/create_entry', {
        method: 'POST',
        body: payload
      });
      const data = await response.json();

      if (data.code === 'success') {
        navigate('/'); // Redirect to home page
      } else {
        setErrorMessage(data.message);
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      setErrorMessage('An error occurred while submitting the form.');
    }
  };

  const isFormValid = formData.name && formData.age && capturedImage;

  return (
    <>
      <Navbar />
      <div className="page1-container">
        <h2>Add New Entry</h2>
        <form onSubmit={handleSubmit} className="employee-form">
          <label>
            Name:
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder='Name'
              required
            />
          </label>
          <label>
            Age:
            <input
              type="number"
              name="age"
              value={formData.age}
              onChange={handleInputChange}
              placeholder='Age'
              required
            />
          </label>
          <label>
            Employee ID:
            <input
              type="text"
              name="employeeId"
              value={formData.employeeId}
              onChange={handleInputChange}
              placeholder='Employee ID (Optional)'
            />
          </label>
          {!isCameraOpen && !capturedImage && (
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
          {capturedImage && (
            <div className="captured-image-container">
              <h3>Captured Photo:</h3>
              <img src={capturedImage} alt="Captured" className="captured-image" />
              <button type="button" onClick={retake} className="retake-button">
                Retake Photo
              </button>
            </div>
          )}
          {errorMessage && <p className="error-message">{errorMessage}</p>}
          <button type="submit" className="submit-button" disabled={!isFormValid}>
            Submit
          </button>
        </form>
      </div>
    </>
  );
}

export default Page1;
