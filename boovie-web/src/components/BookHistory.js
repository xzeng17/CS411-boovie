import React from "react";
import { Redirect } from 'react-router-dom'

function BookHistory(props) {
    const {isLoggedIn} = props;

    if (!isLoggedIn) {
        return <Redirect to='/Login' />
    }

    return (
        <div>
            Book History Page
        </div>
    )
}

export default BookHistory;