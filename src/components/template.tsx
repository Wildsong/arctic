import React, {useState, useEffect} from 'react';
import { Container } from 'react-bootstrap'

const NewComponent = () => {
    const [mystate, setMyState] = useState(0);
    
    return (
        <Container>
            <h2>NewComponent</h2>
            <div>
                Content goes here. mystate is {mystate}.
            </div>
        </Container>
    );
}
export default NewComponent;
