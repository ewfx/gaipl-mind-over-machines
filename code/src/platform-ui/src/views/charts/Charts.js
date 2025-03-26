import React from 'react'
import { CCard, CCardBody, CCol, CCardHeader, CRow } from '@coreui/react'
import {
  CChartBar,
  CChartDoughnut,
  CChartLine,
  CChartPie,
  CChartPolarArea,
  CChartRadar,
} from '@coreui/react-chartjs'
import { DocsLink } from 'src/components'

const Charts = () => {
  const random = () => Math.round(Math.random() * 100)

  return (
    <CRow>
      <CCol xs={12}></CCol>
      <CCol xs={6}>
        <CCard className="mb-4">
          <CCardHeader>
            Bar Chart <DocsLink name="chart" />
          </CCardHeader>
          <CCardBody>
            <CChartBar
              data={{
                labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                datasets: [
                  {
                    label: 'GitHub Commits',
                    backgroundColor: '#f87979',
                    data: [40, 20, 12, 39, 10, 40, 39, 80, 40],
                  },
                ],
              }}
              labels="months"
            />
          </CCardBody>
        </CCard>
      </CCol>
      <CCol xs={6}>
        <CCard className="mb-4">
          <CCardHeader>
            Line Chart <DocsLink name="chart" />
          </CCardHeader>
          <CCardBody>
            <CChartLine
              data={{
                labels: ['October', 'Novemeber', 'December', 'January', 'February', 'March'],
                datasets: [
                  {
                    label: 'New',
                    backgroundColor: '#6004a7',
                    borderColor: '#6004a7',
                    pointBackgroundColor: '#6004a7',
                    pointBorderColor: '#fff',
                    data: [19, 25, 24, 20, 25, 26],
                  },
                  {
                    label: 'In Progress',
                    backgroundColor: '#0371ea',
                    borderColor: '#0371ea',
                    pointBackgroundColor: '#0371ea',
                    pointBorderColor: '#fff',
                    data: [11, 13, 12, 10, 9, 7],
                  },
                  {
                    label: 'On Hold',
                    backgroundColor: '#0c2198',
                    borderColor: '#0c2198',
                    pointBackgroundColor: '#0c2198',
                    pointBorderColor: '#fff',
                    data: [5, 7, 8, 3, 9, 2],
                  },
                  {
                    label: 'Resolved',
                    backgroundColor: '#745749',
                    borderColor: '#745749',
                    pointBackgroundColor: '#745749',
                    pointBorderColor: '#fff',
                    data: [15, 20, 21, 16, 15, 18],
                  },
                  {
                    label: 'Closed',
                    backgroundColor: '#018b6b',
                    borderColor: '#018b6b',
                    pointBackgroundColor: '#018b6b',
                    pointBorderColor: '#fff',
                    data: [18, 26, 25, 19, 27, 29],
                  },
                  {
                    label: 'Cancelled',
                    backgroundColor: '#df0f41',
                    borderColor: '#df0f41',
                    pointBackgroundColor: '#df0f41',
                    pointBorderColor: '#fff',
                    data: [5, 8, 3, 9, 2, 8],
                  },
                ],
              }}
            />
          </CCardBody>
        </CCard>
      </CCol>
      <CCol xs={6}>
        <CCard className="mb-4">
          <CCardHeader>
            Doughnut Chart <DocsLink name="chart" />
          </CCardHeader>
          <CCardBody>
            <CChartDoughnut
              data={{
                labels: ['New', 'In progress', 'On Hold', 'Resolved', 'Closed', 'Cancelled'],
                datasets: [
                  {
                    backgroundColor: [
                      '#6004a7',
                      '#0371ea',
                      '#0c2198',
                      '#745749',
                      '#018b6b',
                      '#df0f41',
                    ],
                    data: [18, 23, 10, 30, 50, 20],
                  },
                ],
              }}
              options={{
                maintainAspectRatio: false,
                responsive: true,
                cutout: '80%', // Adjust the size of the inner circle (higher % means a smaller chart)
              }}
              style={{ height: '440px', width: '700px' }} // Set the desired size
            />
          </CCardBody>
        </CCard>
      </CCol>
      <CCol xs={6}>
        <CCard className="mb-4">
          <CCardHeader>
            Pie Chart <DocsLink name="chart" />{' '}
          </CCardHeader>
          <CCardBody>
            <CChartPie
              data={{
                labels: ['Red', 'Green', 'Yellow'],
                datasets: [
                  {
                    data: [300, 50, 100],
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                    hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                  },
                ],
              }}
            />
          </CCardBody>
        </CCard>
      </CCol>
      <CCol xs={6}>
        <CCard className="mb-4">
          <CCardHeader>
            Polar Area Chart
            <DocsLink name="chart" />
          </CCardHeader>
          <CCardBody>
            <CChartPolarArea
              data={{
                labels: ['Red', 'Green', 'Yellow', 'Grey', 'Blue'],
                datasets: [
                  {
                    data: [11, 16, 7, 3, 14],
                    backgroundColor: ['#FF6384', '#4BC0C0', '#FFCE56', '#E7E9ED', '#36A2EB'],
                  },
                ],
              }}
            />
          </CCardBody>
        </CCard>
      </CCol>
      <CCol xs={6}>
        <CCard className="mb-4">
          <CCardHeader>
            Radar Chart <DocsLink name="chart" />
          </CCardHeader>
          <CCardBody>
            <CChartRadar
              data={{
                labels: [
                  'Eating',
                  'Drinking',
                  'Sleeping',
                  'Designing',
                  'Coding',
                  'Cycling',
                  'Running',
                ],
                datasets: [
                  {
                    label: 'My First dataset',
                    backgroundColor: 'rgba(220, 220, 220, 0.2)',
                    borderColor: 'rgba(220, 220, 220, 1)',
                    pointBackgroundColor: 'rgba(220, 220, 220, 1)',
                    pointBorderColor: '#fff',
                    pointHighlightFill: '#fff',
                    pointHighlightStroke: 'rgba(220, 220, 220, 1)',
                    data: [65, 59, 90, 81, 56, 55, 40],
                  },
                  {
                    label: 'My Second dataset',
                    backgroundColor: 'rgba(151, 187, 205, 0.2)',
                    borderColor: 'rgba(151, 187, 205, 1)',
                    pointBackgroundColor: 'rgba(151, 187, 205, 1)',
                    pointBorderColor: '#fff',
                    pointHighlightFill: '#fff',
                    pointHighlightStroke: 'rgba(151, 187, 205, 1)',
                    data: [28, 48, 40, 19, 96, 27, 100],
                  },
                ],
              }}
            />
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  )
}

export default Charts
