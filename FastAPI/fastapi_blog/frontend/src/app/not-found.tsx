import Link from "next/link";
import Button from "@/components/ui/Button";

export default function NotFound() {
  return (
    <div className="py-24 flex flex-col items-center text-center gap-4">
      <p className="font-serif text-[72px] font-bold text-ink leading-none">4<span className="text-primary">?</span>4</p>
      <p className="text-lg text-muted">We {"couldn't"} find that page.</p>
      <div className="flex gap-2">
        <Link href="/"><Button>Back to feed</Button></Link>
        <Link href="/writers"><Button variant="secondary">Browse writers</Button></Link>
      </div>
    </div>
  );
}