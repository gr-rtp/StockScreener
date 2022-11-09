import React from "react";
import Section from "./Section";

export default function StockList({ stocks = [], columns = [], onStockSelect }) {

  return (
    <Section>
      <p>Showing all {stocks.length} stocks</p>
      <table className="w-full table-auto">
      <thead className="p-4">
        {columns.map((item) => (
          <td key={item.name} className="p-2 text-sm font-bold text-gray-700">{item.name}</td>
        ))}
      </thead>
      <tbody>
      {stocks.map((stock, i) => {
        const bg = i % 2 == 0 ? " bg-gray-50" : "";

        return (
          <tr
            key={stock[""]}
            className={
              "rounded cursor-pointer hover:bg-blue-50" +
              bg
            }
            onClick={() => onStockSelect(stock)}
          >
            {
              columns.map((column) => {
                let val = Number(stock[column.accessor]);

                if (!!val) {
                  val = val.toLocaleString();
                } else {
                  val = stock[column.accessor]
                }
                
                return <td className={"p-2 text-left " + column.className}>{ val }</td>
              })
            }
          </tr>
        );
      })}
      </tbody>
      </table>
    </Section>
  );
}
