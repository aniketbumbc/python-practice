"use client";
import Link from "next/link";
import { useAuth } from "@/store/auth";
import Button from "@/components/ui/Button";
import AvatarMenu from "./AvatarMenu";

export default function Header() {
  const { currentUser } = useAuth();
  return (
    <header className="h-16 border-b border-divider bg-surface">
      <div className="h-full max-w-[1120px] mx-auto px-5 flex items-center gap-4">
        <Link href="/" className="flex items-center gap-2.5 shrink-0">
          <span className="w-[30px] h-[30px] grid place-items-center rounded-lg bg-primary text-ink font-serif font-bold">B</span>
          <span className="font-serif font-bold text-lg text-ink">Blog API</span>
        </Link>
        <input
          placeholder="Search posts…"
          className="focus-ring ml-auto h-10 w-52 px-3 rounded-[9px] bg-page text-sm border border-border-strong placeholder:text-subtle"
        />
        {currentUser ? (
          <>
            <Link href="/posts/new"><Button>＋ New Post</Button></Link>
            <AvatarMenu user={currentUser} />
          </>
        ) : (
          <>
            <Link href="/login"><Button variant="ghost">Log in</Button></Link>
            <Link href="/signup"><Button>Sign up</Button></Link>
          </>
        )}
      </div>
    </header>
  );
}