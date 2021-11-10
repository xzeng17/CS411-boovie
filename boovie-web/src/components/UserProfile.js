import React from "react";

function UserProfile(props) {
    const {isLoggedIn, userRole} = props;

    return (
        <div>
            <div>
                User Profile Page
            </div>

            {isLoggedIn ? 
                <div>
                    You are logged in as {userRole}!
                </div>
                :
                <div>
                    Please Login first!
                </div>
            }
            
        </div>
    )
}

export default UserProfile;