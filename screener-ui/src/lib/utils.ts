export const columns = [
    {
      name: "SYMBOL",
      accessor: "symbol",
      className: "font-medium text-gray-600",
      required: true,
    },
    {
      name: "Open Price",
      accessor: "open",
      className: "text-blue-800",
      required: false,
    },
    {
      name: "Close Price",
      accessor: "close",
      className: "text-blue-800",
      required: false,
    },
    {
      name: "Volume Traded",
      accessor: "volume",
      className: "",
      required: false,
    },
    {
      name: "Relative Strength",
      accessor: "relative_strength_sp500",
      className: "text-blue-800",
      required: false,
    },
    {
      name: "Relative Strength Rank",
      accessor: "rank",
      className: "",
      required: true,
    },
  ];