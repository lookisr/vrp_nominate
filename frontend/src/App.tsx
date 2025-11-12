import { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { NavBar } from './components/NavBar';
import { MainPage } from './pages/MainPage';
import { NominationsPage } from './pages/NominationsPage';
import { NominationVotingPage } from './pages/NominationVotingPage';
import { VoteConfirmationPage } from './pages/VoteConfirmationPage';
import { ResultsPage } from './pages/ResultsPage';
import { NominationResultsPage } from './pages/NominationResultsPage';

// Инициализация Telegram Web App SDK
declare global {
  interface Window {
    Telegram?: {
      WebApp: {
        ready: () => void;
        expand: () => void;
        close: () => void;
        version: string;
        platform: string;
        colorScheme: 'light' | 'dark';
        themeParams: {
          bg_color?: string;
          text_color?: string;
          hint_color?: string;
          link_color?: string;
          button_color?: string;
          button_text_color?: string;
        };
      };
    };
  }
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  useEffect(() => {
    // Инициализация Telegram Web App
    if (window.Telegram?.WebApp) {
      window.Telegram.WebApp.ready();
      window.Telegram.WebApp.expand();
    }
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/" element={<MainPage />} />
            <Route path="/nominations" element={<NominationsPage />} />
            <Route path="/nominations/:id" element={<NominationVotingPage />} />
            <Route path="/vote/confirm" element={<VoteConfirmationPage />} />
            <Route path="/results" element={<ResultsPage />} />
            <Route path="/results/:id" element={<NominationResultsPage />} />
          </Routes>
          <NavBar />
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
