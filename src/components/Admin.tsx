import React, {useState, useEffect} from 'react';

const Admin = () => {
    const [mystate, setMyState] = useState(0);
    
    return (
        <>
            <h2>Admin</h2>
            <div>
                Content goes here. mystate is {mystate}.
            </div>
        </>
    );
}
export default Admin;
