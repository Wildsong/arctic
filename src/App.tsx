import React from 'react';
import PropTypes from 'prop-types'
import {ListItems, Navbar} from './components'

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';

const App = ({title}) => {
    return (
        <>
        <h1>{title}</h1>
        <Navbar/>
        <ListItems/>
        </>
    );
}
App.propTypes = {
    "title": PropTypes.string.isRequired
};
export default App;
