import React, { useState } from 'react';
import Select from './Select';
import { columns } from '../../lib/utils';

export default function StockFilter({ filter, updateFilter }) {
    const [ values, setValues ] = useState({
        left: undefined,
        right: undefined
    });
    const [operator, setOperator] = useState(undefined);

    const operators = [
        { label: ">", name: "gt" },
        { label: "<", name: "lt" },
        { label: "==", name: "eq" },
      ]

    return(
        <div className='flex space-x-1 bg-blue-500 rounded-lg max-w-fit items-center'>
            <Select field="select operand" options={columns} selection={values.left} updateSelection={(val) => setValues(state => ({...state, left: val}))} label="name" identifier='accessor' />
            <span className='text-white'>|</span>
            <Select field="select operation" options={operators} selection={operator} updateSelection={setOperator} label="label" identifier='name' />
            <span className='text-white'>|</span>
            <Select field="select operand" options={columns} selection={values.right} updateSelection={(val) => setValues(state => ({...state, right: val}))} label="name" identifier='accessor' />
        </div>
    )
}