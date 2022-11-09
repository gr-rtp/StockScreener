import React, { useState } from 'react';

export default function TextBtn({ text = 'Click me!', acitve = false }) {

    return (
        <button className="">{ text }</button>
    )
}