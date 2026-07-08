import Header from "./Header";
import Footer from "./Footer";

export default function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 w-full max-w-[1120px] mx-auto px-5 py-8">{children}</main>
      <Footer />
    </div>
  );
}