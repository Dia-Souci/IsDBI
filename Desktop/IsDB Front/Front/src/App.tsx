import { Outlet } from 'react-router-dom';
import { Toaster } from '@/components/ui/toaster';
import { ThemeProvider } from '@/components/ThemeProvider';
import { Layout } from '@/components/layout/Layout';

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <Layout>
        <Outlet />
      </Layout>
      <Toaster />
    </ThemeProvider>
  );
}

export default App;