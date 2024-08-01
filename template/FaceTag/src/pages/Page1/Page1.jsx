import React, { useState, useRef, useCallback, useEffect } from 'react';
import Webcam from 'react-webcam';
import './Page1.css';
import Navbar from '../../components/Navbar/Navbar';

function Page1() {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    employeeId: ''
  });

  const [showCamera, setShowCamera] = useState(false);
  const [cameraOn, setCameraOn] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const webcamRef = useRef(null);

  // Determine if the form is complete
  const isFormComplete = () => {
    return formData.name && formData.age && capturedImage;
  };

  useEffect(() => {
    // Update the submit button state based on form completeness
    setIsSubmitEnabled(isFormComplete());
  }, [formData, capturedImage]);

  const [isSubmitEnabled, setIsSubmitEnabled] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    if (imageSrc) {
      setCapturedImage(imageSrc);
      setCameraOn(false); // Turn off the camera after capturing
    }
  }, [webcamRef]);

  const handleRetake = () => {
    setCapturedImage(null);
    setCameraOn(true); // Turn the camera back on
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isFormComplete()) {
      // Handle form submission
      console.log(formData);
      console.log(capturedImage);
      // Handle any form submission logic here
    }
  };

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

          {!showCamera ? (
            <button
              type="button"
              onClick={() => {
                setShowCamera(true);
                setCameraOn(true);
              }}
              className="start-camera-button"
            >
              Start Camera
            </button>
          ) : cameraOn ? (
            <div className="camera-container">
              <h3>Capture Photo:</h3>
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
          ) : (
            <div className="captured-image-container">
              <h3>Captured Photo:</h3>
              <img src={capturedImage} alt="Captured" className="captured-image"/>
              <button
                type="button"
                onClick={handleRetake}
                className="retake-button"
              >
                Retake Photo
              </button>
            </div>
          )}

          <button
            type="submit"
            className="submit-button"
            disabled={!isSubmitEnabled}
          >
            Submit
          </button>
        </form>
      </div>
    </>
  );
}

export default Page1;
