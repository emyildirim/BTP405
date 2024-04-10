import { useState } from 'react';
import { useRouter } from 'next/router';
import { Form, Button, Container, Alert, Card } from 'react-bootstrap';
import { authenticateUser } from '../lib/authenticate'; // Adjust the path as necessary

export default function Login() {
    const [userName, setUserName] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const isAuthenticated = await authenticateUser(userName, password);
            if (isAuthenticated) {
                router.push('/profile');
            } else {
                setError('Authentication failed. Please check your credentials.');
            }
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <Container style={{ width: '600px' }}>
            <Card bg="light" className="mt-5">
                <Card.Body><h2>Login</h2>Enter your login information below:</Card.Body>
            </Card>
            <br />
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label className="col-sm-2 col-form-label">Email</Form.Label>
                        <Form.Control
                            name="username"
                            type="text"
                            value={userName}
                            onChange={(e) => setUserName(e.target.value)}
                            required
                            autoComplete="off"
                        />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label className="col-sm-2 col-form-label">Password</Form.Label>
                        <Form.Control
                            name="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            autoComplete="off"
                        />
                </Form.Group>
                <Button variant="dark" style={{ width: '150px' }} type="submit">Login</Button>
            </Form>
            <br />
            {error && <Alert variant="danger">{error}</Alert>}
        </Container>
    );
}