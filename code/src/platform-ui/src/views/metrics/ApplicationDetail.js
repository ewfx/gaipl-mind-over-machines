/* eslint-disable prettier/prettier */
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { CCard, CCardBody, CCardHeader, CSpinner, CBadge } from '@coreui/react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import ApiService from '../../apiService'
const API_URL = 'http://localhost:8000/api/applications_details'

const ApplicationDetails = () => {
  const params = useParams()
  console.log('Params:', params) // Debugging purpose
  const applicationId = params.applicationId || window.location.hash.split('/').pop() // Extract ID manually

  console.log('applicationId : ' + applicationId)
  useParams()
  const [appData, setAppData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const userData = {
      id: '1',
      message:
        "You're now viewing " +
        applicationId +
        ' 📝. Here, you can check the details, status, and updates related to this application. Let me know if you need any assistance or further insights! 😊',
      page: 'metrics',
      dataId: applicationId, // Replace with a dynamic or meaningful ID if needed
    }
    ApiService.postIncident(userData)
  }, [])

  useEffect(() => {
    const fetchApplicationDetails = async () => {
      try {
        const response = await fetch(`${API_URL}?app_id=${applicationId}`)
        const data = await response.json()
        setAppData(data)
      } catch (err) {
        setError('Failed to load application details')
      } finally {
        setLoading(false)
      }
    }
    fetchApplicationDetails()
  }, [applicationId])

  if (loading) return <CSpinner color="primary" />
  if (error) return <div className="text-danger">{error}</div>

  return (
    <div className="container-fluid">
      {appData &&
        appData.map((data, index) => (
          <CCard className="mb-4">
            <CCardHeader className="bg-primary text-white">Application Details</CCardHeader>
            <CCardBody>
              <h3>{data.name}</h3>
              <CBadge color={appData.status === 'Running' ? 'success' : 'danger'}>
                {data.status}
              </CBadge>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  data={data.metrics.cpuUsage.map((cpu, index) => ({
                    timestamp: `T${index + 1}`,
                    cpu: cpu,
                    memory: data.metrics.memoryUsage[index] || 0,
                  }))}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="timestamp" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="cpu" stroke="#8884d8" name="CPU Usage" />
                  <Line type="monotone" dataKey="memory" stroke="#82ca9d" name="Memory Usage" />
                </LineChart>
              </ResponsiveContainer>
            </CCardBody>
          </CCard>
          
        ))}
    </div>
  )
}

export default ApplicationDetails
