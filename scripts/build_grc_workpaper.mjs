#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const scriptPath = path.resolve(process.argv[1]);
const root = process.env.PROJECT_ROOT
  ? path.resolve(process.env.PROJECT_ROOT)
  : path.resolve(path.dirname(scriptPath), "..");
const dataDir = path.join(root, "data");
const outputPath = path.join(root, "output", "workbook", "BSI_Public_Evidence_GRC_Workpaper.xlsx");
const deliveryPath = path.resolve(root, "..", "outputs", "grc-audit-workpaper", "BSI_Public_Evidence_GRC_Workpaper.xlsx");
const renderDir = path.join(root, "tmp", "workbook-renders");

const sheetSpecs = [
  {
    csv: "source_catalog.csv",
    name: "Source_Catalog",
    table: "SourceCatalogTable",
    widths: [12, 28, 46, 15, 22, 14, 33, 65, 15, 55],
  },
  {
    csv: "incident_timeline.csv",
    name: "Incident_Timeline",
    table: "IncidentTimelineTable",
    widths: [12, 15, 11, 35, 75, 32, 15, 16],
  },
  {
    csv: "evidence_claims.csv",
    name: "Evidence_Claims",
    table: "EvidenceClaimsTable",
    widths: [12, 24, 72, 33, 16, 17, 65],
  },
  {
    csv: "control_observability.csv",
    name: "Control_Observability",
    table: "ControlObservabilityTable",
    widths: [12, 27, 67, 18, 77, 18, 31, 52],
  },
  {
    csv: "recommendation_register.csv",
    name: "Recommendations",
    table: "RecommendationsTable",
    widths: [15, 10, 17, 28, 68, 58, 18, 52, 45, 35],
  },
];

const columnName = (index) => {
  let value = index + 1;
  let result = "";
  while (value > 0) {
    const remainder = (value - 1) % 26;
    result = String.fromCharCode(65 + remainder) + result;
    value = Math.floor((value - 1) / 26);
  }
  return result;
};

async function csvMatrix(filename) {
  const text = await fs.readFile(path.join(dataDir, filename), "utf8");
  const imported = await Workbook.fromCSV(text, { sheetName: "Imported" });
  const used = imported.worksheets.getItem("Imported").getUsedRange(true);
  return used.values;
}

function applyBaseStyle(sheet, lastColumn, lastRow) {
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(1);
  const used = sheet.getRange(`A1:${lastColumn}${lastRow}`);
  used.format = {
    font: { name: "Arial", size: 9, color: "#111111" },
    verticalAlignment: "top",
  };
  const header = sheet.getRange(`A1:${lastColumn}1`);
  header.format = {
    fill: "#404040",
    font: { name: "Arial", size: 9, bold: true, color: "#FFFFFF" },
    verticalAlignment: "center",
    wrapText: true,
    borders: { preset: "outside", style: "thin", color: "#404040" },
    rowHeight: 30,
  };
  if (lastRow > 1) {
    const body = sheet.getRange(`A2:${lastColumn}${lastRow}`);
    body.format = {
      font: { name: "Arial", size: 9, color: "#111111" },
      verticalAlignment: "top",
      wrapText: true,
      borders: {
        insideHorizontal: { style: "thin", color: "#D9D9D9" },
        bottom: { style: "thin", color: "#BFBFBF" },
      },
    };
    body.format.rowHeight = 58;
  }
}

function setWidths(sheet, widths, lastRow) {
  widths.forEach((width, index) => {
    const col = columnName(index);
    sheet.getRange(`${col}1:${col}${lastRow}`).format.columnWidth = width;
  });
}

function buildCover(workbook) {
  const sheet = workbook.worksheets.add("Cover");
  sheet.showGridLines = false;
  sheet.mergeCells("A1:F1");
  sheet.getRange("A1").values = [["PUBLIC-EVIDENCE INCIDENT ASSESSMENT WORKPAPER"]];
  sheet.getRange("A1:F1").format = {
    fill: "#404040",
    font: { name: "Arial", size: 15, bold: true, color: "#FFFFFF" },
    verticalAlignment: "center",
    rowHeight: 34,
  };

  const metadata = [
    ["Subject", "Bank Syariah Indonesia - May 2023 service disruption and cyber incident"],
    ["Assessment type", "Independent public-evidence IT GRC case study"],
    ["Research cut-off", "13 July 2026"],
    ["Evidence base", "Issuer disclosures, OJK release and regulation, audited filing, law, NIST guidance, and attributed Reuters reporting"],
    ["Assessment boundary", "Public observability only; not an internal audit or control-effectiveness opinion"],
    ["Prepared for", "Portfolio review and interview discussion"],
  ];
  sheet.getRange("A3:B8").values = metadata;
  sheet.getRange("A3:A8").format = {
    fill: "#E7E6E6",
    font: { name: "Arial", size: 9, bold: true, color: "#111111" },
    verticalAlignment: "top",
  };
  sheet.getRange("B3:B8").format = {
    font: { name: "Arial", size: 9, color: "#111111" },
    wrapText: true,
    verticalAlignment: "top",
  };
  sheet.getRange("A3:B8").format.borders = {
    insideHorizontal: { style: "thin", color: "#D9D9D9" },
    bottom: { style: "thin", color: "#BFBFBF" },
  };
  sheet.getRange("A3:B8").format.rowHeight = 34;

  sheet.getRange("A10:B10").values = [["CONTROL TOTAL", "FORMULA RESULT"]];
  sheet.getRange("A10:B10").format = {
    fill: "#404040",
    font: { name: "Arial", size: 9, bold: true, color: "#FFFFFF" },
  };
  sheet.getRange("A11:A15").values = [
    ["Registered public sources"],
    ["Timeline events"],
    ["Evidence claims"],
    ["Control domains"],
    ["Recommendations"],
  ];
  sheet.getRange("B11:B15").formulas = [
    ["=COUNTA(Source_Catalog!A2:A10)"],
    ["=COUNTA(Incident_Timeline!A2:A8)"],
    ["=COUNTA(Evidence_Claims!A2:A13)"],
    ["=COUNTA(Control_Observability!A2:A11)"],
    ["=COUNTA(Recommendations!A2:A9)"],
  ];
  sheet.getRange("A11:B15").format = {
    font: { name: "Arial", size: 9, color: "#111111" },
    borders: {
      insideHorizontal: { style: "thin", color: "#D9D9D9" },
      bottom: { style: "thin", color: "#BFBFBF" },
    },
  };
  sheet.getRange("B11:B15").format = {
    font: { name: "Arial", size: 9, bold: true, color: "#111111" },
    numberFormat: "0",
    horizontalAlignment: "right",
  };

  sheet.getRange("A17:F17").merge();
  sheet.getRange("A17").values = [["REVIEW NOTE"]];
  sheet.getRange("A17:F17").format = {
    fill: "#E7E6E6",
    font: { name: "Arial", size: 9, bold: true, color: "#111111" },
  };
  sheet.getRange("A18:F20").merge();
  sheet.getRange("A18").values = [["A public source can show that an event, statement, or action was disclosed. It normally cannot prove that an internal control was appropriately designed, operated consistently, or passed independent testing. Rows marked 'Not publicly observable' are therefore not classified as control failures."]];
  sheet.getRange("A18:F20").format = {
    font: { name: "Arial", size: 9, color: "#111111" },
    wrapText: true,
    verticalAlignment: "top",
    borders: { preset: "outside", style: "thin", color: "#BFBFBF" },
  };

  sheet.getRange("A1:A20").format.columnWidth = 29;
  sheet.getRange("B1:B20").format.columnWidth = 78;
  sheet.getRange("C1:F20").format.columnWidth = 15;
  sheet.getRange("A18:F20").format.rowHeight = 24;
  sheet.freezePanes.freezeRows(1);
}

async function buildWorkbook() {
  const workbook = Workbook.create();

  for (const spec of sheetSpecs) {
    const matrix = await csvMatrix(spec.csv);
    const sheet = workbook.worksheets.add(spec.name);
    const rows = matrix.length;
    const columns = matrix[0].length;
    const lastColumn = columnName(columns - 1);
    sheet.getRange(`A1:${lastColumn}${rows}`).values = matrix;
    applyBaseStyle(sheet, lastColumn, rows);
    setWidths(sheet, spec.widths, rows);
    const table = sheet.tables.add(`A1:${lastColumn}${rows}`, true, spec.table);
    table.style = "TableStyleLight1";
    table.showBandedRows = false;
    table.showFilterButton = true;
  }

  buildCover(workbook);

  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.mkdir(path.dirname(deliveryPath), { recursive: true });
  await fs.mkdir(renderDir, { recursive: true });

  const exported = await SpreadsheetFile.exportXlsx(workbook);
  await exported.save(outputPath);
  await exported.save(deliveryPath);

  const imported = await SpreadsheetFile.importXlsx(await FileBlob.load(outputPath));
  const sheetNames = ["Cover", ...sheetSpecs.map((spec) => spec.name)];
  for (const sheetName of sheetNames) {
    const preview = await imported.render({
      sheetName,
      autoCrop: "all",
      scale: 1,
      format: "png",
    });
    const filename = `${sheetName.toLowerCase()}-preview.png`;
    await fs.writeFile(path.join(renderDir, filename), new Uint8Array(await preview.arrayBuffer()));
  }

  const inspection = await imported.inspect({
    kind: "workbook,sheet,table,formula",
    maxChars: 12000,
    tableMaxRows: 4,
    tableMaxCols: 8,
    tableMaxCellChars: 100,
  });
  const inspectionText = inspection.ndjson ?? JSON.stringify(inspection);
  const formulaErrors = inspectionText.match(/#(?:REF!|DIV\/0!|VALUE!|NAME\?|N\/A)/g) ?? [];
  if (formulaErrors.length > 0) {
    throw new Error(`Formula errors detected: ${[...new Set(formulaErrors)].join(", ")}`);
  }

  console.log(`workbook=${outputPath}`);
  console.log(`delivery=${deliveryPath}`);
  console.log(`sheets=${sheetNames.length}`);
  console.log(`renders=${sheetNames.length}`);
  console.log("formula_errors=0");
  console.log(inspectionText.slice(0, 3500));
}

await buildWorkbook();
