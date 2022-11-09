import React, { useEffect } from "react";

export const InfoItem = ({ label = "label", value = "value", valueClasses="", labelClasses="" }) => {
  let val = Number(value);
            let style = ""

            if (!!val) {
              style = val < 0 ? "text-red-600" : "text-green-600";
              val = val.toLocaleString();
            } else {
              val = value
            }
  return (
    <p className="flex justify-between">
      <span className={"font-medium" + (!!labelClasses ? (" " + labelClasses) : "")}>{ label }</span>
      <span className={style + (!!valueClasses ? (" " + valueClasses) : "")}>{ val }</span>
    </p>
  );
};

export default function Quarter({ heading = "QX", info }) {

  return (
    <div className="p-2">
      <h3 className="font-bold text-xl underline">{heading}</h3>
      {
          Object.entries(info).map(item => {
            return <InfoItem label={item[0]} value={item[1]} />
          })
      }
    </div>
  );
}
