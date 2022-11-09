import React from "react";

export default function Holder({ holder }) {
  return (
    <div className="rounded-md shadow my-2 p-2">
      <p className="font-medium">{holder.holder}</p>
      <p className="flex justify-between"><span>Date Reported:</span> <span>{holder.datereported}</span></p>
      <p className="flex justify-between"><span>Shares:</span> <span>{holder.share}</span></p>
      <p className="flex justify-between"><span>Share %:</span> <span>{ holder.sharepercentage }</span></p>
      <p className="flex justify-between"><span>Value:</span> <span>${ holder.value }</span></p>
    </div>
  );
}
