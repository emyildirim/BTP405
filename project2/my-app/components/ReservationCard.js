// components/ReservationCard.js
import { Card, Button } from 'react-bootstrap';

export default function ReservationCard({ reservation, onDelete, onEdit }) {
    return (
        <Card style={{ width: '18rem', marginBottom: '1rem' }}>
            <Card.Body>
                <Card.Title>Reservation for {reservation.number_of_guests} Guests</Card.Title>
                <Card.Text>
                    <strong>Date:</strong> {reservation.reservation_date}<br />
                    <strong>Time:</strong> {reservation.reservation_time}
                </Card.Text>
                <Button variant="primary" onClick={() => onEdit(reservation.reservation_id)}>Edit</Button>
                {' '}
                <Button variant="danger" onClick={() => onDelete(reservation.reservation_id)}>Delete</Button>
            </Card.Body>
        </Card>
    );
}
