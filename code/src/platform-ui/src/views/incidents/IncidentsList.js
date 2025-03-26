/* eslint-disable prettier/prettier */
import { useState, useEffect } from 'react'
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CAvatar,
  CProgress,
  CButton,
  CButtonGroup,
  CSpinner,
  CInputGroup,
  CInputGroupText,
  CFormInput,
  CHeaderNav,
  CNavItem,
  CNavLink,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilBug, cilSearch } from '@coreui/icons'
import { Link } from 'react-router-dom'
import ApiService from '../../apiService';
const itemsPerPage = 5
const API_URL = 'http://localhost:8000/api/'

const IncidentsList = () => {
  const [tableData, setTableData] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const userData = {
      message: "Welcome to the List of Incidents Page! 🚨 Here, you can view all reported incidents, track their status, and take necessary actions. Let me know if you need help filtering or finding specific incidents! 😊",
      page: "incidents",
      id: '1',
      dataId: '1234',
    };
    ApiService.postIncident(userData);
  }, []);

  // Fetch data from API
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(API_URL + 'incident_list')
        const data = await response.json()
        setTableData(data)
      } catch (err) {
        setError('Failed to load data')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  // 🔹 Search function: Filter all columns
  const filteredData = tableData.filter((item) => {
    const searchText = searchQuery.toLowerCase()

    return (
      item.incident.name.toLowerCase().includes(searchText) ||
      item.component.toLowerCase().includes(searchText) ||
      item.progress.value.toString().includes(searchText) ||
      item.priority.toLowerCase().includes(searchText) ||
      item.activity.toLowerCase().includes(searchText)
    )
  })

  // Calculate total pages
  const totalPages = Math.ceil(filteredData.length / itemsPerPage)

  // Get current page items
  const indexOfLastItem = currentPage * itemsPerPage
  const indexOfFirstItem = indexOfLastItem - itemsPerPage
  const currentItems = filteredData.slice(indexOfFirstItem, indexOfLastItem)

  return (
    <>
      <h3 className="mb-3">Incident List</h3>

      {/* Search Bar */}
      <CInputGroup className="mb-3" style={{ maxWidth: '400px' }}>
        <CInputGroupText>
          <CIcon icon={cilSearch} />
        </CInputGroupText>
        <CFormInput
          type="text"
          placeholder="Search incidents..."
          value={searchQuery}
          onChange={(e) => {
            setSearchQuery(e.target.value)
            setCurrentPage(1)
          }}
        />
      </CInputGroup>

      {loading && <CSpinner color="primary" />}
      {error && <div className="text-danger">{error}</div>}

      {!loading && !error && (
        <>
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
              {currentItems.length > 0 ? (
                currentItems.map((item, index) => (
                  <CTableRow key={index}>
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
                ))
              ) : (
                <CTableRow>
                  <CTableDataCell colSpan="6" className="text-center">
                    No incidents found
                  </CTableDataCell>
                </CTableRow>
              )}
            </CTableBody>
          </CTable>

          {/* Pagination Controls */}
          <div className="d-flex justify-content-end mt-3">
            <CButtonGroup>
              <CButton
                color="primary"
                disabled={currentPage === 1}
                onClick={() => setCurrentPage((prev) => prev - 1)}
              >
                Previous
              </CButton>
              {[...Array(totalPages)].map((_, index) => (
                <CButton
                  key={index}
                  color={currentPage === index + 1 ? 'dark' : 'secondary'}
                  onClick={() => setCurrentPage(index + 1)}
                >
                  {index + 1}
                </CButton>
              ))}
              <CButton
                color="primary"
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage((prev) => prev + 1)}
              >
                Next
              </CButton>
            </CButtonGroup>
          </div>
        </>
      )}
    </>
  )
}

export default IncidentsList
