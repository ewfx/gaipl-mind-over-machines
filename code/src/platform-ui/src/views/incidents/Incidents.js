/* eslint-disable prettier/prettier */
import React, { useEffect, useState } from 'react'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import CIcon from '@coreui/icons-react'
import {
  CCol,
  CAvatar,
  CProgress,
  CRow,
  CCard,
  CCardBody,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CWidgetStatsB,
  CHeaderNav,
  CNavItem,
  CNavLink,
} from '@coreui/react'
import { cilBug } from '@coreui/icons'
import { CChartLine, CChartBar, CChartDoughnut } from '@coreui/react-chartjs'
import { Link, NavLink } from 'react-router-dom'
import ApiService from '../../apiService';

// eslint-disable-next-line prettier/prettier
// eslint-disable-next-line prettier/prettier

const API_URL = 'http://localhost:8000/api/'

const Incidents = () => {
  const [incidents, setIncidents] = useState([])
  const [incMetrics, setIncMetrics] = useState({
    summary: [],
    metrics: [ 
    ]
  })

  useEffect(() => {
    const userData = {
      message: "Welcome to the Incidents Page! 🚀 Here, you can track, report, and manage incidents seamlessly. Let me know if you need assistance in logging a new issue or checking the status of an existing one. I'm here to help! 😊",
      page: "incidents",
      id: '1',
      dataId: '1234',
    };
    ApiService.postIncident(userData);  // Sending only the message
  }, []);

  useEffect(() => {
    fetch(API_URL + 'incidents-overview')
      .then((response) => response.json())
      .then((data) => {
        setIncMetrics(data)
      })
      .catch((error) => console.error('Error fetching incidents:', error))
  }, [])


  // useEffect(() => {
  //   fetch(API_URL + 'incidents-data')
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setIncidentsData(data)
  //     })
  //     .catch((error) => console.error('Error fetching incidents:', error))
  // }, [])

  useEffect(() => {
    fetch(API_URL + 'incident_list?limit=6')
      .then((response) => response.json())
      .then((data) => {
        setIncidents(data)
      })
      .catch((error) => console.error('Error fetching incidents:', error))
  }, [])

  useEffect(() => {
    fetch(API_URL + 'incident-metrics')
      .then((response) => response.json())
      .then((data) => {
        console.log(JSON.stringify(data))
        setIncidentMetrics(data)
      })
      .catch((error) => console.error('Error fetching incidents:', error))
  }, [])

  // Line Chart Component
  const ChartLine = ({ title, labels, data, color }) => (
    <CCard className="mb-4">
      <CCardBody>
        <h5 className="text-center">{title}</h5>
        <CChartLine
          data={{
            labels,
            datasets: [{ label: title, borderColor: color, borderWidth: 2, data }],
          }}
          options={{ maintainAspectRatio: false, plugins: { legend: { display: false } } }}
          style={{ height: '300px' }}
        />
      </CCardBody>
    </CCard>
  )

  // Bar Chart Component
  const ChartBar = ({ title, labels, data, color }) => (
    <CCard className="mb-4">
      <CCardBody>
        <h5 className="text-center">{title}</h5>
        <CChartBar
          data={{
            labels,
            datasets: [{ label: title, backgroundColor: color, data }],
          }}
          options={{ maintainAspectRatio: false, plugins: { legend: { display: false } } }}
          style={{ height: '300px' }}
        />
      </CCardBody>
    </CCard>
  )

  // Doughnut Chart Component
  const ChartDoughnut = ({ title, labels, data, colors }) => (
    <CCard className="mb-4">
      <CCardBody>
        <h5 className="text-center">{title}</h5>
        <CChartDoughnut
          data={{
            labels,
            datasets: [{ backgroundColor: colors, data }],
          }}
          options={{ maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }}
          style={{ height: '300px' }}
        />
      </CCardBody>
    </CCard>
  )

  const calculateSeverityProgress = (priority) => {
    switch (priority) {
      case 'High':
        return 90 // High severity incidents almost max out progress
      case 'Medium':
        return 60 // Medium severity incidents are halfway
      case 'Low':
        return 30 // Low severity incidents have minimal impact
      case 'Planned':
        return 10 // Planned events should have the least urgency
      default:
        return 50 // Default value for unknown priority
    }
  }

  //   const incidentMetrics = {
  //     timestamps: ["Jan", "Feb", "Mar", "Apr", "May"], // X-axis for line chart
  //     incidentCount: [10, 20, 15, 30, 25], // Incident count over time

  //     severityLevels: ["Low", "Medium", "High", "Critical"], // X-axis for bar chart
  //     severityCounts: [5, 12, 8, 4], // Number of incidents per severity

  //     resolutionTimes: [5, 8, 6, 12, 10, 4, 7], // Time taken to resolve incidents over days
  //     types: ["Network", "Hardware", "Software", "Security"], // Incident categories
  //     typeCounts: [15, 10, 25, 5], // Number of incidents per type
  //   };

  return (
    <>
      {/* <WidgetsDropdown className="mb-4" /> */}
      <div>
        <CRow xs={{ gutter: 4 }}>
          {incMetrics && incMetrics.summary && incMetrics.summary.map((incident, index) => (
            <CCol key={index} xs={12} sm={5} md={5} lg={3}>
              <CWidgetStatsB
                color={incident.color}
                inverse
                value={incident.status}
                title={incident.title}
                progress={{ value: calculateSeverityProgress(incident.priority) }}
                text={`Affected: ${incident.system} | Reported: ${incident.reportedTime}`}
              />
            </CCol>
          ))}
        </CRow>
        {/* First Row: CPU Usage (Line) & Disk I/O (Bar) */}
        <CRow className="mt-4">
          {/* Line Chart - Incident Count Over Time */}
          <CCol xs={12} md={6}>
            <ChartLine
              title="Incident Trend Over Time"
              labels={incMetrics && incMetrics.metrics && incMetrics.metrics.timestamps}
              data={incMetrics && incMetrics.metrics && incMetrics.metrics.incidentCount}
              color="#ff6384"
            />
          </CCol>

          {/* Bar Chart - Incident Severity Distribution */}
          <CCol xs={12} md={6}>
            <ChartBar
              title="Incident Severity Distribution"
              labels={incMetrics && incMetrics.metrics && incMetrics.metrics.severityLevels}
              data={incMetrics && incMetrics.metrics && incMetrics.metrics.severityCounts}
              color="#36a2eb"
            />
          </CCol>
        </CRow>

        {/* Second Row: Memory Usage (Doughnut) & Network Usage (Doughnut) */}
        <CRow className="mt-4">
          {/* Area Chart - Incident Resolution Over Time */}
          <CCol xs={12} md={6}>
            <CCard>
              <CCardBody>
                <h5 className="text-center">Incident Resolution Trend</h5>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart
                    data={incMetrics && incMetrics.metrics && incMetrics.metrics.resolutionTimes && incMetrics.metrics.resolutionTimes.map((val, i) => ({
                      name: `Day ${i + 1}`,
                      value: val,
                    }))}
                  >
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="value" stroke="#8884d8" fill="#8884d8" />
                  </AreaChart>
                </ResponsiveContainer>
              </CCardBody>
            </CCard>
          </CCol>

          {/* Doughnut Chart - Incident Type Distribution */}
          <CCol xs={12} md={6}>
            <ChartDoughnut
              title="Incident Type Distribution"
              labels={incMetrics && incMetrics.metrics && incMetrics.metrics.types}
              data={incMetrics && incMetrics.metrics && incMetrics.metrics.typeCounts}
              colors={['#4bc0c0', '#ff6384', '#36a2eb', '#ff9f40']}
            />
          </CCol>
        </CRow>
      </div>
      <CRow>
        <CCol xs={12}></CCol>
      </CRow>
      <CRow>
        <CCol xs={12}>
          <CTable align="middle" className="mb-0 border" hover responsive>
            <CTableHead className="text-nowrap">
              <CTableRow>
                <CTableHeaderCell className="bg-body-tertiary text-center"></CTableHeaderCell>
                <CTableHeaderCell className="bg-body-tertiary">Incident</CTableHeaderCell>
               
                <CTableHeaderCell className="bg-body-tertiary">Progress</CTableHeaderCell>
                <CTableHeaderCell className="bg-body-tertiary text-center">
                  Priority
                </CTableHeaderCell>
                <CTableHeaderCell className="bg-body-tertiary">Activity</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              {incidents && incidents.map((item, index) => (
                <CTableRow v-for="item in tableItems" key={index}>
                  <CTableDataCell className="text-center">
                    <CAvatar size="md" status={item.avatar.status}>
                      <CIcon icon={cilBug} size="lg" />
                    </CAvatar>
                  </CTableDataCell>
                  <CTableDataCell>
                    <div>
                      <Link
                        to={`/incidentDetail/${item.incident.name}`}
                        className="text-primary text-decoration-none"
                      >
                        {item.incident.name}
                      </Link>
                    </div>
                    <div className="small text-body-secondary text-nowrap">
                      <span>{item.incident.new ? 'New' : 'Recurring'}</span> | Registered:{' '}
                      {item.incident.registered}
                    </div>
                  </CTableDataCell>
                  
                  <CTableDataCell>
                    <div className="d-flex justify-content-between text-nowrap">
                      <div className="fw-semibold">{item.progress.value}%</div>
                      <div className="ms-3">
                        <small className="text-body-secondary">{item.progress.period}</small>
                      </div>
                    </div>
                    <CProgress thin color={item.progress.color} value={item.progress.value} />
                  </CTableDataCell>
                  <CTableDataCell className="text-center">
                    <div className="fw-semibold text-nowrap">{item.priority}</div>
                  </CTableDataCell>
                  <CTableDataCell>
                    <div className="small text-body-secondary text-nowrap">Last login</div>
                    <div className="fw-semibold text-nowrap">{item.activity}</div>
                  </CTableDataCell>
                </CTableRow>
              ))}
              <div
                style={{
                  float: 'right',
                  fontWeight: 'bold',
                  marginTop: '12px',
                  marginRight: '10px',
                }}
              >
                <CHeaderNav className="d-none d-md-flex">
                  <CNavItem>
                    <CNavLink to="/incidentsList" as={NavLink} className="nav-link">
                      More
                    </CNavLink>
                  </CNavItem>
                </CHeaderNav>
              </div>
            </CTableBody>
          </CTable>
        </CCol>
      </CRow>
      <CRow>
        <CCol xs={12}></CCol>
      </CRow>
    </>
  )
}

export default Incidents
