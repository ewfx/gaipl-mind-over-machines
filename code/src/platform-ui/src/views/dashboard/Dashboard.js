import React, { useEffect, useRef, useState } from 'react'
import classNames from 'classnames'
import { getStyle } from '@coreui/utils'

import {
  CAvatar,
  CButton,
  CButtonGroup,
  CCard,
  CCardBody,
  CCardFooter,
  CCardHeader,
  CCol,
  CHeaderNav,
  CNavItem,
  CNavLink,
  CProgress,
  CRow,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CWidgetStatsE,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilCloudDownload, cilBug } from '@coreui/icons'
import { CChartLine } from '@coreui/react-chartjs'

import { GaugeComponent } from 'react-gauge-component'
import { Link, NavLink } from 'react-router-dom'
import ApiService from '../../apiService'

const API_URL = 'http://localhost:8000/api/'

const Dashboard = () => {
  const [dashboardMetrics, setDashboardMetrics] = useState({
    system_metrics: [],
    network_metrics: [],
    performance_metrics: [],
    applications: [],
  })

  const [incidentMetrics, setIncidentMetrics] = useState({
    labels: [],
    datasets: [],
    percentage: 0,
    averageResolutionTime: 0,
    incidentResolutionRate: 0,
    incidentStatusCounts: {
      New: 0,
      Resolved: 0,
      Unresolved: 0,
      Closed: 0,
    },
  })

  const [incidentStatus, setIncidentStatus] = useState({
    labels: [],
    datasets: [],
    progress: [],
  })

  const [incidents, setIncidents] = useState([])

  const [selectedApplications, setSelectedApplications] = useState([]) // Selected applications

  const chartRef = useRef(null)

  useEffect(() => {
    const userData = {
      message: 'Hey welcome to SentinelX Dashboard',
      page: 'dashboard',
      id: '1',
      dataId: '1234',
    }
    ApiService.postIncident(userData)
  }, [])

  useEffect(() => {
    // Fetch progress data from API
    fetch(API_URL + 'dashboard/metrics') // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => setDashboardMetrics(data))
      .catch((error) => console.error('Error fetching data:', error))
  }, [])

  useEffect(() => {
    // Fetch progress data from API
    fetch(API_URL + 'latest_seven_days_incidents') // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => setIncidentMetrics(data))
      .catch((error) => console.error('Error fetching data:', error))
  }, [])

  useEffect(() => {
    // Fetch progress data from API
    fetch(API_URL + 'latest_six_months_incidents') // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => setIncidentStatus(data))
      .catch((error) => console.error('Error fetching data:', error))
  }, [])

  useEffect(() => {
    fetch(API_URL + 'incident_list?limit=6')
      .then((response) => response.json())
      .then((data) => {
        setIncidents(data)
      })
      .catch((error) => console.error('Error fetching incidents:', error))
  }, [])

  useEffect(() => {
    // Fetch data from API
    fetch(API_URL + 'applications-individual') // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => {
        setSelectedApplications(data)
      })
      .catch((error) => console.error('Error fetching data:', error))
  }, [])

  useEffect(() => {
    document.documentElement.addEventListener('ColorSchemeChange', () => {
      if (chartRef.current) {
        setTimeout(() => {
          chartRef.current.options.scales.x.grid.borderColor = getStyle(
            '--cui-border-color-translucent',
          )
          chartRef.current.options.scales.x.grid.color = getStyle('--cui-border-color-translucent')
          chartRef.current.options.scales.x.ticks.color = getStyle('--cui-body-color')
          chartRef.current.options.scales.y.grid.borderColor = getStyle(
            '--cui-border-color-translucent',
          )
          chartRef.current.options.scales.y.grid.color = getStyle('--cui-border-color-translucent')
          chartRef.current.options.scales.y.ticks.color = getStyle('--cui-body-color')
          chartRef.current.update()
        })
      }
    })
  }, [chartRef])

  return (
    <>
      {/* <WidgetsDropdown className="mb-4" /> */}
      <CRow>
        <CCol xs={12}></CCol>
        <CCol xs={6} style={{ height: '500px' }}>
          <CRow className="g-4">
            {/* First Row */}
            <CCol xs={6} style={{ height: '150px', overflow: 'hidden' }}>
              <CWidgetStatsE
                style={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                }}
                chart={
                  <CChartLine
                    className="mx-auto"
                    style={{ height: '50px', width: '100%' }} // Adjusted to fit within 150px
                    data={{
                      labels: incidentMetrics && incidentMetrics.labels,
                      datasets: incidentMetrics && incidentMetrics.datasets,
                    }}
                    options={{
                      maintainAspectRatio: false,
                      elements: {
                        line: { tension: 0.4 },
                        point: { radius: 0 },
                      },
                      plugins: {
                        legend: { display: false },
                      },
                      scales: {
                        x: { display: true },
                        y: { display: true },
                      },
                    }}
                  />
                }
                title="Incidents Overview"
                value={incidentMetrics && incidentMetrics.incidentResolutionRate}
              />
            </CCol>

            <CCol xs={6}>
              <CCard>
                <CCardBody
                  className="d-flex flex-column justify-content-center align-items-center"
                  style={{ height: '150px' }}
                >
                  <h5 className="text-center">Incident Resolution Time</h5>
                  <h5 className="text-center mt-2">24.05 hrs</h5>
                </CCardBody>
              </CCard>
            </CCol>

            {/* Second Row */}
            <CCol xs={6}>
              <CCard>
                <CCardBody
                  style={{
                    height: '300px',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                  }}
                >
                  <h6 style={{ marginBottom: '15px' }}>Incidents</h6>
                  <div
                    style={{
                      width: '100%',
                      height: '100%',
                      display: 'grid',
                      gridTemplateColumns: '1fr 1fr',
                      gridTemplateRows: '1fr 1fr',
                      gap: '10px',
                      textAlign: 'center',
                    }}
                  >
                    {/* Row 1 */}
                    <div
                      style={{
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center',
                        borderRight: '1px solid #ccc',
                        borderBottom: '1px solid #ccc',
                      }}
                    >
                      <h5 style={{ fontWeight: 'bold', margin: 0 }}>
                        {incidentMetrics &&
                          incidentMetrics.incidentStatusCounts &&
                          incidentMetrics.incidentStatusCounts.New}
                      </h5>
                      <small>New</small>
                    </div>
                    <div
                      style={{
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center',
                        marginLeft: '-10px',
                        borderBottom: '1px solid #ccc',
                      }}
                    >
                      <h5 style={{ fontWeight: 'bold', margin: 0 }}>
                        {incidentMetrics &&
                          incidentMetrics.incidentStatusCounts &&
                          incidentMetrics.incidentStatusCounts.Unresolved}
                      </h5>
                      <small>Unresolved</small>
                    </div>
                    {/* Row 2 */}
                    <div
                      style={{
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center',
                        borderRight: '1px solid #ccc',
                        marginTop: '-10px',
                      }}
                    >
                      <h5 style={{ fontWeight: 'bold', margin: 0 }}>
                        {incidentMetrics &&
                          incidentMetrics.incidentStatusCounts &&
                          incidentMetrics.incidentStatusCounts.Resolved}
                      </h5>
                      <small>Resolved</small>
                    </div>
                    <div
                      style={{
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center',
                        marginTop: '-10px',
                      }}
                    >
                      <h5 style={{ fontWeight: 'bold', margin: 0 }}>
                        {incidentMetrics &&
                          incidentMetrics.incidentStatusCounts &&
                          incidentMetrics.incidentStatusCounts.Closed}
                      </h5>
                      <small>Closed</small>
                    </div>
                  </div>
                </CCardBody>
              </CCard>
            </CCol>

            <CCol xs={6}>
              <CCard>
                <CCardBody
                  className="d-flex flex-column justify-content-center align-items-center"
                  style={{ height: '300px' }}
                >
                  <div>Incident Resolution Rate</div>
                  <GaugeComponent
                    value={incidentMetrics && incidentMetrics.incidentResolutionRate}
                    type="radial"
                    labels={{
                      tickLabels: {
                        type: 'inner',
                        ticks: [
                          { value: 20 },
                          { value: 40 },
                          { value: 60 },
                          { value: 80 },
                          { value: 100 },
                        ],
                      },
                    }}
                    arc={{
                      colorArray: ['#5BE12C', '#EA4228'],
                      subArcs: [{ limit: 10 }, { limit: 30 }, {}, {}, {}],
                      padding: 0.02,
                      width: 0.3,
                    }}
                    pointer={{
                      elastic: true,
                      animationDelay: 0,
                    }}
                  />
                </CCardBody>
              </CCard>
            </CCol>
          </CRow>
        </CCol>

        <CCol xs={6} style={{ height: '500px' }}>
          <CCard className="mb-8">
            <CCardBody style={{ height: '475px' }}>
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
                  {incidents &&
                    incidents.map((item, index) => (
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
                          <div className="small text-body-secondary text-nowrap">Incident Registered</div>
                          <div className="fw-semibold text-nowrap">{item.activity}</div>
                        </CTableDataCell>
                      </CTableRow>
                    ))}
                </CTableBody>
              </CTable>
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
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
      <CCard className="mb-4">
        <CCardBody>
          <CRow>
            <CCol sm={5}>
              <h4 id="traffic" className="card-title mb-0">
                Incidents
              </h4>
              <div className="small text-body-secondary">October - March 2025</div>
            </CCol>
            <CCol sm={7} className="d-none d-md-block">
              <CButton color="primary" className="float-end">
                <CIcon icon={cilCloudDownload} />
              </CButton>
              <CButtonGroup className="float-end me-3">
                {['Day', 'Month', 'Year'].map((value) => (
                  <CButton
                    color="outline-secondary"
                    key={value}
                    className="mx-0"
                    active={value === 'Month'}
                  >
                    {value}
                  </CButton>
                ))}
              </CButtonGroup>
            </CCol>
          </CRow>
          <CChartLine
            ref={chartRef}
            style={{ height: '300px', marginTop: '40px' }}
            data={{
              labels: incidentStatus && incidentStatus.labels,
              datasets: incidentStatus && incidentStatus.datasets,
            }}
            options={{
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: false,
                },
              },
              scales: {
                x: {
                  grid: {
                    color: getStyle('--cui-border-color-translucent'),
                    drawOnChartArea: false,
                  },
                  ticks: {
                    color: getStyle('--cui-body-color'),
                  },
                },
                y: {
                  beginAtZero: true,
                  border: {
                    color: getStyle('--cui-border-color-translucent'),
                  },
                  grid: {
                    color: getStyle('--cui-border-color-translucent'),
                  },
                  max: 40,
                  ticks: {
                    color: getStyle('--cui-body-color'),
                    maxTicksLimit: 5,
                    stepSize: Math.ceil(40 / 5),
                  },
                },
              },
              elements: {
                line: {
                  tension: 0.4,
                },
                point: {
                  radius: 0,
                  hitRadius: 10,
                  hoverRadius: 4,
                  hoverBorderWidth: 3,
                },
              },
            }}
          />
        </CCardBody>
        <CCardFooter>
          <CRow
            xs={{ cols: 1, gutter: 5 }}
            sm={{ cols: 2 }}
            lg={{ cols: 6 }}
            xl={{ cols: 6 }}
            className="mb-2 text-center"
          >
            {incidentStatus &&
              incidentStatus.progress &&
              incidentStatus.progress.map((item, index, items) => (
                <CCol
                  className={classNames({
                    'd-none d-sm-block': index + 1 === items.length,
                  })}
                  key={index}
                >
                  <div className="text-body-secondary">{item.title}</div>
                  <div className="fw-semibold text-truncate">
                    {item.value} ({item.percent}%)
                  </div>
                  <CProgress thin className="mt-2" color={item.color} value={item.percent} />
                </CCol>
              ))}
          </CRow>
        </CCardFooter>
      </CCard>
      <CRow>
        <CCol xs>
          <CCard className="mb-4">
            <CCardHeader>Telemetry {' & '} Metrics</CCardHeader>
            <CCardBody>
              <CRow>
                <CCol xs={12} md={6} xl={6}>
                  <CRow>
                    <CCol xs={6}>
                      <div className="border-start border-start-4 border-start-info py-1 px-3">
                        <div className="text-body-secondary text-truncate small">CPU Usage</div>
                        <div className="fs-5 fw-semibold">45%</div>
                      </div>
                    </CCol>
                    <CCol xs={6}>
                      <div className="border-start border-start-4 border-start-danger py-1 px-3 mb-3">
                        <div className="text-body-secondary text-truncate small">Memory Usage</div>
                        <div className="fs-5 fw-semibold">68%</div>
                      </div>
                    </CCol>
                  </CRow>
                  <hr className="mt-0" />
                  {dashboardMetrics &&
                    dashboardMetrics.system_metrics &&
                    dashboardMetrics.system_metrics.map((item, index) => (
                      <div className="progress-group mb-4" key={index}>
                        <div className="progress-group-prepend">
                          <span className="text-body-secondary small">{item.title}</span>
                        </div>
                        <div className="progress-group-bars">
                          <div className="d-flex justify-content-between">
                            <span className="text-info small">Current: {item.value1}%</span>
                            <span className="text-danger small">Peak: {item.value2}%</span>
                          </div>
                          <CProgress thin color="info" value={item.value1} />
                          <CProgress thin color="danger" value={item.value2} />
                        </div>
                      </div>
                    ))}
                </CCol>
                <CCol xs={12} md={6} xl={6}>
                  <CRow>
                    <CCol xs={6}>
                      <div className="border-start border-start-4 border-start-warning py-1 px-3 mb-3">
                        <div className="text-body-secondary text-truncate small">Disk Usage</div>
                        <div className="fs-5 fw-semibold">75%</div>
                      </div>
                    </CCol>
                    <CCol xs={6}>
                      <div className="border-start border-start-4 border-start-success py-1 px-3 mb-3">
                        <div className="text-body-secondary text-truncate small">
                          Network Latency
                        </div>
                        <div className="fs-5 fw-semibold">120 ms</div>
                      </div>
                    </CCol>
                  </CRow>

                  <hr className="mt-0" />

                  {dashboardMetrics &&
                    dashboardMetrics.network_metrics &&
                    dashboardMetrics.network_metrics.map((item, index) => (
                      <div className="progress-group mb-4" key={index}>
                        <div className="progress-group-header">
                          <CIcon className="me-2" icon={item.icon} size="lg" />
                          <span>{item.title}</span>
                          <span className="ms-auto fw-semibold">{item.value}%</span>
                        </div>
                        <div className="progress-group-bars">
                          <CProgress thin color="warning" value={item.value} />
                        </div>
                      </div>
                    ))}

                  <div className="mb-5"></div>

                  {dashboardMetrics &&
                    dashboardMetrics.performance_metrics &&
                    dashboardMetrics.performance_metrics.map((item, index) => (
                      <div className="progress-group mb-4" key={index}>
                        <div className="progress-group-header">
                          <CIcon className="me-2" icon={item.icon} size="lg" />
                          <span>{item.title}</span>
                          <span className="ms-auto fw-semibold">
                            {item.value}{' '}
                            <span className="text-body-secondary small">({item.percent}%)</span>
                          </span>
                        </div>
                        <div className="progress-group-bars">
                          <CProgress thin color="success" value={item.percent} />
                        </div>
                      </div>
                    ))}
                </CCol>
              </CRow>

              <br />

              <CTable align="middle" className="mb-0 border" hover responsive>
                <CTableHead className="text-nowrap">
                  <CTableRow>
                    <CTableHeaderCell className="bg-body-tertiary">Application</CTableHeaderCell>
                    <CTableHeaderCell className="bg-body-tertiary text-center">
                      Status
                    </CTableHeaderCell>
                    <CTableHeaderCell className="bg-body-tertiary">Memory</CTableHeaderCell>
                    <CTableHeaderCell className="bg-body-tertiary text-center">
                      Requests
                    </CTableHeaderCell>
                    <CTableHeaderCell className="bg-body-tertiary">Last Restarted</CTableHeaderCell>
                    <CTableHeaderCell className="bg-body-tertiary">Action</CTableHeaderCell>
                  </CTableRow>
                </CTableHead>
                <CTableBody>
                  {selectedApplications &&
                    selectedApplications.map((item, index) => (
                      <CTableRow v-for="item in tableItems" key={index}>
                        <CTableDataCell>
                          <div>
                            <Link
                              to={`/applicationDetail/${item.application.name}`}
                              className="text-primary text-decoration-none"
                            >
                              {item.application.name}
                            </Link>
                          </div>
                          <div className="small text-body-secondary text-nowrap">
                            <span>{item.application.type}</span> | Registered:{' '}
                            {item.application.registered}
                          </div>
                        </CTableDataCell>
                        <CTableDataCell className="text-center">
                          <div className="fw-semibold text-nowrap">
                            {item.status ? 'UP' : 'Down'}
                          </div>
                        </CTableDataCell>
                        <CTableDataCell>
                          <div className="d-flex justify-content-between text-nowrap">
                            <div className="fw-semibold">{item.memory.value}</div>
                            <div className="ms-3">
                              <small className="text-body-secondary">{item.memory.period}</small>
                            </div>
                          </div>
                          <CProgress thin color={item.memory.color} value={item.memory.value} />
                        </CTableDataCell>
                        <CTableDataCell className="text-center">
                          <div className="fw-semibold text-nowrap">{item.requests}</div>
                        </CTableDataCell>
                        <CTableDataCell>
                          <div className="fw-semibold text-nowrap">{item.activity}</div>
                        </CTableDataCell>
                        <CTableDataCell>
                          <span>{item.status ? 'Stop' : 'Start'}</span>
                        </CTableDataCell>
                      </CTableRow>
                    ))}
                </CTableBody>
              </CTable>
              <div
                style={{
                  float: 'left',
                  fontWeight: 'bold',
                  marginTop: '12px',
                  marginRight: '10px',
                }}
              >
                <CHeaderNav className="d-none d-md-flex">
                  <CNavItem>
                    <CNavLink to="/applicationsList" as={NavLink} className="nav-link">
                      More
                    </CNavLink>
                  </CNavItem>
                </CHeaderNav>
              </div>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}

export default Dashboard
