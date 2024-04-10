import React, {useState, useEffect} from 'react';

const Search = () => {
    const [mystate, setMyState] = useState(0);
    
    return (
        <>
            <h2>Search</h2>
            <div>
                Content goes here. mystate is {mystate}.
            </div>
        </>
    );
}
export default Search;
