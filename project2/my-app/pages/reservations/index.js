// pages/reservations/index.js
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { Container, Table, Button, Card } from 'react-bootstrap';
import { getAllReservations, deleteReservation } from '../../lib/userData';

export default function Reservations() {
    const [reservations, setReservations] = useState([]);
    const [isStaff, setIsStaff] = useState(false);
    const [error, setError] = useState('');
    const router = useRouter();

    useEffect(() => {
        const fetchReservations = async () => {
            try {
                const data = await getAllReservations();
                setReservations(data);
                setIsStaff(data.every(reservation => 'fullname' in reservation));
            } catch (error) {
                if (error.message === "No reservations found for the user") {
                    setError('No reservations found.');
                    setReservations([]);
                } else {
                    setError('Failed to load reservations');
                    router.push('/login');
                }
            }
        };

        fetchReservations();

        const handleRouteChange = () => {
            fetchReservations();
        };

        router.events.on('routeChangeComplete', handleRouteChange);

        return () => {
            router.events.off('routeChangeComplete', handleRouteChange); // Cleanup event listener
        };
    }, [router]);

    
    const handleDelete = async (reservationId) => {
        const confirmDeletion = confirm('Are you sure you want to delete this reservation?');
        if (!confirmDeletion) return;

        try {
            await deleteReservation(reservationId);
            setReservations(reservations.filter(reservation => reservation.reservation_id !== reservationId));
        } catch (error) {
            setError(error.message);
        }
    };


    return (
        <Container>
            <Card bg="light" className="mt-5">
                <Card.Body><h2>{isStaff ? "Staff Dashboard" : "Customer Dashboard"}</h2>{isStaff ? "Modify reservation below:" : "Modify or Create reservation below:"}</Card.Body>
            </Card>
            <br />
            {reservations.length > 0 ? (
                <>
                    <Table striped bordered hover>
                        <thead>
                            <tr>
                                <th>#</th>
                                {isStaff && <th>Customer</th>}
                                <th>Date</th>
                                <th>Time</th>
                                <th>Guests</th>
                                {!isStaff && <th>Created At</th>}
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {reservations.map((reservation, index) => (
                                <tr key={reservation.reservation_id}>
                                    <td>{index + 1}</td>
                                    {isStaff && <td>{reservation.fullname}</td>}
                                    <td>{reservation.reservation_date}</td>
                                    <td>{reservation.reservation_time}</td>
                                    <td>{reservation.number_of_guests}</td>
                                    {!isStaff && <td>{reservation.created_at}</td>}
                                    <td>
                                        <Button variant="primary" size="sm" onClick={() => router.push(`/reservations/edit/${reservation.reservation_id}`)}>Edit</Button>
                                        {' '}
                                        <Button variant="danger" size="sm" onClick={() => handleDelete(reservation.reservation_id)}>Delete</Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                    {error && <div className="alert alert-danger" role="alert">{error}</div>}
                </>
            ) : (
                <div>
                    {error && <div className="alert alert-info" role="alert">{error}</div>} 
                </div>
            )}
            {!isStaff && (
                <Button variant="success" size="sm" onClick={() => router.push('/reservations/create')}>Create Reservation</Button>            )}
        </Container>
    );
}
