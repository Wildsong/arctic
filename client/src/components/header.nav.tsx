import Card from 'react-bootstrap/Card'
import Nav from 'react-bootstrap/Nav'
import Licenses from '../routes/licenses'
import Contact from '../routes/contact'
import Login from '../routes/login'

const Header = () => {
    return (
        <>
        <Card>
          <Card.Body>
          <h1>Arctic Spa</h1>
            <Nav variant="tags"
              id="arctic-spa"
              className="mb-3"
              defaultActiveKey={"#home"}
            >
              <Nav.Item>
                <Nav.Link href="#home" title="Home">
                  Content for Home
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link href="#licenses" title="Licenses">
                  <Licenses/>
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link href="#contact" title="Contact">
                  <Contact />
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link href="#user" title="Log in">
                  <Login />
                </Nav.Link>
              </Nav.Item>
            </Nav>
          </Card.Body>
        </Card>
        </>
      );
}
export default Header