import React from 'react';
import { Admin, ContentManager, Login, Navbar, Search } from './components'
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';

const App = () => {
    return (
        <>
            <h1>arctic geoportal</h1>
            <Navbar/>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<ContentManager />} />
                    <Route path="/admin" element={<Admin />} />
                    <Route path="/search" element={<Search />} />
                    <Route path="/login" element={<Login />} />
                </Routes>
            </BrowserRouter>
        
        </>
    );
}
export default App;
