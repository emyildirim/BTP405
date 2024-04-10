import { Container } from 'react-bootstrap';
import styles from '../styles/Footer.module.css'; // Assuming you are using CSS modules

export default function Footer() {
    return (
        <footer className={`${styles.footer} py-3 bg-dark`}>
            <Container>
                <span className="text-light">&copy;2024 by Erkam Yildirim</span>
            </Container>
        </footer>
    );
}
