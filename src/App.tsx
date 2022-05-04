import React from 'react';
import PropTypes from 'prop-types'
import {BrowserRouter as Router, Route, NavLink} from "react-router-dom" // eslint-disable-line no-unused-vars
import {ListItems} from '../components'

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

const App = ({title}) => {
    return (
        <>
        <h1>{title}</h1>

        <ListItems/>
        </>
    );
}
App.propTypes = {
    "title": PropTypes.string.isRequired
};
export default App;
