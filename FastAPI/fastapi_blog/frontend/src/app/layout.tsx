import type { Metadata } from "next";
import { Public_Sans, Source_Serif_4, IBM_Plex_Mono } from "next/font/google";
import Shell from "@/components/shell/Shell";
import ToastHost from "@/components/ui/Toast";
import "./globals.css";

const ui = Public_Sans({ subsets: ["latin"], variable: "--font-ui-loaded", weight: ["400","500","600","700"] });
const serif = Source_Serif_4({ subsets: ["latin"], variable: "--font-serif-loaded", weight: ["400","500","600","700"], style: ["normal","italic"] });
const mono = IBM_Plex_Mono({ subsets: ["latin"], variable: "--font-mono-loaded", weight: ["400","500"] });

export const metadata: Metadata = { title: "Blog API", description: "A content-first publishing platform." };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${ui.variable} ${serif.variable} ${mono.variable}`}>
      <body>
        <Shell>{children}</Shell>
        <ToastHost />
      </body>
    </html>
  );
}