// pages/register.js
import { useState } from 'react';
import { useRouter } from 'next/router';
import { Form, Button, Container, Alert, Row, Col, Card } from 'react-bootstrap';
import { registerUser } from '../lib/authenticate';

export default function Register() {
    const [fullname, setFullname] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await registerUser({ fullname, email, phone, password, confirmPassword });
            router.push('/login'); // Redirect to main after successful registration
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <Container style={{ width: '600px' }}>
            <Card bg="light" className="mt-5">
                <Card.Body><h2>Register</h2>Register for an account:</Card.Body>
            </Card>
            <br />
            <Form onSubmit={handleSubmit}>
                <Row className="mb-3">
                    <Form.Group as={Col} controlId="fullname">
                        <Form.Label>Full Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Enter Full Name"
                            onChange={(e) => setFullname(e.target.value)}
                            autoComplete="off"
                        />
                    </Form.Group>
                </Row>
                <Row className="mb-3">
                    <Form.Group as={Col} controlId="email">
                        <Form.Label>Email</Form.Label>
                        <Form.Control
                            type="email"
                            placeholder="example@domain.com"
                            onChange={(e) => setEmail(e.target.value)}
                            autoComplete="off"
                        />
                    </Form.Group>
                </Row>
                <Row className="mb-3">
                    <Form.Group as={Col} controlId="phone">
                        <Form.Label>Phone Number</Form.Label>
                        <Form.Control
                            type="tel"
                            placeholder="1231231234"
                            onChange={(e) => setPhone(e.target.value)}
                            autoComplete="off"
                        />
                    </Form.Group>
                </Row>
                <Row className="mb-3">
                    <Form.Group as={Col} controlId="password">
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            type="password"
                            onChange={(e) => setPassword(e.target.value)}
                            autoComplete="off"
                        />
                    </Form.Group>
                </Row>
                <Row className="mb-3">
                    <Form.Group as={Col} controlId="confirmPassword">
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control
                            type="password"
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            autoComplete="off"
                        />
                    </Form.Group>
                </Row>
                <Button variant="dark" style={{ width: '150px' }} type="submit">Register</Button>
            </Form>
            <br />
            {error && <Alert variant="danger">{error}</Alert>}
        </Container>
    );
}