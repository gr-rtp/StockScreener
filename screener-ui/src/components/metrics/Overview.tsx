import React, { useEffect, useState } from "react";
import Section from "../container/Section";
import {
  PieChart,
  Pie,
  ResponsiveContainer,
  Tooltip,
  BarChart,
  Cell,
  XAxis,
  YAxis,
  Legend,
  Bar,
  ReferenceLine,
} from "recharts";

const colors = getColorArray(20);
const RADIAN = Math.PI / 180;

const renderCustomizedLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
  index,
}) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.7;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  if (percent > 0.05) {
    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? "start" : "end"}
        dominantBaseline="central"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  }
};

const MyPie = ({ data, title = "Title" }) => {
  return (
    <ResponsiveContainer width="99%">
      <PieChart margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
        <text
          x={"50%"}
          y={20}
          fill="gray"
          textAnchor="middle"
          dominantBaseline="central"
        >
          <tspan fontSize="20">{ title }</tspan>
        </text>
        <Pie
          data={data}
          dataKey="value"
          isAnimationActive={false}
          cx="50%"
          cy="50%"
          outerRadius={120}
          fill="#8884d8"
          labelLine={false}
          label={renderCustomizedLabel}
          blendStroke={true}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
          ))}
        </Pie>

        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
};
export default function Overview({ sectors, industries, strength }) {
  return (
    <Section>
      <div className="flex justify-between h-96 max-w-96">
        <div className="flex flex-col whitespace-nowrap text-xl">
            <span><span className="font-bold">Dataset:</span> All Stocks vs S&P500</span>
            <span><span className="font-bold">Date:</span> 2022-06-11</span>
        </div>

        <MyPie data={sectors} title={"Sector Overview"} />

        <MyPie data={industries} title={"Industry Overview"} />
      </div>
    </Section>
  );
}

function getColorArray(num: number) {
  var result = [
    "#EC6B56",
    "#FFC154",
    "#47B39C",
    "#5867d6",
    "#d47f24",
    "#36c943",
    "#3d82db",
    "#FFA600",
    "#db3d4d",
    "#FF6361",
    "#003F5C",
    "#e6d240",
    "#58508D"
  ];
  for (var i = 0; i < num; i += 1) {
    var letters = "0123456789ABCDEF".split("");
    var color = "#";
    for (var j = 0; j < 6; j += 1) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    result.push(color);
  }
  return result;
}
