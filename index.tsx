import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './src/App';

//import configureStore from './src/configureStore'
//const { store } = configureStore()

// React 18 format

const container = document.getElementById('app');
const root = createRoot(container!);
root.render(
    <App title="arctic openportal"/>
);
