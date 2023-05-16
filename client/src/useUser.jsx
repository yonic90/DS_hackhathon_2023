import { useState } from 'react';

const useUser = () => {
    const getUser = () => {
        const userString = localStorage.getItem('User');
        const user = JSON.parse(userString);
        return user?.id
    };
    const [user, setUser] = useState(getUser());
    const saveUser = user => {
        localStorage.setItem('User', JSON.stringify(user));
        setUser(user);
    };

    return {
        setUser: saveUser,
        user
    }

}

export default useUser