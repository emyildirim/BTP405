import { jwtDecode } from 'jwt-decode';

// Set token in localStorage
export function setToken(token) {
    localStorage.setItem('access_token', token);
}

// Get token from localStorage
export function getToken() {
    return localStorage.getItem('access_token');
}

// Remove token from localStorage
export function removeToken() {
    localStorage.removeItem('access_token');
}

// Decode token to read payload
export function readToken() {
    const token = getToken();
    return token ? jwtDecode(token) : null;
}

// Check if user is authenticated
export function isAuthenticated() {
    const token = readToken();
    return !!token;
}

// Authenticate user
export async function authenticateUser(userName, password) {
    let res;
    try {
        res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                username: userName,
                password: password
            }),
        });
    } catch (error) {
        console.error('Network error:', error);
        throw new Error('Network error when trying to log in');
    }

    if (!res.ok) {
        let errorText;
        try {
            // Attempt to parse a JSON error response
            const errorData = await res.json();
            errorText = errorData.message;
        } catch {
            // Fallback to text response
            errorText = await res.text();
        }
        throw new Error(errorText || `Authentication error: ${res.status} ${res.statusText}`);
    }

    const data = await res.json();
    setToken(data.token);
    return true;
}


// Register user
export async function registerUser(userData) {
    if(userData.password !== userData.confirmPassword) {
        throw new Error('Passwords do not match');
    }
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            type_id: 1,
            fullname: userData.fullname,
            email: userData.email,
            phone: userData.phone,
            password: userData.password,
        }),
    });

    if (res.status === 200 || res.status === 201) {
        return await res.json();
    } else {
        const error = await res.text();
        throw new Error(error || 'Registration failed');
    }
}
