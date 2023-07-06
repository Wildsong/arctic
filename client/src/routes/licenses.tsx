import { Card } from 'react-bootstrap'
import DataGrid from 'react-data-grid'
import 'react-data-grid/lib/styles.css'
// Refer to https://www.npmjs.com/package/react-data-grid
import { useQuery } from '@apollo/client';
import { GET_LICENSES, PING } from '../queries';

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


const ShowLicenses = () => {
    const { loading, error, data } = useQuery(GET_LICENSES);
    if (error) return <>Error : {error.message}</>
    if (loading) return <>Loading...</>

    let columns = data.licenses.map( ({id,product,user,checkout}) => {
        [
            { key: 'id', name: id },
            { key: 'product', name: product },
            { key: 'user', name: user },
            { key: 'checkout', name: checkout }
        ]
    });
    console.log("Licenses", columns)

    return (
      <>
      nothin
      </>
    );
    //        <DataGrid columns={columns} rows={rows} />

}

const Ping = () => {
    const { loading, error, data } = useQuery(PING);
    if (loading) return <>Server starting up...</>;
    if (error) return <>Connect failed: {error.message}</>;
    console.log('Ping', data.ping)
    return <>server timestamp: {data.ping}</>
}


const Licenses = () => {
    return (
        <>
        <Card>
          <Card.Title>
            ArcGIS Licenses
          </Card.Title>
          <Card.Text>
          <ShowLicenses/>
          </Card.Text>
          <Card.Text>
          <Ping />
          </Card.Text>
        </Card>

        </>
    );
}
export default Licenses