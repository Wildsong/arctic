import { useState } from 'react'
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import { Header, Footer } from './components'
import Licenses from './routes/licenses'
import Contact from './routes/contact'
import Login from './routes/login'

import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css'

const App = () => {
    const [key, setKey] = useState('home');

  return (
    <>      <Header/>
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

      <Footer />

    </>
  )
}
export default App
