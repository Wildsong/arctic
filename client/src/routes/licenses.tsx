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

import { useQuery } from '@apollo/client';
import { GET_LICENSES, PING } from './queries';

const ShowInstruments = ({ querytype, lastname }) => {
    const { loading, error, data } = useQuery(GET_INSTRUMENTS, {
        variables: {querytype,lastname}
    });
    if (error) return <p>Error : {error.message}</p>;
    if (loading) return <p>Loading...</p>;
  
    return data.instruments.map(({ id, firstname, lastname, recording_date }) => (
      <div key={id}>
        {id} {firstname} {lastname} {recording_date} <br />
      </div>
    ));
}

const Ping = () => {
    const { loading, error, data } = useQuery(PING);
    if (loading) return <>Server starting up...</>;
    if (error) return <>Connect failed: {error.message}</>;
    return (
        <font color="lightgrey">{data.ping}</font>
    );
}


const Licenses = () => {
    return (
        <Card>
          <Card.Title>
            ArcGIS Licenses
          </Card.Title>
          <Card.Text>
          <DataGrid columns={columns} rows={rows} />
          </Card.Text>
          <Ping /><br />
        </Card>
      );
}
export default Licenses