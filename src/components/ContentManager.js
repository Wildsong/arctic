import React, {useState, useEffect} from 'react';  // eslint-disable-line no-unused-vars
import {getItem} from '@esri/arcgis-rest-portal'

const ContentManager = () => {
    let id = "0"

    const url = "https://delta.co.clatsop.or.us/"

    getItem(id)
        .then(response => {
            console.log(response.title)
        });

    return (
        <>
            <h2>Content Manager</h2>
            <div>
                Upload
            </div>
        </>
    );
}
export default ContentManager;
