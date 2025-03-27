/* eslint-disable prettier/prettier */
import React, { useState, useEffect } from "react";
import { CButton, CForm, CFormLabel, CFormInput, CCol, CRow } from "@coreui/react";
import ApiService from "../../apiService";

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");

  useEffect(() => {
    const userData = {
      message: 'Hey I am trained on Knowledge Based which you provided.',
      page: 'kb',
      id: '1',
      dataId: '1234',
      tools: [],
    }
    ApiService.postIncident(userData)
  }, [])

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleTextChange = (e) => {
    setText(e.target.value);
  };

  const handleSave = () => {
    if (!file && !text) {
      alert("Please provide a file or text to save.");
      return;
    }
    console.log("Saving Data:", { file, text });
    alert("Data saved successfully!");
  };

  return (
    <div className="container p-4">
      <h3 className="mb-4">Build your model on Knowledge Base</h3>
      <CForm>
        <CRow className="mb-3">
          <CCol md="4">
            <CFormLabel>Folder path</CFormLabel>
            <CFormInput type="folder" onChange={handleFileChange} />
          </CCol>
        </CRow>

        <CRow className="mb-3">
          <CCol md="4">
            <CFormLabel>Provide Knowledge Base URL to Crawl</CFormLabel>
            <CFormInput type="text" value={text} onChange={handleTextChange} placeholder="Enter some text" />
          </CCol>
        </CRow>

        <CButton color="primary" onClick={handleSave}>
          Save
        </CButton>
      </CForm>
    </div>
  );
};

export default UploadPage;
