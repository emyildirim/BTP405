// lib/userData.js
import { getToken } from './authenticate';

async function request(url, method, body = null) {
    const token = getToken();
    const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
    };
    const config = {
        method: method,
        headers: headers,
    };
    if (body) {
        config.body = JSON.stringify(body);
    }
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${url}`, config);
    if (response.ok) {
        return response.json();
    } else if (response.status !== 501){
        const { message } = await response.json();
        throw new Error(message);
    } else {
        throw new Error('Server responded with an error');
    }
}

// Fetch user profile
export async function getUserProfile() {
    return request(`/profile`, 'GET');
}

// Update user profile
export async function updateUserProfile(profileData) {
    return request(`/profile`, 'PUT', profileData);
}

// Fetch all reservations
export async function getAllReservations() {
    return request(`/reservations`, 'GET');
}

// Fetch specific reservation
export async function getReservationById(id) {
    return request(`/reservations/${id}`, 'GET');
}

// Fetch reservations due today
export async function getReservationsDueToday() {
    return request(`/reservations/due`, 'GET');
}

// Create new reservation
export async function createReservation(reservationData) {
    return request(`/reservations`, 'POST', reservationData);
}

// Update specific reservation
export async function updateReservation(id, reservationData) {
    return request(`/reservations/${id}`, 'PUT', reservationData);
}

// Delete specific reservation
export async function deleteReservation(id) {
    return request(`/reservations/${id}`, 'DELETE');
}
