// fake vaccination sites until the backend has a sites endpoint
const mockSites = [
  {
    id: '1',
    name: 'Riverside Health Clinic',
    address: '120 River Rd',
    location: { type: 'Point', coordinates: [-74.006, 40.7128] },
    capacity: 300,
    active: true,
  },
  {
    id: '2',
    name: 'Main Street Pharmacy',
    address: '45 Main St',
    location: { type: 'Point', coordinates: [-73.995, 40.7306] },
    capacity: 120,
    active: true,
  },
  {
    id: '3',
    name: 'Northside Community Center',
    address: '9 North Ave',
    location: { type: 'Point', coordinates: [-73.9442, 40.8116] },
    capacity: 200,
    active: false,
  },
  {
    id: '4',
    name: 'Eastview Medical Office',
    address: '310 East Blvd',
    location: { type: 'Point', coordinates: [-73.9352, 40.7306] },
    capacity: 150,
    active: true,
  },
]

export default mockSites
