import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter } from 'react-router-dom';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
 <React.StrictMode>
 <App />
 </React.StrictMode>
);
ReactDOM.render(
<React.StrictMode> [DCB5][JL6]
<BrowserRouter>
<App />
</BrowserRouter>
</React.StrictMode>,
document.getElementById('root')
);

reportWebVitals();