import React from "react";
import { Transition } from "@headlessui/react";

export default function Slideout({ children, open, handleClose }) {
  return (
    <Transition
      as="div"
      appear={true} //THIS will make the transition run everytime the component is rendered
      show={open}
      className="fixed inset-0"
    >
      <Transition.Child
      as="div"
        enter="transition-opacity ease-linear duration-150"
        enterFrom="opacity-0"
        enterTo="opacity-60"
        leave="transition-opacity ease-linear duration-150"
        leaveFrom="opacity-60"
        leaveTo="opacity-0"
        className="bg-gray-400 w-full h-full opacity-60"
        onClick={handleClose}
      >
      </Transition.Child>
      <Transition.Child
      as="div"
        enter="transition ease-in-out duration-150 transform"
        enterFrom="translate-x-full"
        enterTo="translate-x-0"
        leave="transition ease-in-out duration-150 transform"
        leaveFrom="translate-x-0"
        leaveTo="translate-x-full"
        className="absolute top-0 right-0 bottom-0 max-w-xl w-full bg-white m-1 rounded p-2"
      >
          {children}
      </Transition.Child>
    </Transition>
  );
}
