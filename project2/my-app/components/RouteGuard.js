import { useRouter } from 'next/router';
import { isAuthenticated } from '@/lib/authenticate';
import { useEffect, useState } from 'react';

const PUBLIC_PATHS = ['/login', '/', '/_error', '/register'];

export default function RouteGuard({ children }) {
    const router = useRouter();
    const [authorized, setAuthorized] = useState(false);

    useEffect(() => {

        const authCheck = (url) => {
            // Splitting to ignore query parameters
            const path = url.split('?')[0];
            if (!isAuthenticated() && !PUBLIC_PATHS.includes(path)) {
                // Delaying redirection to ensure state updates are processed
                setTimeout(() => router.push('/login'), 0);
                setAuthorized(false);
            } else {
                setAuthorized(true);
            }
        };

        const handleRouteChange = (url) => {
            authCheck(url);
        };

        authCheck(router.pathname);
        router.events.on('routeChangeStart', handleRouteChange);

        return () => {
            router.events.off('routeChangeStart', handleRouteChange);
        };
    }, [router]);

    if (!authorized) {
        return null;
    }

    return <>{children}</>;
}