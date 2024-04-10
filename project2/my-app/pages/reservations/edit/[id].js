// pages/reservations/edit/[id].js
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { getReservationById, updateReservation } from '@/../../lib/userData';

export default function EditReservation() {
    const [reservation, setReservation] = useState({
        reservation_date: '',
        reservation_time: '',
        number_of_guests: 1,
    });
    const [error, setError] = useState('');
    const router = useRouter();
    const { id } = router.query;

    useEffect(() => {
        const fetchReservation = async () => {
            try {
                const data = await getReservationById(id);
                setReservation(data);
            } catch (error) {
                setError('Failed to load reservation');
                router.push('/login');
            }
        };

        if (id) {
            fetchReservation();
        }
    }, [id, router]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        const updatedReservation = {
            ...reservation,
            reservation_time: convertTo24HourFormat(reservation.reservation_time),
        };
        console.log(updatedReservation.reservation_time)
        try {
            await updateReservation(id, updatedReservation);
            router.push('/reservations');
        } catch (error) {
            setError(error.message);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setReservation(prevState => ({
            ...prevState,
            [name]: value,
        }));
    };

    const convertTo24HourFormat = (timeStr) => {
        const [time, modifier] = timeStr.split(' ');
        let [hours, minutes] = time.split(':');

        if (hours === '12') {
            hours = modifier === 'AM' ? '00' : '12';
        } else if (modifier === 'PM') {
            hours = parseInt(hours, 10) + 12;
        }

        return `${hours.toString().padStart(2, '0')}:${minutes}`;
    };

    const formatTimeForInput = (timeStr) => {
        if (!timeStr) return '';

        if (timeStr.match(/^\d{2}:\d{2}$/)) {
            return timeStr;
        }

        const [time, modifier] = timeStr.split(' ');
        if (modifier) {
            return convertTo24HourFormat(timeStr);
        }

        return timeStr;
    };

    return (
        <Container style={{ width: '500px' }}>
            <h2 className="mt-5 mb-3">Edit Reservation</h2>
            <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                    <Form.Label>Date</Form.Label>
                    <Form.Control type="date" name="reservation_date" value={reservation.reservation_date} onChange={handleChange} required />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Time</Form.Label>
                    <Form.Control type="time" name="reservation_time" value={formatTimeForInput(reservation.reservation_time)} onChange={handleChange} required />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Number of Guests</Form.Label>
                    <Form.Control type="number" min="1" name="number_of_guests" value={reservation.number_of_guests.toString()} onChange={handleChange} required />
                </Form.Group>

                <Button variant="primary" type="submit">Update Reservation</Button>
            </Form>
            <br/>
            {error && <Alert variant="danger">{error}</Alert>}
        </Container>
    );
}
