import { Card } from 'react-bootstrap'
import DataGrid from 'react-data-grid'
import 'react-data-grid/lib/styles.css'
// Refer to https://www.npmjs.com/package/react-data-grid

const columns = [
  { key: 'id', name: 'ID' },
  { key: 'product', name: 'Product' },
  { key: 'user', name: 'User' },
  { key: 'checkout', name: 'Checked out'}
];

const rows = [
  { id: 0, product: 'ArcGIS Pro', user: 'User 1', checkout: '2023-01-01' },
  { id: 1, product: 'ArcMap', user: 'User 2', checkout: '2023-10-10' },
  { id: 2, product: 'ArcMap', user: 'User 3', checkout: '2023-10-11' }
];

const Licenses = () => {
    return (
        <Card>
          <Card.Title>
            ArcGIS Licenses
          </Card.Title>
          <Card.Text>
          <DataGrid columns={columns} rows={rows} />
          </Card.Text>
        </Card>
      );
}
export default Licenses