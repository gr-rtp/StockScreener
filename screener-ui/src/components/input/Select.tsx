import React, { useState } from "react";
import { Transition } from "@headlessui/react";

export default function Select({
  options,
  selection,
  updateSelection,
  label = "name",
  identifier = "id",
  field = "select"
}) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <button
        className="py-1 px-4 rounded bg-blue-500 text-white"
        type="button"
        onBlur={() => setOpen(false)}
        onClick={() => setOpen(true)}
      >
        {selection ? selection[label] : field}
      </button>
      <Transition
        show={open}
        enter="transition duration-100 ease-out"
        enterFrom="transform -translate-y-5 opacity-0"
        enterTo="transform translate-y-0 opacity-100"
        leave="transition duration-75 ease-out"
        leaveFrom="transform translate-y-0 opacity-100"
        leaveTo="transform -translate-y-5 opacity-0"
      >
        <ul className="p-2 absolute top-full min-w-full bg-white rounded shadow-md">
          {options.map((item) => {
            return (
              <li key={item[identifier]} onClick={() => updateSelection(item)} className="whitespace-nowrap py-1 px-2 hover:bg-gray-100 cursor-pointer">
                {item[label]}
              </li>
            );
          })}
        </ul>
      </Transition>
    </div>
  );
}
