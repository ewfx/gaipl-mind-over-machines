/* eslint-disable prettier/prettier */
import { useState, useEffect } from 'react'
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CProgress,
  CButton,
  CButtonGroup,
  CSpinner,
  CInputGroup,
  CInputGroupText,
  CFormInput,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilSearch } from '@coreui/icons'
import { Link } from 'react-router-dom'
import ApiService from '../../apiService';
const itemsPerPage = 5
const API_URL = 'http://localhost:8000/api/'

const ApplicationsList = () => {
  const [tableData, setTableData] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const userData = {
      message: "Welcome to the List of Open Shift Applications Page! 🏆 Here, you can review all open shift requests, track their status, and take necessary actions. Let me know if you need help filtering or managing applications! 😊",
      page: "metrics",
      id: '1',
      dataId: '1234',
    };
    ApiService.postIncident(userData);
  }, []);

  // Fetch data from API
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(API_URL + 'applications')
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
      item.application.name.toLowerCase().includes(searchText) ||
      item.application.type.toLowerCase().includes(searchText) ||
      item.status.toLowerCase().includes(searchText) ||
      item.memory.value.toString().includes(searchText) ||
      item.requests.toLowerCase().includes(searchText) ||
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
      <h3 className="mb-3">Applications List</h3>

      {/* Search Bar */}
      <CInputGroup className="mb-3" style={{ maxWidth: '400px' }}>
        <CInputGroupText>
          <CIcon icon={cilSearch} />
        </CInputGroupText>
        <CFormInput
          type="text"
          placeholder="Search applications..."
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
                <CTableHeaderCell className="bg-body-tertiary">Application</CTableHeaderCell>
                <CTableHeaderCell className="bg-body-tertiary text-center">Status</CTableHeaderCell>
                <CTableHeaderCell className="bg-body-tertiary">Memory</CTableHeaderCell>
                <CTableHeaderCell className="bg-body-tertiary text-center">
                  Requests
                </CTableHeaderCell>
                <CTableHeaderCell className="bg-body-tertiary">Last Restarted</CTableHeaderCell>
                <CTableHeaderCell className="bg-body-tertiary">Action</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              {currentItems.length > 0 ? (
                currentItems.map((item, index) => (
                  <CTableRow v-for="item in tableItems" key={index}>
                    <CTableDataCell>
                      <Link
                        to={`/applicationDetail/${item.application.name}`}
                        className="text-primary text-decoration-none"
                      >
                        {item.application.name}
                      </Link>
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
                        <div className="fw-semibold">{item.memory.value}%</div>
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
                ))
              ) : (
                <CTableRow>
                  <CTableDataCell colSpan="6" className="text-center">
                    No Applications found
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

export default ApplicationsList
