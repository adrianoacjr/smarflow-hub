import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./style.css";
import { ThemeProvider } from "@/components/theme-provider";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TestPage from "./pages/Test";

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
            <BrowserRouter>
            <Routes>
                <Route path="/" element={<App />} />
                <Route path="/test" element={<TestPage />} />
            </Routes>
            </BrowserRouter>
        </ThemeProvider>
    </React.StrictMode>
);
