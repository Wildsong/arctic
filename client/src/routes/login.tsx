import { Card, Button } from 'react-bootstrap'

const Login = () => {
    return (
      <Card>
        <Card.Title>
          Log in
        </Card.Title>
        <Card.Text>
          When I implement logging in, here is
          where you will do that.
          
          username <input name="username"/>
          password <input name="password"/>
          <Button>Log in</Button>
          </Card.Text>
      </Card>
    );
}
export default Login