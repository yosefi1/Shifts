import React, { useState, useEffect, useRef } from "react";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";
import { AgGridReact } from "ag-grid-react";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

const MyAgGridComponent = (props: any) => {
  const gridRef = useRef(null);
  const { args } = props;
  const rowData = args.data;
  const workers = args.workers;

  const columnDefs = [
    { field: "position", headerName: "עמדה", editable: false },
    ...args.columns.map((col: string) => ({
      field: col,
      editable: true,
      cellEditor: 'agSelectCellEditor',
      cellEditorParams: {
        values: workers,
      }
    }))
  ];

  const onCellValueChanged = () => {
    const api = (gridRef.current as any).api;
    const updatedData = [];
    api.forEachNode((node: any) => updatedData.push(node.data));
    Streamlit.setComponentValue(updatedData);
  };

  return (
    <div className="ag-theme-alpine" style={{ height: 500, width: "100%" }}>
      <AgGridReact
        ref={gridRef}
        rowData={rowData}
        columnDefs={columnDefs}
        onCellValueChanged={onCellValueChanged}
        singleClickEdit={true}
        stopEditingWhenCellsLoseFocus={false}
      />
    </div>
  );
};

export default withStreamlitConnection(MyAgGridComponent);
