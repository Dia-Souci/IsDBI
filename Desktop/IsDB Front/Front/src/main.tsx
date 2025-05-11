import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import App from './App.tsx';
import './index.css';

// Pages
import { HomePage } from './pages/HomePage.tsx';
import { ChatPage } from './pages/ChatPage.tsx';
import { QuestionPage } from './pages/QuestionPage.tsx';
import { SimpleChatPage } from './pages/SimpleChatPage.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route index element={<HomePage />} />
          <Route path="chat" element={<ChatPage />} />
          <Route path="question" element={<QuestionPage />} />
          <Route path="simple-chat" element={<SimpleChatPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>
);