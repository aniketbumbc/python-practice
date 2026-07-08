"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/store/auth";
import { useToast } from "@/store/toast";
import Avatar from "@/components/ui/Avatar";
import type { User } from "@/lib/types";

export default function AvatarMenu({ user }: { user: User }) {
  const [open, setOpen] = useState(false);
  const { logout } = useAuth();
  const push = useToast((s) => s.push);
  const router = useRouter();

  return (
    <div className="relative">
      <button onClick={() => setOpen((o) => !o)} className="focus-ring rounded-full">
        <Avatar src={user.avatarUrl} size={38} />
      </button>
      {open && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />
          <div className="absolute right-0 mt-2 w-56 z-20 bg-surface border border-border rounded-[12px] shadow-[var(--shadow-card)] p-1.5">
            <div className="px-3 py-2 border-b border-divider">
              <p className="text-sm font-semibold text-ink">{user.username}</p>
              <p className="text-xs text-subtle">@{user.handle}</p>
            </div>
            <Link href={`/u/${user.handle}`} className="block px-3 py-2 text-sm rounded-md hover:bg-page" onClick={() => setOpen(false)}>Profile</Link>
            <Link href="/settings" className="block px-3 py-2 text-sm rounded-md hover:bg-page" onClick={() => setOpen(false)}>Settings</Link>
            <button
              className="w-full text-left px-3 py-2 text-sm rounded-md text-danger hover:bg-danger-bg"
              onClick={() => { logout(); setOpen(false); push("Signed out"); router.push("/"); }}
            >Log out</button>
          </div>
        </>
      )}
    </div>
  );
}