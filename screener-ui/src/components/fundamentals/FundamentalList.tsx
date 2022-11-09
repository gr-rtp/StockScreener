import React, { useEffect, useState } from "react";
import { Disclosure, Transition } from "@headlessui/react";
import { StockFundamentals } from "../../types/fundamental";
import Quarter, { InfoItem } from "./Quarter";
import Holder from "./Holder";
import { IoMdArrowDropdown } from "react-icons/io";

type Props = {
  stock: StockFundamentals;
};

const DropSection = ({ heading = "Section", children }) => {
  return (
    <Disclosure>
      {({ open }) => {
        return (
          <>
            <Disclosure.Button className="w-full text-left font-medium text-gray-600 text-xl px-2 py-1 rounded-md bg-gray-200">
              <div className="flex justify-between">
                <span>{heading}</span>

                <IoMdArrowDropdown className={open ? '' : 'rotate-90'} />
              </div>
            </Disclosure.Button>
            <Transition
              show={open}
              enter="transition duration-100 ease-out"
              enterFrom="transform -translate-y-5 opacity-0"
              enterTo="transform translate-y-0 opacity-100"
              leave="transition duration-75 ease-out"
              leaveFrom="transform translate-y-0 opacity-100"
              leaveTo="transform -translate-y-5 opacity-0"
            >
              <Disclosure.Panel static>
                <div className="p-2 text-lg">{children}</div>
              </Disclosure.Panel>
            </Transition>
          </>
        );
      }}
    </Disclosure>
  );
};

export default function FundamentalList({ stock }: Props) {
  const [pastYears, setPastYears] = useState({});
  const [holders, setHolders] = useState([]);

  if (!stock) {
    return <h3>No Data.</h3>;
  }

  useEffect(() => {
    const pastYears = {};

    Object.keys(stock).forEach((key) => {
      const year = stripYear(key);

      if (year.startsWith("20")) {
        if (!!pastYears[year]) {
          pastYears[year][key] = stock[key];
        } else {
          pastYears[year] = {
            [key]: stock[key],
          };
        }
      }

      if (key == "InstitutionalHolders") {
        const val = stock.InstitutionalHolders.slice(2, -3).replaceAll("\\n", "");
        setHolders(JSON.parse(val));
      }

      if (key = "MajorHolders:") {
        console.log(stock["MajorHolders:"])
      }
    });

    setPastYears(pastYears);
  }, [stock]);

  const stripYear = (string: string) => string.slice(0, 4);
  const stripPrefix = (string: string) => string.slice(16);

  const identifyQuarter = (string: string) => {
    if (string.includes("Quarter1")) {
      return "Q1";
    } else if (string.includes("Quarter2")) {
      return "Q2";
    } else if (string.includes("Quarter3")) {
      return "Q3";
    } else if (string.includes("Quarter4")) {
      return "Q4";
    }
  };

  return (
    <div className="space-y-2 text-gray-700 h-full overflow-y-auto">
      <DropSection heading="Entity Overview">
        <div>
          <InfoItem label="Name:" value={stock["Name:"]} />
          <InfoItem label="Industry:" value={stock["Industry:"]} />
          <InfoItem label="Sector:" value={stock["Sector:"]} />
          <InfoItem label="Country:" value={stock["Country:"]} />
          <InfoItem label="Description:" value="  " />
          <p className="text-sm">{stock["Description:"]}</p>
        </div>
      </DropSection>
      <DropSection heading="Stock Overview">
        <div>
          <InfoItem
            label="Trading Since:"
            value={
              stock["IpoDate:"] +
              " " +
              "(approx. " +
              stock["IpoAge:"] +
              " years)"
            }
          />
          <InfoItem
            label="Market Cap.:"
            value={stock["MarketCapitalization:"]}
          />
          <InfoItem label="Trading Since:" value={stock["IpoDate:"]} />
          <InfoItem label="Institutional Holders:" value="  " />
          {holders.map((item) => (
            <Holder holder={item} />
          ))}
        </div>
      </DropSection>
      <DropSection heading="Earnings">
        <div>
          <InfoItem label="PE Ratio:" value={stock.priceEarningsRatio} />
          <InfoItem label="Price Fair Value:" value={stock.priceFairValue} />
          <InfoItem
            label="Price to Book Ratio:"
            value={stock.priceToBookRatio}
          />
          <InfoItem
            label="Price to Sales Ratio:"
            value={stock.priceToSalesRatio}
          />
          <InfoItem label="Return on CE:" value={stock.returnOnCE} />
          <InfoItem label="Return on Equity:" value={stock.returnOnEquity} />
          <InfoItem label="Debt Ratio:" value={stock.debtRatio} />
        </div>
      </DropSection>
      <DropSection heading="Trading Volume">
        {Object.entries(stock).map((item) => {
          if (item[0].startsWith("Volume")) {
            return <InfoItem label={item[0]} value={item[1]} />;
          }
        })}
      </DropSection>
      {Object.keys(pastYears).map((year) => {
        return (
          <DropSection key={year} heading={year + " Financials"}>
            {(() => {
              const quarters = {};

              Object.keys(pastYears[year]).forEach((key) => {
                const quarter = identifyQuarter(key);
                const quarterKey = stripPrefix(key);

                if (!!quarters[quarter]) {
                  quarters[quarter][quarterKey] = pastYears[year][key];
                } else {
                  quarters[quarter] = {
                    [quarterKey]: pastYears[year][key],
                  };
                }
              });

              return Object.entries(quarters).map((quarter) => {
                return (
                  <Quarter
                    key={quarter[0]}
                    heading={quarter[0]}
                    info={quarter[1]}
                  />
                );
              });
            })()}
          </DropSection>
        );
      })}
    </div>
  );
}
