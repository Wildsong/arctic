import React, {useState, useEffect} from 'react';  // eslint-disable-line no-unused-vars
import {getItem} from '@esri/arcgis-rest-portal'

const ListItems = () => {
    let id = "0"

    const url = "https://delta.co.clatsop.or.us/server/rest/"

    getItem(id)
        .then(response => {
            console.log(response.title)
        });

    return (
        <>
        stuff in a list
        </>
    );
}
export default ListItems;
