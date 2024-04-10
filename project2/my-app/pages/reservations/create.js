// pages/reservations/create.js
import { useState } from 'react';
import { useRouter } from 'next/router';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { createReservation } from '../../lib/userData';

export default function CreateReservation() {
    const [reservationDate, setReservationDate] = useState('');
    const [reservationTime, setReservationTime] = useState('');
    const [numberOfGuests, setNumberOfGuests] = useState(1);
    const [error, setError] = useState('');
    const router = useRouter();

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            await createReservation({
                reservation_date: reservationDate,
                reservation_time: reservationTime,
                number_of_guests: numberOfGuests,
            });
            router.push('/reservations');
        } catch (error) {
            setError(error.message);
        }
    };


    return (
        <Container style={{ width: '500px' }}>
            <h2 className="mt-5 mb-3">Create a New Reservation</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label>Date</Form.Label>
                    <Form.Control type="date" value={reservationDate} onChange={(e) => setReservationDate(e.target.value)} required />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Time</Form.Label>
                    <Form.Control type="time" value={reservationTime} onChange={(e) => setReservationTime(e.target.value)} required />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Number of Guests</Form.Label>
                    <Form.Control type="number" min="1" value={numberOfGuests} onChange={(e) => setNumberOfGuests(e.target.value)} required />
                </Form.Group>

                <Button variant="primary" type="submit">Submit Reservation</Button>
            </Form>
            <br />
            {error && <Alert variant="danger">{error}</Alert>}
        </Container>
    );
}
