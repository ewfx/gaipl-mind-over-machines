/* eslint-disable prettier/prettier */
// App.js
import React from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import Sidebar from "./Sidebar";
import EditorArea from "./EditorArea";

const Chain = () => {
    console.log("WOrking...............")
  return (
    <DndProvider backend={HTML5Backend}>
      <div style={{ display: "flex" }}>
        <Sidebar />
        <EditorArea />
      </div>
    </DndProvider>
  );
};

export default Chain;
