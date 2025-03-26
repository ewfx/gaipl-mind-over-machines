/* eslint-disable prettier/prettier */
import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import {
  CCol,
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
  CFormSelect,
  CWidgetStatsB,
  CHeaderNav,
  CNavItem,
  CNavLink,
} from '@coreui/react';
import { CChartLine, CChartBar, CChartDoughnut } from '@coreui/react-chartjs';
import axios from 'axios';
import { Link, NavLink } from 'react-router-dom';
import ApiService from '../../apiService';
const API_URL = 'http://localhost:8000/api/';

const Metrics = () => {
  const [selectedDC, setSelectedDC] = useState(''); // Default Data Center
  const [dataCenters, setDataCenters] = useState([]); // Store all data centers
  const [selectedTelemetry, setSelectedTelemetry] = useState([]); // Selected telemetry data
  const [selectedMetrics, setSelectedMetrics] = useState([]); // Selected metrics
  const [selectedApplications, setSelectedApplications] = useState([]); // Selected applications
  const [loading, setLoading] = useState(true); // Loading state

  // useEffect(() => {
  //   // Fetch data from API
  //   fetch(API_URL + 'metrics') // Replace with your actual API endpoint
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setDataCenters(data);
  //       if (data.length > 0) {
  //         const firstDC = Object.keys(data[0])[0]; // Default to first DC
  //         updateSelectedData(firstDC, data);
  //       }
  //     })
  //     .catch((error) => console.error('Error fetching data:', error))
  //     .finally(() => setLoading(false)); // Hide loader after data is fetched
  // }, []);

  useEffect(() => {
    // Fetch data from API
    fetch(API_URL + 'datacenters') // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => {
        setDataCenters(data);
      })
      .catch((error) => console.error('Error fetching data:', error))
  }, []);

  useEffect(() => {
    // Fetch data from API
    fetch(API_URL + 'metrics-individual') // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => {
        setSelectedMetrics(data);
      })
      .catch((error) => console.error('Error fetching data:', error))
  }, []);


  useEffect(() => {
    // Fetch data from API
    fetch(API_URL + 'telemetry-individual') // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => {
        setSelectedTelemetry(data);
      })
      .catch((error) => console.error('Error fetching data:', error))
  }, []);


  useEffect(() => {
    // Fetch data from API
    fetch(API_URL + 'applications-individual') // Replace with your actual API endpoint
      .then((response) => response.json())
      .then((data) => {
        setSelectedApplications(data);
      })
      .catch((error) => console.error('Error fetching data:', error))
      .finally(() => setLoading(false)); // Hide loader after data is fetched
  }, []);

  // Function to update state when data center is changed
  const updateSelectedData = (dcName, allData) => {
    const selectedData = allData.find((dc) => dc[dcName]);
    if (selectedData) {
      setSelectedDC(dcName);
      setSelectedTelemetry(selectedData[dcName].telemetryData);
      setSelectedMetrics(selectedData[dcName].metrics);
      setSelectedApplications(selectedData[dcName].applications);
    }
  };

  useEffect(() => {
    const userData = {
      message:
        "Welcome to the Open Shift Metrics Page! 📊 Here, you can monitor shift metrics, analyze trends, and optimize workforce efficiency. Let me know if you need insights or assistance with any data! 😊",
      page: 'metrics',
      id: '1',
      dataId: '1234',
    };
    ApiService.postIncident(userData);
  }, []);

  // Function to calculate progress based on value
  const calculateProgress = (title, value) => {
    if (title === 'State') return value === 'UP' ? 100 : 0; // Full if UP, 0 if DOWN
    const num = parseFloat(value.replace(/[^0-9.]/g, '')) || 0;
    return Math.min(100, Math.max(10, num % 100)); // Keeps progress between 10-100%
  };

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
  );

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
  );

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
  );

  return (
    <>
      {/* Show loading spinner with gray overlay while data is being fetched */}
      {loading && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(128, 128, 128, 0.5)', // Semi-transparent gray overlay
            zIndex: 1000, // Ensure it's on top of other content
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div style={{ opacity: loading ? 0.5 : 1, transition: 'opacity 0.3s ease-in-out' }}>
        {/* Dropdown for Data Center Selection */}
        <CFormSelect
          value={selectedDC}
          className="mb-3"
        >
          {dataCenters.map((dc) => {
            const dcName = Object.keys(dc)[0];
            return (
              <option key={dcName} value={dcName}>
                {dcName}
              </option>
            );
          })}
        </CFormSelect>

        {/* Telemetry Metrics Widgets */}
        <CRow xs={{ gutter: 4 }}>
          {selectedTelemetry &&
            selectedTelemetry.map((metric, index) => (
              <CCol key={index} xs={12} sm={6} lg={4} xl={2}>
                <CWidgetStatsB
                  color={metric.color}
                  inverse
                  value={metric.value}
                  title={metric.title}
                  progress={{ value: calculateProgress(metric.title, metric.value) }}
                  text={`${metric.title} metric for ${selectedDC}`}
                />
              </CCol>
            ))}
        </CRow>

        {/* First Row: CPU Usage (Line) & Disk I/O (Bar) */}
        <CRow className="mt-4">
          <CCol xs={12} md={6}>
            <ChartLine
              title="CPU Usage"
              labels={selectedMetrics && selectedMetrics.timestamps}
              data={selectedMetrics && selectedMetrics.cpuUsage}
              color="#ff6384"
            />
          </CCol>
          <CCol xs={12} md={6}>
            <ChartBar
              title="Disk I/O Utilization"
              labels={selectedMetrics && selectedMetrics.timestamps}
              data={selectedMetrics && selectedMetrics.diskIO}
              color="#36a2eb"
            />
          </CCol>
        </CRow>

        {/* Second Row: Memory Usage (Doughnut) & Network Usage (Doughnut) */}
        <CRow className="mt-4">
          <CCol xs={12} md={6}>
            <CCard>
              <CCardBody>
                <h5 className="text-center">Memory Usage</h5>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart
                    data={
                      selectedMetrics &&
                      selectedMetrics.memoryUsage &&
                      selectedMetrics.memoryUsage.map((val, i) => ({
                        name: `T-${i}`,
                        value: val,
                      }))
                    }
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
          <CCol xs={12} md={6}>
            <ChartDoughnut
              title="Network Usage"
              labels={['Inbound', 'Outbound']}
              data={selectedMetrics && selectedMetrics.networkUsage}
              colors={['#4bc0c0', '#ff6384']}
            />
          </CCol>
        </CRow>

        {/* Applications Table */}
        <CRow>
          <CCol xs={12}>
            <CTable align="middle" className="mb-0 border" hover responsive>
              <CTableHead className="text-nowrap">
                <CTableRow>
                  <CTableHeaderCell className="bg-body-tertiary">Application</CTableHeaderCell>
                  <CTableHeaderCell className="bg-body-tertiary text-center">Status</CTableHeaderCell>
                  <CTableHeaderCell className="bg-body-tertiary">Memory</CTableHeaderCell>
                  <CTableHeaderCell className="bg-body-tertiary text-center">Requests</CTableHeaderCell>
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
                        <div className="fw-semibold text-nowrap">{item.status ? 'UP' : 'Down'}</div>
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
                float: 'right',
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
          </CCol>
        </CRow>
      </div>
    </>
  );
};

export default Metrics;