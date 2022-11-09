import React, { useEffect, useState } from "react";
import Section from "../components/container/Section";
import Slideout from "../components/container/Slideout";
import StockList from "../components/container/StockList";
import "../styles/global.css";
import Papa from "papaparse";
import FundamentalList from "../components/fundamentals/FundamentalList";
import { IoMdRefreshCircle } from "react-icons/io";
import { StockFundamentals } from "../types/fundamental";
import Overview from "../components/metrics/Overview";
import Select from "../components/input/Select";
import { columns  } from "../lib/utils";
import StockFilter from "../components/input/StockFilter";

// markup
const IndexPage = () => {
  const [selectedStock, setSelectedStock] = useState(undefined);
  const [selectedFunds, setSelectedFunds] = useState(undefined);
  const [stocks, setStocks] = useState([]);
  const [loadinStocks, setLoadingStocks] = useState(false);
  const [fundamentals, setFundamentals] = useState<StockFundamentals[]>([]);
  const [metrics, setMetrics] = useState({
    sector: [],
    industry: [],
    strength: []
  });

  useEffect(() => {
    init();
  }, []);

  const init = async () => {
    setLoadingStocks(true);

    const rows = await getData("/data/technicals.csv");
    getData("/data/fundamentals.csv").then((data) => {
      setFundamentals(data);
    });

    setLoadingStocks(false);
    setStocks(rows);
  };

  useEffect(() => {
    const metrics = {
      "Sector:": {},
      "Industry:": {}
    }

    fundamentals.forEach((stock) => {
      if (stock["Sector:"]) {
        if (!!metrics["Sector:"][stock["Sector:"]]) {
          metrics["Sector:"][stock["Sector:"]] += 1
        } else {
          metrics["Sector:"][stock["Sector:"]] = 1
        }
      }

      if (stock["Industry:"]) {
        if (!!metrics["Industry:"][stock["Industry:"]]) {
          metrics["Industry:"][stock["Industry:"]] += 1
        } else {
          metrics["Industry:"][stock["Industry:"]] = 1
        }
      }
    });

    const sectors = Object.entries(metrics["Sector:"]).map(item => ({ name: item[0], value: item[1] })).sort((a, b) => a.value - b.value);
    const industries = Object.entries(metrics["Industry:"]).map(item => ({ name: item[0], value: item[1] })).sort((a, b) => a.value - b.value);

    setMetrics((state) => ({
      ...state,
      sector: sectors,
      industry: industries
    }));
  }, [fundamentals]);


  // useEffect(() => {
  //   const metrics = {
  //     strength: []
  //   }


  // }, [stocks])

  useEffect(() => {
    if (!selectedStock) {
      setSelectedFunds(undefined);
    } else {
      const result = fundamentals.find((item) => {
        return item.STOCK == selectedStock.symbol;
      });

      // console.log(result)

      setSelectedFunds(result);
    }
  }, [selectedStock]);

  async function getData(path: string) {
    const response = await fetch(path);
    const reader = response?.body?.getReader();
    const result = await reader?.read(); // raw array
    const decoder = new TextDecoder("utf-8");
    const csv = decoder.decode(result?.value); // the csv text
    const results = Papa.parse(csv, { header: true }); // object with { data, errors, meta }
    return results.data; // array of objects
  }

  return (
    <main>
      <title>Super Stock Screener</title>

      <Overview sectors={metrics.sector} industries={metrics.industry} strength={metrics.strength} />

      {loadinStocks ? (
        <div className="flex items-center justify-center my-14">
          <IoMdRefreshCircle size={50} className="animate-spin text-blue-500 mt-20" />
        </div>
      ) : (
        <StockList stocks={stocks} onStockSelect={setSelectedStock} columns={columns} />
      )}

      <Slideout
        open={!!selectedStock}
        handleClose={() => setSelectedStock(undefined)}
      >
        {!!selectedStock ? <FundamentalList stock={selectedFunds} /> : null}
      </Slideout>
    </main>
  );
};

export default IndexPage;
