import Link from "next/link";

const links = ["About", "Writers", "API docs", "Privacy", "Terms"];

export default function Footer() {
  return (
    <footer className="border-t border-divider bg-surface">
      <div className="max-w-[1120px] mx-auto px-5 py-6 flex flex-wrap items-center justify-between gap-3">
        <span className="text-sm text-muted">
          <span className="font-serif font-bold text-ink">Blog API</span> · © {new Date().getFullYear()}
        </span>
        <nav className="flex gap-4 text-sm text-muted">
          {links.map((l) => <Link key={l} href="#" className="hover:text-text">{l}</Link>)}
        </nav>
      </div>
    </footer>
  );
}