import React, { useState } from "react";
import { Container, Button, Row, Col, Form, FormControl } from 'react-bootstrap'

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [portalUrl, setPortalUrl] = useState("https://delta.co.clatsop.or.us/");
    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Login " + portalUrl + " " + username + " " + password);
    }
    return (
        <Container>
            <Row>
                <Col md="4">
                    <h1>Log In</h1>
                    <Form>
                        <Form.Group controlId="portalUrlId">
                            <Form.Label>portal</Form.Label>
                            <Form.Control
                                type="text"
                                name="portalUrl"
                                placeholder="Enter portal URL"
                                value={portalUrl}
                                onChange={e=>setPortalUrl(e.target.value)}
                            />
                        </Form.Group>
                        <Form.Group controlId="usernameId">
                            <Form.Label>user</Form.Label>
                            <Form.Control
                                type="username"
                                name="username"
                                placeholder="Enter user name"
                                value={username}
                                onChange={e=>setUsername(e.target.value)}
                            />
                        </Form.Group>
                        <Form.Group controlId="passwordId">
                            <Form.Label>password</Form.Label>
                            <Form.Control
                                type="password"
                                name="password"
                                placeholder="Enter password"
                                value={password}
                                onChange={e=>setPassword(e.target.value)}
                            />
                            <p className="mt-2">
                                Forgot your password? Call x1152
                            </p>
                        </Form.Group>
                    </Form>
                    <Button variant="primary" type="submit" onClick={handleSubmit}>
                        Sign in now
                    </Button>
                </Col>
            </Row>
        </Container>
    )
}
export default Login;