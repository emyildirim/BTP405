import Link from 'next/link';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { isAuthenticated, removeToken } from '../lib/authenticate';

export default function NavigationBar() {
    const router = useRouter();
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);
    const [userName, setUserName] = useState('');

    useEffect(() => {
        const handleRouteChange = () => {
            setIsLoggedIn(isAuthenticated());
            closeExpanding();
        };

        handleRouteChange();
        router.events.on('routeChangeComplete', handleRouteChange);

        return () => {
            router.events.off('routeChangeComplete', handleRouteChange);
        };
    }, [router.events]);

    const logout = () => {
        removeToken();
        setIsLoggedIn(false); 
        router.push('/login');
        closeExpanding();
    };

    const toggleExpanding = () => {
        setIsExpanded(!isExpanded)
    }

    const closeExpanding = () => {
        setIsExpanded(false)
    }

    return (
        <Navbar bg="py-3 navbar-dark bg-dark" expanded={isExpanded}>
            <Container>
                <Navbar.Brand href="/">Restaurant Reservation</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" onClick={toggleExpanding} />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto flex-grow-1">
                        {isLoggedIn && (
                            <>
                                <Link href="/reservations" passHref legacyBehavior>
                                    <Nav.Link active={router.pathname === "/reservations"} onClick={closeExpanding}>Reservations</Nav.Link>
                                </Link>
                                <Link href="/profile" passHref legacyBehavior>
                                    <Nav.Link active={router.pathname === "/profile"} onClick={closeExpanding}>Profile</Nav.Link>
                                </Link>
                            </>
                        )}
                    </Nav>
                    <Nav>
                        {isLoggedIn ? (
                            <NavDropdown title="Account" id="collapsible-nav-dropdown">
                                <NavDropdown.Item onClick={logout}>Logout</NavDropdown.Item>
                            </NavDropdown>
                        ) : (
                            <>
                                <Link href="/login" passHref legacyBehavior>
                                        <Nav.Link active={router.pathname === "/login"} onClick={closeExpanding}>Login</Nav.Link>
                                </Link>
                                    <Link href="/register" passHref legacyBehavior>
                                        <Nav.Link onClick={closeExpanding} active={router.pathname === "/register"}>Register</Nav.Link>
                                </Link>
                            </>
                        )}
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}
