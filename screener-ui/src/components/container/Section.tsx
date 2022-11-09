import React from 'react';

type Props = {
    children: React.ReactNode
}

export default function Section({ children }: Props) {

    return (
        <div className='m-4 rounded-lg shadow-md p-2'>
            {children}
        </div>
    )
}