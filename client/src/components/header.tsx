import { useState } from 'react'
import Card from 'react-bootstrap/Card'
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import Licenses from '../routes/licenses'
import Contact from '../routes/contact'
import Login from '../routes/login'

const Header = () => {
  const [key, setKey] = useState('home');

    return (
        <>
        <Card style={{minWidth: '48rem', flexGrow: 1, margin:'0rem', minHeight:'32rem'}}>
          <Card.Body>
          <h1>Arctic Spa</h1>
            <Tabs
              id="arctic-spa"
              activeKey={key}
              onSelect={(k) => setKey(k)}
              className="mb-3"
            >
              <Tab eventKey="home" title="Home">
                Tab content for Home
              </Tab>
              <Tab eventKey="licenses" title="Licenses">
                <Licenses/>
              </Tab>
              <Tab eventKey="contact" title="Contact">
                <Contact />
              </Tab>
              <Tab eventKey="user" title="Log in">
                <Login />
              </Tab>
            </Tabs>    
          </Card.Body>
        </Card>
        </>
      );
}
export default Header