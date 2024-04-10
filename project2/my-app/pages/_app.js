import '../styles/globals.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import RouteGuard from '../components/RouteGuard';
import NavigationBar from '../components/Navbar';
import Footer from '../components/Footer';

export default function MyApp({ Component, pageProps }) {
  return (
    <RouteGuard>
      <NavigationBar />
      <main>
        <Component {...pageProps} />
      </main>
      <Footer />
    </RouteGuard>
  );
}
