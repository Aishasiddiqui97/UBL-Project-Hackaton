/**
 * Print a report to PDF or printer
 * @param {string} title - Report title
 * @param {Array} headers - Table headers
 * @param {Array} data - Table data rows
 * @param {Object} options - Additional options
 */
export const printReport = (title, headers, data, options = {}) => {
  const {
    filename = `${title.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.html`,
    orientation = 'portrait',
    includeTimestamp = true,
    logo = null,
    footer = null,
  } = options;

  // Build HTML content
  const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>${title}</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      padding: 20px;
      color: #1e293b;
      line-height: 1.5;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
      padding-bottom: 20px;
      border-bottom: 2px solid #e2e8f0;
    }
    .header h1 {
      font-size: 24px;
      font-weight: 700;
      color: #0f172a;
    }
    .header .timestamp {
      font-size: 12px;
      color: #64748b;
    }
    .logo {
      max-height: 50px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    th, td {
      padding: 12px 16px;
      text-align: left;
      border-bottom: 1px solid #e2e8f0;
    }
    th {
      background: #f8fafc;
      font-weight: 600;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #475569;
    }
    td {
      font-size: 13px;
    }
    tr:nth-child(even) {
      background: #f8fafc;
    }
    .footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #e2e8f0;
      font-size: 11px;
      color: #94a3b8;
      text-align: center;
    }
    @media print {
      body {
        padding: 0;
      }
      .no-print {
        display: none;
      }
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h1>${title}</h1>
      ${includeTimestamp ? `<div class="timestamp">Generated on ${new Date().toLocaleString()}</div>` : ''}
    </div>
    ${logo ? `<img src="${logo}" alt="Logo" class="logo">` : ''}
  </div>
  
  <table>
    <thead>
      <tr>
        ${headers.map(header => `<th>${header}</th>`).join('')}
      </tr>
    </thead>
    <tbody>
      ${data.map(row => `
        <tr>
          ${row.map(cell => `<td>${cell ?? '-'}</td>`).join('')}
        </tr>
      `).join('')}
    </tbody>
  </table>
  
  ${footer ? `<div class="footer">${footer}</div>` : `
    <div class="footer">
      <p>AFCIP - Anti Financial Crime Intelligence Platform</p>
      <p>This report is confidential and intended for authorized personnel only.</p>
    </div>
  `}
  
  <div class="no-print" style="position: fixed; bottom: 20px; right: 20px;">
    <button onclick="window.print()" style="
      background: #38bdf8;
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">Print Report</button>
  </div>
</body>
</html>
  `;

  // Open in new window for printing
  const printWindow = window.open('', '_blank');
  if (printWindow) {
    printWindow.document.write(htmlContent);
    printWindow.document.close();
  } else {
    console.error('Failed to open print window. Please allow popups.');
  }
};

/**
 * Export data to CSV
 * @param {string} title - Report title
 * @param {Array} headers - Table headers
 * @param {Array} data - Table data rows
 * @param {string} filename - Filename
 */
export const exportToCSV = (title, headers, data, filename) => {
  const csvFilename = filename || `${title.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.csv`;
  
  // Build CSV content
  const csvContent = [
    headers.join(','),
    ...data.map(row => row.map(cell => {
      // Escape values that contain commas or quotes
      const cellStr = String(cell ?? '');
      if (cellStr.includes(',') || cellStr.includes('"') || cellStr.includes('\n')) {
        return `"${cellStr.replace(/"/g, '""')}"`;
      }
      return cellStr;
    }).join(','))
  ].join('\n');

  // Create and download file
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', csvFilename);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

/**
 * Export data to JSON
 * @param {Array} data - Data to export
 * @param {string} filename - Filename
 */
export const exportToJSON = (data, filename) => {
  const jsonFilename = filename || `export_${new Date().toISOString().split('T')[0]}.json`;
  
  const jsonContent = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonContent], { type: 'application/json' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  
  link.setAttribute('href', url);
  link.setAttribute('download', jsonFilename);
  link.style.visibility = 'hidden';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

export default printReport;
