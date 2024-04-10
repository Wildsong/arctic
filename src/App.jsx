import React from 'react';
import Root from './Root';
import { Route, Routes, NavLink } from 'react-router-dom';
import { Admin, ContentManager, Login, Search } from './components'

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';
import { Form } from 'react-bootstrap';

const App = () => {
    return (
        <>
            <h1>arctic geoportal</h1>

            <Root>
                <Routes>
                    <Route path="/" element={<ContentManager />} />
                    <Route path="/admin" element={<Admin />} />
                    <Route path="/search" element={<Search />} />
                    <Route path="/login" element={<Login />} />
                </Routes>
                <NavLink to="/">Content Manager</NavLink>
                <NavLink to="/admin">Admin</NavLink>
                <NavLink to="/search">Search</NavLink>
                <NavLink to="/login">Login</NavLink>
                Signed in to: Delta
            </Root>
        </>
    );
}
export default App;
