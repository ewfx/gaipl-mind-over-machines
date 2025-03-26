/* eslint-disable prettier/prettier */
import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { CCard, CCardBody, CCardHeader, CRow, CCol, CBadge, CSpinner, CContainer, CFormTextarea } from '@coreui/react'
import ApiService from '../../apiService';
const API_URL = 'http://localhost:8000/api/'

const statusColors = {
    Open: 'danger',
    InProgress: 'warning',
    Resolved: 'success',
    Closed: 'secondary',
  };

const IncidentDetail = () => {

    const params = useParams();
    console.log("Params:", params); // Debugging purpose
    const incidentId = params.incidentId || window.location.hash.split('/').pop(); // Extract ID manually

    console.log("incidentId : "+incidentId)
  
    const [incident, setIncident] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    console.log("incidentId ===== "+incidentId)

    useEffect(() => {
      const userData = {
        message: "You're now viewing Incident "+incidentId+" 🔍. Here, you can check the details, status, and updates related to this incident. Let me know if you need any assistance or further insights! 😊",
        page: "incident_detail",
        id: '1',
        dataId: incidentId,
      };
      ApiService.postIncident(userData);
    }, []);

    useEffect(() => {
        const fetchIncident = async () => {
        try {
            const response = await fetch(`${API_URL}incidents_elastic?incident_id=${incidentId}`)
            const data = await response.json()
            setIncident(data)
        } catch (err) {
            setError('Failed to load incident details')
        } finally {
            setLoading(false)
        }
        }

        fetchIncident()
    }, [incidentId])

    if (loading) return <CSpinner color="primary" />
    if (error) return <div className="text-danger">{error}</div>

    return (
        <CContainer fluid className="mt-4">
          <CCard className="shadow-lg">
            <CCardHeader className="bg-primary text-white">
              <h4 className="mb-0">Incident Details</h4>
            </CCardHeader>
            <CCardBody>
              {/* Incident Info */}
              <CRow className="mb-3">
                <CCol md={3}>
                  <strong>Incident ID:</strong>
                  <p className="text-primary fw-bold">{incident.IncidentId}</p>
                </CCol>
                <CCol md={3}>
                  <strong>Priority:</strong>
                  <p className="fw-bold">{incident.priority}</p>
                </CCol>
                <CCol md={3}>
                  <strong>Title:</strong>
                  <p>{incident.title}</p>
                </CCol>
                <CCol md={3}>
                  <strong>Status:</strong>
                  <CBadge color={statusColors[incident.status] || 'secondary'}>
                    {incident.status}
                  </CBadge>
                </CCol>
              </CRow>
    
              {/* Description Box */}
              <CCard className="mb-4">
                <CCardHeader>
                  <strong>Description</strong>
                </CCardHeader>
                <CCardBody>
                  <p className="text-muted">{incident.description}</p>
                </CCardBody>
              </CCard>
    
              {/* Comments & Resolution */}
              <CRow>
                <CCol md={6}>
                  <CCard className="mb-4">
                    <CCardHeader>
                      <strong>Comments</strong>
                    </CCardHeader>
                    <CCardBody>
                      <CFormTextarea rows="3" placeholder="Add a comment..." />
                    </CCardBody>
                  </CCard>
                </CCol>
    
                <CCol md={6}>
                  <CCard className="mb-4">
                    <CCardHeader>
                      <strong>Resolution</strong>
                    </CCardHeader>
                    <CCardBody>
                      <CFormTextarea rows="3" placeholder="Add resolution details..." value={incident.rootCause} />
                    </CCardBody>
                  </CCard>
                </CCol>
              </CRow>
    
              {/* Created & Updated */}
              <CRow>
                <CCol md={6}>
                  <strong>Created At:</strong>
                  <p>{incident.createdDate}</p>
                </CCol>
                <CCol md={6}>
                  <strong>Closed At:</strong>
                  <p>{incident.closedDate}</p>
                </CCol>
              </CRow>
            </CCardBody>
          </CCard>
        </CContainer>
      );
}

export default IncidentDetail
