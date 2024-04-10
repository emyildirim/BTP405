import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { Form, Button, Container, Alert, Card } from 'react-bootstrap';
import { getUserProfile, updateUserProfile } from '../lib/userData'; // Adjust the path as necessary

export default function Profile() {
    const [user, setUser] = useState({});
    const [error, setError] = useState('');
    const router = useRouter();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const profileData = await getUserProfile();
                setUser(profileData);
            } catch (error) {
                setError('Failed to load profile data');
                router.push('/login');
            }
        };

        fetchProfile();
    }, [router]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        try {
            await updateUserProfile(user);
            alert('Profile updated successfully');
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <Container>
            <Card bg="light" className="mt-5">
                <Card.Body><h2>Profile</h2>Enter to update your profile:</Card.Body>
            </Card>
            <br/>
            <p>
                <strong>Email:</strong> {user.email}
            </p>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="fullname">
                    <Form.Label>Full Name</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter your full name"
                        value={user.fullname || ''}
                        onChange={(e) => setUser({ ...user, fullname: e.target.value })}
                        style={{ width: '50%' }} 
                    />
                </Form.Group>
                <Form.Group controlId="phone">
                    <Form.Label>Phone</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter your phone number"
                        value={user.phone || ''}
                        onChange={(e) => setUser({ ...user, phone: e.target.value })}
                        style={{ width: '50%' }}
                    />
                </Form.Group>
                <br />
                <Button variant="primary" type="submit">
                    Update Profile
                </Button>
            </Form>
            <br />
            {error && <Alert variant="danger">{error}</Alert>}
        </Container>
    );
}