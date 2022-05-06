import React from "react";
import { BrowserRouter as Router, Route, Routes, NavLink } from 'react-router-dom';
import { Container } from 'react-bootstrap'
import { Admin, ContentManager, Login, Search } from '.'

const Navbar = () => {
    return (
        <>
            <Router>
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
            </Router>
        </>
    )
}
export default Navbar;