import { Button, Container, Row, Col } from 'react-bootstrap';
import Link from 'next/link';
import Image from 'next/image';

export default function Home() {
  return (
    <Container fluid className="min-vh-100 d-flex flex-column justify-content-center">
      <Row className="justify-content-center">
        <Col md={6} className="text-center">
          <h1>Welcome to Our Restaurant</h1>
          <p>This is the best place to enjoy exquisite dishes and make reservations for your memorable moments.</p>
          <Link href="/reservations/create" passHref legacyBehavior>
            <Button variant="dark">Make a Reservation Now</Button>
          </Link>
        </Col>
      </Row>
      <Row className="justify-content-center my-5">
        <Col md={6} className="text-center">
          <h2>About Us</h2>
          <p>Discover our variety of food and what makes us unique. Anytime a go-to spot for food lovers.</p>
        </Col>
      </Row>
      <Row className="justify-content-center my-5">
        <Col md={3} className="text-center">
          <h2>Contact Us</h2>
          <p>
            405 BTP Course, Toronto, Yum <br />
            +1 (234) 567-890 <br />
            Open daily from 8am to 10pm
          </p>
          <Image src="/aboutUsIcon.jpg" alt="Restaurant Image" width={150} height={125} />

        </Col>
      </Row>
    </Container>
  );
}
