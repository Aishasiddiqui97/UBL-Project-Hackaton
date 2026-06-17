// src/utils/exportCSV.js
export const exportToCSV = (data, filename = "export.csv") => {
  if (!data || data.length === 0) return;

  const headers = Object.keys(data[0]).join(",");
  const rows = data.map(row =>
    Object.values(row).map(val => `"${val}"`).join(",")
  ).join("\n");

  const csv = `${headers}\n${rows}`;
  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
};