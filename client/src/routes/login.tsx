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
          <form>
          <div>username <input name="username"/></div>
          <div>password <input name="password"/></div>
          <Button>Log in</Button>
          </form>
        </Card.Text>
      </Card>
    );
}
export default Login